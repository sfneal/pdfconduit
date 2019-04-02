import os
import unittest
from tempfile import TemporaryDirectory

from looptools import Timer

from pdf.conduit.lib import IMAGE_DEFAULT, IMAGE_DIRECTORY
from pdf.modify.draw.image import DrawPIL, img_adjust
from tests import *


class TestModifyDrawImage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.img_path = img_path
        cls.wtrmrk_path = os.path.join(IMAGE_DIRECTORY, IMAGE_DEFAULT)
        cls.pdf = None

    def setUp(self):
        self.temp = TemporaryDirectory()

    def tearDown(self):
        self.temp.cleanup()

    @Timer.decorator
    def test_draw_text(self):
        """Draw text onto an image."""
        draw = DrawPIL(tempdir=self.temp.name)
        draw.draw_text('Here is the first text', y=10, opacity=50)
        draw.draw_text('Here is the second text', y=50, opacity=50)
        d = draw.save(destination=test_data_dir, file_name='draw_text')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_draw_img(self):
        """Draw text onto an image."""
        draw = DrawPIL(tempdir=self.temp.name)
        draw.draw_img(self.img_path)
        draw.draw_img(self.wtrmrk_path, opacity=0.08, rotate=30)
        d = draw.save(destination=test_data_dir, file_name='draw_img')

        # Assert file exists
        self.assertTrue(os.path.exists(d))
        return d

    @Timer.decorator
    def test_image_rotate(self):
        """Test the function 'img_rotate.'"""
        rotated = img_adjust(self.wtrmrk_path, rotate=30, fit=1)

        # Assert file exists
        self.assertTrue(os.path.exists(rotated))
        return rotated


if __name__ == '__main__':
    unittest.main()
