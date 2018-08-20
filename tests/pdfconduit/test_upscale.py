import unittest
import os
from pdfconduit import Info, upscale
from tests import pdf


class TestUpscale(unittest.TestCase):
    def test_upscale(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s)

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_20x(self):
        s = 2.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_2.0')

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_15x(self):
        s = 1.5
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_1.5')

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))

    def test_upscale_30x(self):
        s = 3.0
        upscale1 = upscale(pdf, scale=s, suffix='upscaled_3.0')

        self.assertTrue(os.path.isfile(upscale1))
        self.assertEqual(Info(upscale1).size, tuple([i * s for i in Info(pdf).size]))


if __name__ == '__main__':
    unittest.main()
