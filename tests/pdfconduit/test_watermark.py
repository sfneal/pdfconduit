import unittest
import os
import shutil
import time
from pdfconduit import Watermark, slicer, Info, Label
from tests import directory, pdf as p


class TestWatermarkMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.pdfs = ['plan_l.pdf', 'plan_p.pdf', 'con docs_sliced.pdf']
        cls.pdfs = ['plan_l.pdf', 'plan_p.pdf']
        # cls.pdfs = ['con docs2_sliced.pdf']

        cls.w = Watermark(p, use_receipt=False, open_file=False)
        if 'con docs2_sliced.pdf' in cls.pdfs and not os.path.exists(os.path.join(directory, 'con docs2_sliced.pdf')):
            slicer(os.path.join(directory, 'con docs2.pdf'), first_page=1, last_page=1, suffix='sliced')

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        dst = os.path.join(results, 'watermark')

        # Create destination if it does not exist
        if not os.path.isdir(dst):
            os.mkdir(dst)

        # Move each file into results folder
        for i in cls.files:
            source = i
            target = os.path.join(dst, str(os.path.basename(i)))
            shutil.move(source, target)

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
        print("%s: %.3f" % (self.id(), t))

    def test_watermark(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate,
                                 flatten=False)
            added = self.w.add(pdf, wtrmrk)
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_underneath(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=True, suffix='watermarked_underneath')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_overlay(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=False, suffix='watermarked_overlay')
            self.files.append(added)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_flat(self):
        for pdf in self.pdfs:
            flat = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=True)
            added = self.w.add(pdf, flat, suffix='watermarked_flat')
            self.files.append(added)

            self.assertTrue(os.path.exists(flat))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_layered(self):
        for pdf in self.pdfs:
            layered = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=False)
            added = self.w.add(pdf, layered, suffix='watermarked_layered')
            self.files.append(added)

            self.assertTrue(os.path.exists(layered))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_encrypt(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08)
            added = self.w.add(pdf, wtrmrk)
            encrypted = self.w.encrypt(self.user_pw, self.owner_pw)
            security = Info(encrypted, self.user_pw).security

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(os.path.exists(encrypted))
            self.assertTrue(Info(encrypted, self.user_pw).resources())
            self.assertEqual(security['/Length'], 128)
            self.assertEqual(security['/P'], -1852)

    def test_watermark_label(self):
        for pdf in self.pdfs:
            label = os.path.basename(pdf)
            l = Label(pdf, label, tempdir=self.w.tempdir).write(cleanup=False)
            self.files.append(l)

            self.assertTrue(os.path.exists(l))
            self.assertTrue(Info(l).resources())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestWatermarkMethods("test_watermark"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    # unittest.main()
    suite()
