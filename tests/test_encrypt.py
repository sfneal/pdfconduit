import unittest
import os
import shutil
import time
from pdfconduit import Encrypt, Info
from tests import *


class TestEncrypt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'encrypt')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        # Log destination
        cls.file_path = 'encrypt.csv'
        cls.csv = os.path.join(os.path.dirname(__file__), 'log', cls.file_path)
        cls.log = []

        cls.files = []

    @classmethod
    def tearDownClass(cls):
        # Move /P value files into results/P
        if not os.path.isdir(os.path.join(cls.dst, 'P')):
            os.mkdir(os.path.join(cls.dst, 'P'))
        for f in os.listdir(cls.dst):
            if f.startswith('-'):
                source = os.path.join(cls.dst, f)
                target = os.path.join(cls.dst, 'P', f)
                shutil.move(source, target)

        write_log(cls.csv, cls.log)

    def setUp(self):
        self.owner_pw = 'foo'
        self.user_pw = 'baz'
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[2:]), t))

        # Determine test result
        if hasattr(self, '_outcome'):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
            result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        ok = not error and not failure

        # demo:   report short info immediately (not important)
        if not ok:
            typ, text = ('ERROR', error) if error else ('FAIL', failure)
        else:
            typ = 'PASS'

        # Log dump
        rows, file_path = dump_log(test_case=self.id().split('.'), time=t, result=typ)
        self.log.append(rows)
        self.file_path = file_path

        # Move each file into results folder
        for i in self.files:
            source = os.path.join(directory, str(os.path.basename(i)))
            target = os.path.join(self.dst, str(os.path.basename(i)))
            try:
                shutil.move(source, target)
                self.files.remove(i)
            except FileNotFoundError:
                pass

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def test_encrypt_printing(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, suffix='secured')
        self.files.append(str(p))
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)
        self.assertEqual(security['/P'], -1852)

    def test_encrypt_128bit(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, bit128=True, suffix='secured_128bit')
        self.files.append(str(p))
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/Length'], 128)

    def test_encrypt_40bit(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, bit128=False, suffix='secured_40bit')
        self.files.append(str(p))

        self.assertTrue(Info(p.output, self.user_pw).encrypted)

    def test_encrypt_commenting(self):
        p = Encrypt(pdf, self.user_pw, self.owner_pw, allow_commenting=True, suffix='secured_commenting')
        self.files.append(str(p))
        security = Info(p.output, self.user_pw).security

        self.assertTrue(Info(p.output, self.user_pw).encrypted)
        self.assertEqual(security['/P'], -1500)


if __name__ == '__main__':
    unittest.main()
