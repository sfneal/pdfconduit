import unittest
import os
from pdfconduit import Watermark, slicer, Info, Label
from tests import directory, pdf as p


class TestWatermarkMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pdfs = ['plan_l.pdf', 'plan_p.pdf']
        # pdfs.append('con docs_sliced.pdf')

        cls.w = Watermark(p, use_receipt=False, open_file=False)
        if 'con docs_sliced.pdf' in pdfs and not os.path.exists(os.path.join(directory, 'con docs_sliced.pdf')):
            slicer(os.path.join(directory, 'con docs.pdf'), first_page=1, last_page=1, suffix='sliced')

    @classmethod
    def tearDownClass(cls):
        cls.w.cleanup()

    def setUp(self):
        self.pdfs = [os.path.join(directory, pdf) for pdf in pdfs]
        self.address = '43 Indian Lane'
        self.town = 'Franklin'
        self.state = 'MA'
        self.rotate = 30
        self.owner_pw = 'foo'
        self.user_pw = 'baz'

    def test_watermark(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk)

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_underneath(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=True, suffix='watermarked_underneath')

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_overlay(self):
        for pdf in self.pdfs:
            wtrmrk = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, rotate=self.rotate)
            added = self.w.add(pdf, wtrmrk, underneath=False, suffix='watermarked_overlay')

            self.assertTrue(os.path.exists(wtrmrk))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_flat(self):
        for pdf in self.pdfs:
            flat = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=True)
            added = self.w.add(pdf, flat, suffix='watermarked_flat')

            self.assertTrue(os.path.exists(flat))
            self.assertTrue(os.path.exists(added))
            self.assertTrue(Info(added).resources())

    def test_watermark_layered(self):
        for pdf in self.pdfs:
            layered = self.w.draw(self.address, str(self.town + ', ' + self.state), opacity=0.08, flatten=False)
            added = self.w.add(pdf, layered, suffix='watermarked_layered')

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
            l = Label(pdf, label).write()

            self.assertTrue(os.path.exists(l))
            self.assertTrue(Info(l).resources())


if __name__ == '__main__':
    unittest.main()
