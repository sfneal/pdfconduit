# Apply a watermark to a PDF file
import os
import shutil
from datetime import datetime
from tempfile import mkdtemp
from looptools import Timer
from pdfwatermarker.utils.gui import gui_watermark
from pdfwatermarker.watermark.add import WatermarkAdd
from pdfwatermarker.watermark.lib import Receipt, bundle_dir
from pdfwatermarker.utils import add_suffix, resource_path, open_window
from pdfwatermarker.encrypt import Encrypt
from pdfwatermarker.watermark.draw import WatermarkDraw, CanvasObjects, CanvasStr, CanvasImg, DrawPIL

default_image_dir = resource_path(bundle_dir() + os.sep + 'img')
default_image = resource_path('Wide.png')


class Watermark:
    def __init__(self, document, remove_temps=True, open_file=True, tempdir=mkdtemp(), receipt=None, use_receipt=True):
        """
        Watermark and encrypt a PDF document.

        Manage watermarking processes from single class initialization.  This class utilizes the draw,
        add and encrypt modules.

        :param document: str
            PDF document full path
        :param remove_temps: bool
            Remove temporary files after completion
        :param open_file: bool
            Open file after completion
        :param tempdir: function or str
            Temporary directory for file writing
        :param receipt: cls
            Use existing Receipt object if already initiated
        :param use_receipt: bool
            Print receipt information to console and write to file
        """
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
             flatten=False, add=False):
        """
        Draw watermark PDF file.

        Create watermark using either a reportlabs canvas or a PIL image.

        :param text1: str
            Text line 1
        :param text2: str
            Text line 2
        :param copyright: bool
            Draw copyright and year to canvas
        :param image: str
            Logo image to be used as base watermark
        :param rotate: int
            Degrees to rotate canvas by
        :param opacity: float
            Watermark opacity
        :param compress: bool
            Compress watermark contents  (not entire PDF)
        :param flatten: bool
            Draw watermark with multiple layers or a single flattened layer
        :param add: bool
            Add watermark to original document
        :return: str
            Watermark PDF file full path
        """

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
        self.receipt.add('WM Flattening', flatten)

        objects = get_objects()

        # Draw watermark to file
        self.watermark = WatermarkDraw(objects, rotate=rotate, compress=compress, tempdir=self.tempdir).write()

        if not add:
            return self.watermark
        else:
            self.add()
            return self.cleanup()

    def add(self, document=None, watermark=None, underneath=False, output=None, suffix='watermarked'):
        """
        Add a watermark file to an existing PDF document.

        Rotate and upscale watermark file as needed to fit existing PDF document.  Watermark can be overlayed or
        placed underneath.

        :param document: str
            PDF document full path
        :param watermark: str
            Watermark PDF full path
        :param underneath: bool
            Place watermark either under or over existing PDF document
        :param output: str
            Output file path
        :param suffix: str
            Suffix to append to existing PDF document file name
        :return: str
            Watermarked PDF Document full path
        """
        self.receipt.add('WM Placement', 'Overlay' if underneath else 'Underneath')
        if not watermark:
            watermark = self.watermark
        if not document:
            document = self.document
        self.document = str(WatermarkAdd(document, watermark, underneath=underneath, output=output,
                                         tempdir=self.tempdir, suffix=suffix))
        self.receipt.add('Watermarked PDF', os.path.basename(self.document))
        if self.open_file:
            open_window(self.document)
        return self.document

    def encrypt(self, user_pw='', owner_pw=None, encrypt_128=True, restrict_permission=True):
        """
        Encrypt a PDF document to add passwords and restrict permissions.

        Add a user password that must be entered to view document and a owner password that must be entered to alter
        permissions and security settings.  Encryption keys are 128 bit when encrypt_128 is True and 40 bit when
        False.  By default permissions are restricted to print only, when set to false all permissions are allowed.
        TODO: Add additional permission parameters

        :param user_pw: str
            User password required to open and view PDF document
        :param owner_pw: str
            Owner password required to alter security settings and permissions
        :param encrypt_128: bool
            Encrypt PDF document using 128 bit keys
        :param restrict_permission: bool
            Restrict permissions to print only
        :return: str
            Encrypted PDF full path
        """
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
        p = Encrypt(self.document, user_pw, owner_pw, output=add_suffix(self.document_og, 'secured'),
                    encrypt_128=encrypt_128, restrict_permission=restrict_permission)
        self.receipt.add('Secured PDF', os.path.basename(p))
        return p


class WatermarkGUI:
    def __init__(self):
        self.receipt = Receipt()
        self.params = gui_watermark().settings
        self.execute()

    def execute(self):
        self.receipt.set_dst(self.params['pdf'])

        # Execute Watermark class
        wm = Watermark(self.params['pdf'], receipt=self.receipt)
        wm.draw(text1=self.params['address'],
                text2=str(self.params['town'] + ', ' + self.params['state']),
                image=self.params['image'],
                opacity=self.params['opacity'],
                compress=self.params['compression']['compressed'],
                flatten=self.params['flattening']['flattened'])
        wm.add(underneath=self.params['placement']['underneath'])

        if self.params['encrypt']:
            wm.encrypt(self.params['user_pw'], self.params['owner_pw'])
        wm.cleanup()

        try:
            print('\nSuccess!')
            input('~~Press Any Key To Exit~~')
            quit()
        except RuntimeError:
            quit()
