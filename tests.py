#!/usr/bin/python3

import unittest
from cleanfolders import cleanfolders
import os
from pathlib import Path
import shutil

class TestFunctions(unittest.TestCase):

    def removedir(self,dir):
        try:
            os.rmdir(dir)
        except:
            pass

    def makedir(self,dir):
        try:
            os.mkdir(dir)
        except:
            pass

    def setUp(self):
        self.cf = cleanfolders()
        # create directory structure for testing
        testdir = '/tmp/cftesting'
        trashdir = testdir + '/TRASH'
        self.makedir(testdir)
        self.makedir(trashdir)
        dirs = ['Test1', 'Test2','Test3']
        files = ['file1.txt','file2.png','file3.dat']
        for d in dirs:
            self.makedir(testdir + '/' + d)
            for f in files:
                p = Path(testdir + '/' + d + '/' + f)
                p.touch()
        # set directories in cleanfolders
        self.cf.basedir = testdir
        self.cf.trashdir = trashdir

    def tearDown(self):
        testdir = '/tmp/cftesting'
        shutil.rmtree(testdir)

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
        ret = self.cf.parse_file(['clean:\r\n', ' Cat\n', 'keep:', '\tDog \r', 'clean:\n\r','  Cow \t'])
        self.assertEqual(ret['keep'],['Dog'])
        self.assertEqual(ret['clean'],['Cat','Cow'])

    def test_check_file_dict(self):
        home = self.cf.basedir
        testdir = home + '/CFTEST1'
        self.makedir(testdir)
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
        self.removedir(self.cf.trashdir)
        self.assertFalse(os.path.exists(self.cf.trashdir))
        self.cf.check_trash()
        self.assertTrue(os.path.exists(self.cf.trashdir))
        self.removedir(self.cf.trashdir)
        self.cf.trashdir = savetrashdir

    def test_keep_dirs(self):
        settings = 'keep:\nTest2\nTest3'
        ret = self.cf.parse_file(settings.splitlines())
        self.cf.process_dirs(ret)
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test1'))
        self.assertTrue(os.path.exists(self.cf.trashdir + '/Test1'))
        self.assertTrue(os.path.exists(self.cf.basedir + '/Test2'))
        self.assertTrue(os.path.exists(self.cf.basedir + '/Test3'))

    def test_keep_none(self):
        settings = ''
        ret = self.cf.parse_file(settings.splitlines())
        self.cf.process_dirs(ret)
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test1'))
        self.assertTrue(os.path.exists(self.cf.trashdir + '/Test1'))
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test2'))
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test3'))

    def test_clean_dirs(self):
        settings = 'clean:\nTest1'
        ret = self.cf.parse_file(settings.splitlines())
        self.cf.process_dirs(ret)
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test2'))
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test3'))
        c = 0
        for i in Path(self.cf.basedir + '/Test1').iterdir(): c = c + 1
        self.assertEqual(0,c)

    def test_clean_and_keep(self):
        settings = 'clean:\nTest2\nkeep:\nTest1'
        ret = self.cf.parse_file(settings.splitlines())
        self.cf.process_dirs(ret)
        self.assertFalse(os.path.exists(self.cf.basedir + '/Test3'))
        self.assertTrue(os.path.exists(self.cf.trashdir + '/Test3'))
        self.assertTrue(os.path.exists(self.cf.basedir + '/Test1'))
        self.assertTrue(os.path.exists(self.cf.basedir + '/Test2'))
        c = 0
        for i in Path(self.cf.basedir + '/Test2').iterdir(): c = c + 1
        self.assertEqual(0,c)

    def test_move_duplicate(self):
        os.mkdir(self.cf.trashdir + '/Test3')
        os.mkdir(self.cf.trashdir + '/Test2')
        os.mkdir(self.cf.trashdir + '/Test2_0')
        settings = 'keep:\nTest1'
        ret = self.cf.parse_file(settings.splitlines())
        self.cf.process_dirs(ret)
        self.assertTrue(os.path.exists(self.cf.trashdir + '/Test3'))
        self.assertTrue(os.path.exists(self.cf.trashdir + '/Test3_0'))
        self.assertTrue(os.path.exists(self.cf.trashdir + '/Test2_1'))

    def test_hidden_files(self):
        os.mkdir(self.cf.basedir + '/.hidden')
        self.assertTrue(os.path.exists(self.cf.basedir + '/.hidden'))
        settings = 'keep:\nTest1'
        ret = self.cf.parse_file(settings.splitlines())
        self.cf.process_dirs(ret)
        self.assertTrue(os.path.exists(self.cf.basedir + '/.hidden'))

    def test_list_remove(self):
        settings = ''
        ret = self.cf.parse_file(settings.splitlines())
        list = self.cf.list_remove(ret)
        self.assertTrue(Path(self.cf.basedir + '/Test2') in list)
        self.assertTrue(Path(self.cf.basedir + '/Test3') in list)
        self.assertTrue(Path(self.cf.basedir + '/Test1') in list)
        settings = 'keep:\nTest1\nTest2'
        ret = self.cf.parse_file(settings.splitlines())
        list = self.cf.list_remove(ret)
        self.assertFalse(Path(self.cf.basedir + '/Test2') in list)
        self.assertTrue(Path(self.cf.basedir + '/Test3') in list)
        self.assertFalse(Path(self.cf.basedir + '/Test1') in list)
        settings = 'keep:\nTest1\nclean:\nTest3'
        ret = self.cf.parse_file(settings.splitlines())
        list = self.cf.list_remove(ret)
        self.assertTrue(Path(self.cf.basedir + '/Test2') in list)
        self.assertFalse(Path(self.cf.basedir + '/Test3') in list)
        self.assertFalse(Path(self.cf.basedir + '/Test1') in list)

    def test_list_clean(self):
        settings = 'clean:\nTest3\nTest2'
        ret = self.cf.parse_file(settings.splitlines())
        list = self.cf.list_clean(ret)
        self.assertTrue(Path(self.cf.basedir + '/Test2') in list)
        self.assertTrue(Path(self.cf.basedir + '/Test3') in list)
        self.assertFalse(Path(self.cf.basedir + '/Test1') in list)
        settings = 'clean:\nTest1\nkeep:\nTest2'
        ret = self.cf.parse_file(settings.splitlines())
        list = self.cf.list_clean(ret)
        self.assertFalse(Path(self.cf.basedir + '/Test2') in list)
        self.assertFalse(Path(self.cf.basedir + '/Test3') in list)
        self.assertTrue(Path(self.cf.basedir + '/Test1') in list)


if __name__ == '__main__':
    unittest.main()
