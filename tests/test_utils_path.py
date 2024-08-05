import os.path
import unittest

from pdfconduit.utils import add_suffix
from tests import *


class TestPath(unittest.TestCase):

    def test_add_suffix(self):
        file_path = test_data_path("article.pdf")
        with_suffix = add_suffix(file_path)

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(
            with_suffix,
            os.path.join(os.path.dirname(file_path), "article_modified.pdf"),
        )

    def test_add_suffix_suffix(self):
        file_path = test_data_path("article.pdf")
        with_suffix = add_suffix(file_path, "new")

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(
            with_suffix, os.path.join(os.path.dirname(file_path), "article_new.pdf")
        )

    def test_add_suffix_suffix_sep(self):
        file_path = test_data_path("article.pdf")
        with_suffix = add_suffix(file_path, "old", "-")

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(
            with_suffix, os.path.join(os.path.dirname(file_path), "article-old.pdf")
        )

    def test_add_suffix_suffix_sep_ext(self):
        file_path = test_data_path("article.pdf")
        with_suffix = add_suffix(file_path, "backup", "-", "zip")

        self.assertIsInstance(with_suffix, str)
        self.assertEqual(
            with_suffix, os.path.join(os.path.dirname(file_path), "article-backup.zip")
        )


if __name__ == "__main__":
    unittest.main()
