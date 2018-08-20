import unittest
import os
import shutil
from pdfconduit import Info, upscale
from tests import pdf, directory


class TestUpscale(unittest.TestCase):
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

    def test_upscale(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s)
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_20x(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_2.0')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_15x(self):
        s = 1.5
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_1.5')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_30x(self):
        s = 3.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_3.0')
        self.files.append(upscale1)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))


if __name__ == '__main__':
    unittest.main()
