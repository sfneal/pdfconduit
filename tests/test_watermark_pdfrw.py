import unittest
import os
import shutil
import time
from pdfconduit import Watermark, slicer, Info, Label
from tests import *


class TestWatermarkMethodsPdfrw(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdfs = ['plan_l.pdf', 'plan_p.pdf', 'document.pdf', 'con docs2_sliced.pdf']

        cls.w = Watermark(pdf, use_receipt=False, open_file=False)
        if 'con docs2_sliced.pdf' in cls.pdfs and not os.path.exists(os.path.join(directory, 'con docs2_sliced.pdf')):
            slicer(os.path.join(directory, 'con docs2.pdf'), first_page=1, last_page=5, suffix='sliced')

        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'watermark')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        # Log destination
        cls.file_path = 'watermark_pdfrw.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        write_log(cls.csv, cls.log)
        cls.w.cleanup()

    def setUp(self):
        self.pdfs = [os.path.join(directory, pdf) for pdf in self.pdfs]
        self.address = '43 Indian Lane'
        self.town = 'Franklin'
        self.state = 'MA'
        self.rotate = 30
        self.owner_pw = 'foo'
        self.user_pw = 'baz'
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[2:]), t))

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            try:
                shutil.move(source, target)
                self.files.remove(i)
            except FileNotFoundError:
                pass

    def test_watermark_pdfrw(self):
        for pdf in self.pdfs:
            self.w.document = pdf
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate,
                                 flatten=False)
            added = self.w.add(pdf, wtrmrk, method='pdfrw', suffix='watermarked_pdfrw')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_underneath_pdfrw(self):
        for pdf in self.pdfs:
            self.w.document = pdf
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=True, suffix='watermarked_underneath_pdfrw', method='pdfrw')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_overlay_pdfrw(self):
        for pdf in self.pdfs:
            self.w.document = pdf
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=False, suffix='watermarked_overlay_pdfrw', method='pdfrw')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_flat_pdfrw(self):
        for pdf in self.pdfs:
            self.w.document = pdf
            flat = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=True)
            added = self.w.add(pdf, flat, suffix='watermarked_flat_pdfrw', method='pdfrw')
            self.files.append(added)

            self.assertTrue(os.path.exists(flat))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_layered_pdfrw(self):
        for pdf in self.pdfs:
            self.w.document = pdf
            layered = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=False)
            added = self.w.add(pdf, layered, suffix='watermarked_layered_pdfrw', method='pdfrw')
            self.files.append(added)
            self.files.append(layered)

            self.assertTrue(os.path.exists(layered))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_label(self):
        for pdf in self.pdfs:
            self.w.document = pdf
            label = os.path.basename(pdf)
            l = Label(pdf, label, tempdir=self.w.tempdir).write(cleanup=False)
            self.files.append(l)

            self.assertTrue(os.path.exists(l))
            self.assertTrue(Info(l).resources())


if __name__ == '__main__':
    unittest.main()
