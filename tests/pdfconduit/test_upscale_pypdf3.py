import unittest
import os
import shutil
import time
from pdfconduit import Info, upscale
from tests import pdf, directory


class TestUpscalePyPDF3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = []

    @classmethod
    def tearDownClass(cls):
        # Destination directory
        dst = os.path.join(directory, 'results', 'scale')

        # Create destination if it does not exist
        if not os.path.isdir(dst):
            os.mkdir(dst)

        # Move each file into results folder
        for i in cls.files:
            source = i
            target = os.path.join(dst, str(os.path.basename(i)))
            shutil.move(source, target)

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[2:]), t))

    def test_upscale_pypdf3(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_pypdf3', method='pypdf3')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_pdfrw(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_20x_pypdf3(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_2.0_pypdf3', method='pypdf3')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_20x_pdfrw(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_2.0_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_15x_pypdf3(self):
        s = 1.5
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_1.5_pypdf3', method='pypdf3')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_15x_pdfrw(self):
        s = 1.5
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_1.5_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_30x_pypdf3(self):
        s = 3.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_3.0_pypdf3', method='pypdf3')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_30x_pdfrw(self):
        s = 3.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_3.0_pdfrw', method='pdfrw')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))


if __name__ == '__main__':
    unittest.main()
