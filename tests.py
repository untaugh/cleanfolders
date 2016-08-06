#!/usr/bin/python3

import unittest
from cleanfolders import cleanfolders
import os

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.cf = cleanfolders()

    def test_argparse(self):
        self.assertTrue(1)

    def test_parse_empty_file(self):
        ret = self.cf.parse_file([''])
        self.assertEqual(ret['keep'],[])
        self.assertEqual(ret['clean'],[])

    def test_parse_simple_file(self):
        ret = self.cf.parse_file(['clean:', 'Desktop', 'keep:', 'Music', 'clean:','Downloads'])
        self.assertEqual(ret['keep'],['Music'])
        self.assertEqual(ret['clean'],['Desktop','Downloads'])

    def test_check_file_dict(self):
        home = os.environ['HOME']
        testdir = home + '/CFTEST1'
        try:
            os.mkdir(testdir)
        except:
            pass
        dirs1 = {'clean':['CFTEST1']}
        dirs2 = {'clean':['CFTEST2'],'keep':['CFTEST3']}
        ret1 = self.cf.check_dirs(dirs1)
        ret2 = self.cf.check_dirs(dirs2)
        self.assertEqual({'clean':['CFTEST1']},ret1)
        self.assertEqual({'clean':[],'keep':[]},ret2)
        os.rmdir(testdir)

    def test_trash_dir(self):
        savetrashdir = self.cf.trashdir
        self.cf.trashdir = '/tmp/testtrash'
        try:
            os.rmdir(self.cf.trashdir)
        except:
            pass
        self.assertFalse(os.path.exists(self.cf.trashdir))
        self.cf.check_trash()
        self.assertTrue(os.path.exists(self.cf.trashdir))
        try:
            os.rmdir(self.cf.trashdir)
        except:
            pass
        self.cf.trashdir = savetrashdir

    def test_clean_dirs(self):
        home = os.environ['HOME']
        testdir = home + '/CFTEST1'
        try:
            os.rmdir(self.cf.trashdir + '/CFTEST1')
        except:
            pass
        try:
            os.mkdir(testdir)
        except:
            pass
        dirs1 = {'clean':['CFTEST1']}
        self.assertTrue(os.path.exists(testdir))
        self.cf.clean_dirs(dirs1)
        self.assertFalse(os.path.exists(testdir))
        self.assertTrue(os.path.exists(self.cf.trashdir + '/CFTEST1'))
        try:
            os.rmdir(testdir)
        except:
            pass
        try:
            os.rmdir(self.cf.trashdir + '/CFTEST1')
        except:
            pass

if __name__ == '__main__':
    unittest.main()
