# Apply a watermark to a PDF file
import os
import shutil
from datetime import datetime
from looptools import Timer
from tempfile import mkdtemp
from pdfwatermarker.watermark.lib import GUI
from pdfwatermarker.watermark.draw import WatermarkDraw, resource_path, bundle_dir
from pdfwatermarker.watermark.add import WatermarkAdd
from pdfwatermarker import add_suffix, open_window, protect
from pdfwatermarker.watermark.draw import CanvasObjects, CanvasStr, CanvasImg

default_image_dir = resource_path(bundle_dir + os.sep + 'lib' + os.sep + 'img')
default_image = resource_path('wide.png')


class Receipt:
    def __init__(self):
        self.dst = None
        self.items = []
        self.add('PDF Watermarker', datetime.now().strftime("%Y-%m-%d %H:%M"))

    def set_dst(self, doc, file_name='watermark receipt.txt'):
        self.dst = os.path.join(os.path.dirname(doc), file_name)
        self.add('Directory', os.path.dirname(doc))
        self.add('PDF', os.path.basename(doc))
        return self

    def add(self, key, value):
        message = str("{0:20}--> {1}".format(key, value))
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
    def __init__(self, document, remove_temps=True, open_file=True, tempdir=mkdtemp(), receipt=None):
        self.time = Timer()
        self.document_og = document
        self.document = self.document_og
        self.watermark = None
        self.remove_temps = remove_temps
        self.open_file = open_file
        self.tempdir = tempdir

        if isinstance(receipt, Receipt):
            self.receipt = receipt
        else:
            self.receipt = Receipt().set_dst(document)

    def __str__(self):
        return str(self.document)

    def save(self):
        runtime = self.time.end
        self.receipt.add('~run time~', runtime)
        self.receipt.dump()
        if self.remove_temps:
            shutil.rmtree(self.tempdir)
        else:
            open_window(self.tempdir)
        return self.document

    def draw(self, text1, text2, copyright=True, image=default_image, opacity=0.1, compress=0, add=False):
        # Add to receipt
        self.receipt.add('Text1', text1)
        self.receipt.add('Text2', text2)
        self.receipt.add('WM Opacity', str(int(opacity * 100)) + '%')

        # Initialize CanvasObjects collector class and add objects
        objects = CanvasObjects()
        objects.add(CanvasImg(os.path.join(default_image_dir, image), opacity=opacity, x=200, y=-200))
        if copyright:
            objects.add(CanvasStr('© copyright ' + str(datetime.now().year), size=16, y=10))
        objects.add(CanvasStr(text1, opacity=opacity, y=-140))
        objects.add(CanvasStr(text2, opacity=opacity, y=-90))

        # Draw watermark to file
        self.watermark = WatermarkDraw(objects, rotate=30, tempdir=self.tempdir, compress=0).write()

        if not add:
            return self.watermark
        else:
            self.add()
            return self.save()

    def add(self, watermark=None, underneath=False):
        if not watermark:
            watermark = self.watermark
        self.document = str(WatermarkAdd(self.document, watermark, underneath=underneath, tempdir=self.tempdir))
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
        self.receipt = Receipt()
        pdf, address, town, state, opacity, encrypt, user_pw, owner_pw = GUI().settings
        self.receipt.set_dst(pdf)

        # Execute Watermark class
        wm = Watermark(pdf, receipt=self.receipt)
        wm.draw(address, str(town + ', ' + state), opacity=opacity)
        wm.add()

        if encrypt:
            wm.secure(user_pw, owner_pw)
        wm.save()

        try:
            print('\nSuccess!')
            input('~~Press Any Key To Exit~~')
        except RuntimeError:
            quit()
