'''
Created on Apr 10, 2012

@organization: cert.org
'''
import unittest
import certfuzz.testcase.testcase_base
import tempfile
import shutil
from certfuzz.testcase.errors import TestCaseError
import logging
from test_certfuzz.mocks import MockSeedfile, MockFuzzedFile, MockLogger
import os


class Test(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='bff-test-')
        self.sf = MockSeedfile()
        self.ff = MockFuzzedFile()
        cfg = {}
        program = 'foo'
        cmd_template = 'foo a b c'
        workdir_base = os.path.join(self.tmpdir, 'workdir_base')
        cmdlist = cmd_template.split()

        self.tc = certfuzz.testcase.testcase_base.TestCaseBase(cfg,
                                                               self.sf,
                                                               self.ff,
                                                               program,
                                                               cmd_template,
                                                               workdir_base,
                                                               cmdlist,)
        pass

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_init(self):
        self.assertEqual(self.sf, self.tc.seedfile)
        self.assertEqual(self.ff, self.tc.fuzzedfile)
        self.assertTrue(self.tc.is_heisenbug)
        self.assertFalse(self.tc.is_zipfile)
        self.assertFalse(self.tc.is_crash)
        self.assertFalse(self.tc.is_unique)
        self.assertFalse(self.tc.should_proceed_with_analysis)
        self.assertFalse(self.tc.is_corrupt_stack)
        self.assertTrue(self.tc.copy_fuzzedfile)
        self.assertFalse(self.tc.debugger_missed_stack_corruption)
        self.assertFalse(self.tc.total_stack_corruption)
        self.assertFalse(self.tc.pc_in_function)

    def test_calculate_hamming_distances(self):
        tc = self.tc

        tc.logger = MockLogger()

        fd, tc.seedfile.path = tempfile.mkstemp(suffix='.seed',
                                                prefix='bff-test-',
                                                dir=self.tmpdir)
        os.write(fd, 'abcdefghijklmnopqrstuvwxyz\n')
        os.close(fd)

        fd, tc.fuzzedfile.path = tempfile.mkstemp(suffix='.fuzzed',
                                                  prefix='bff-test-',
                                                  dir=self.tmpdir)
        os.write(fd, 'ABCDefghijklmnopqrstuvwxyz\n')
        os.close(fd)

        self.assertEqual(None, tc.hd_bits)
        self.assertEqual(None, tc.hd_bytes)
        tc.calculate_hamming_distances()
        self.assertEqual(4, tc.hd_bits)
        self.assertEqual(4, tc.hd_bytes)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
