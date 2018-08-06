# Apply a watermark to a PDF file
import os
import shutil
from datetime import datetime
from looptools import Timer
from tempfile import mkdtemp
from pdfwatermarker.watermark.draw import WatermarkDraw
from pdfwatermarker.watermark.add import WatermarkAdd
from pdfwatermarker.watermark.utils import resource_path, bundle_dir
from pdfwatermarker.utils.path import add_suffix
from pdfwatermarker.utils.view import open_window
from pdfwatermarker.encrypt import protect
from pdfwatermarker.watermark.canvas import CanvasObjects, CanvasStr, CanvasImg, DrawPIL

default_image_dir = resource_path(bundle_dir() + os.sep + 'lib' + os.sep + 'img')
default_image = resource_path('Wide.png')


class Receipt:
    def __init__(self, use=True):
        self.dst = None
        self.use = use
        self.items = []
        self.add('PDF Watermarker', datetime.now().strftime("%Y-%m-%d %H:%M"))

    def set_dst(self, doc, file_name='watermark receipt.txt'):
        self.dst = os.path.join(os.path.dirname(doc), file_name)
        self.add('Directory', os.path.dirname(doc))
        self.add('PDF', os.path.basename(doc))
        return self

    def add(self, key, value):
        message = str("{0:20}--> {1}".format(key, value))
        if self.use:
            print(message)
        self.items.append(message)

    def dump(self):
        exists = os.path.isfile(self.dst)
        with open(self.dst, 'a') as f:
            if exists:
                f.write('*******************************************************************\n')

            for item in self.items:
                f.write(item + '\n')


class Watermark:
    def __init__(self, document, remove_temps=True, open_file=True, tempdir=mkdtemp(), receipt=None, use_receipt=True):
        self.time = Timer()
        self.document_og = document
        self.document = self.document_og
        self.watermark = None
        self.remove_temps = remove_temps
        self.open_file = open_file
        self.tempdir = tempdir

        self.use_receipt = use_receipt
        if isinstance(receipt, Receipt):
            self.receipt = receipt
        else:
            self.receipt = Receipt(use_receipt).set_dst(document)

    def __str__(self):
        return str(self.document)

    def cleanup(self):
        runtime = self.time.end
        self.receipt.add('~run time~', runtime)
        if self.use_receipt:
            self.receipt.dump()
        if self.remove_temps:
            shutil.rmtree(self.tempdir)
        else:
            open_window(self.tempdir)
        return self.document

    def draw(self, text1, text2=None, copyright=True, image=default_image, rotate=30, opacity=0.08, compress=0,
             add=False, flatten=False):

        def get_objects():
            # Initialize CanvasObjects collector class and add objects
            obj = CanvasObjects()
            obj.add(CanvasImg(os.path.join(default_image_dir, image), opacity=opacity, x=200, y=-200))

            if not flatten:
                if copyright:
                    obj.add(CanvasStr('© copyright ' + str(datetime.now().year), size=16, y=10, opacity=opacity))
                if text2:
                    obj.add(CanvasStr(text1, opacity=opacity, size=40, y=-140))
                    obj.add(CanvasStr(text2, opacity=opacity, size=40, y=-90))
                else:
                    obj.add(CanvasStr(text1, opacity=opacity, size=40, y=-115))
            else:
                img = DrawPIL()
                if copyright:
                    img.draw_text('© copyright ' + str(datetime.now().year), size=16, y=0)
                if text2:
                    img.draw_text(text1, size=40, y=140, opacity=opacity)
                    img.draw_text(text2, size=40, y=90, opacity=opacity)
                else:
                    img.draw_text(text2, size=40, y=115, opacity=opacity)
                i = img.save(tempdir=self.tempdir)
                obj.add(CanvasImg(i, opacity=1, x=200, y=-630))
            return obj

        # Add to receipt
        self.receipt.add('Text1', text1)
        self.receipt.add('Text2', text2)
        self.receipt.add('Image', image)
        self.receipt.add('WM Opacity', str(int(opacity * 100)) + '%')
        self.receipt.add('WM Compression', compress)

        objects = get_objects()

        # Draw watermark to file
        self.watermark = WatermarkDraw(objects, rotate=rotate, compress=compress, tempdir=self.tempdir).write()

        if not add:
            return self.watermark
        else:
            self.add()
            return self.cleanup()

    def add(self, document=None, watermark=None, underneath=False, output=None):
        self.receipt.add('WM Placement', 'Overlay' if underneath else 'Underneath')
        if not watermark:
            watermark = self.watermark
        if not document:
            document = self.document
        self.document = str(WatermarkAdd(document, watermark, underneath=underneath, output=output,
                                         tempdir=self.tempdir))
        self.receipt.add('Watermarked PDF', os.path.basename(self.document))
        if self.open_file:
            open_window(self.document)
        return self.document

    def secure(self, user_pw='', owner_pw=None, encrypt_128=True, restrict_permission=True):
        self.receipt.add('User pw', user_pw)
        self.receipt.add('Owner pw', owner_pw)
        if encrypt_128:
            self.receipt.add('Encryption key size', '128')
        else:
            self.receipt.add('Encryption key size', '40')
        if restrict_permission:
            self.receipt.add('Permissions', 'Allow printing')
        else:
            self.receipt.add('Permissions', 'Allow ALL')
        p = protect(self.document, user_pw, owner_pw, output=add_suffix(self.document_og, 'secured'),
                    encrypt_128=encrypt_128, restrict_permission=restrict_permission)
        self.receipt.add('Secured PDF', os.path.basename(p))
        return p


class WatermarkGUI:
    def __init__(self):
        from pdfwatermarker.utils.gui import GUI
        self.receipt = Receipt()
        self.params = GUI().settings
        self.execute()

    def execute(self):
        self.receipt.set_dst(self.params['pdf'])

        # Execute Watermark class
        wm = Watermark(self.params['pdf'], receipt=self.receipt)
        wm.draw(text1=self.params['address'],
                text2=str(self.params['town'] + ', ' + self.params['state']),
                image=self.params['image'],
                opacity=self.params['opacity'],
                compress=self.params['compression']['compressed'])
        wm.add(underneath=self.params['placement']['underneath'])

        if self.params['encrypt']:
            wm.secure(self.params['user_pw'], self.params['owner_pw'])
        wm.cleanup()

        try:
            print('\nSuccess!')
            input('~~Press Any Key To Exit~~')
        except RuntimeError:
            quit()
