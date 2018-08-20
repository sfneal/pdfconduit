import unittest
import os
from pdfconduit import Info, Merge
from tests import directory


class TestMerge(unittest.TestCase):
    def test_merge(self):
        pdfs = [os.path.join(directory, p) for p in ['article.pdf', 'charts.pdf', 'document.pdf', 'manual.pdf']]
        m = Merge(pdfs)

        self.assertTrue(os.path.exists(m.file))
        self.assertEqual(sum([Info(pdf).pages for pdf in pdfs]), Info(m.file).pages)


if __name__ == '__main__':
    unittest.main()
