#!/usr/bin/python3

import argparse
import os, shutil
from pathlib import Path

class cleanfolders:
    trashdir = os.environ['HOME'] + '/TRASH'
    basedir = os.environ['HOME']
    runclean = False

    parser = argparse.ArgumentParser(description='clean some folders')
    parser.add_argument('-f', default='settings', type=argparse.FileType('r'))
    parser.add_argument('-r', action='store_true')
    args = parser.parse_args()
    settingsfile = args.f
    if args.r:
        runclean = True

    def parse_file(self,lines):
        dict = {'keep':[], 'clean':[]}
        mode = 'keep'
        for l in lines:
            l = l.strip()
            if l == 'keep:':
                mode = 'keep'
            elif l == 'clean:':
                mode = 'clean'
            elif len(l):
                    dict[mode].append(l)
        return dict

    def check_dirs(self,dirs):
        if 'clean' in dirs:
            for d in dirs['clean']:
                if not os.path.exists(self.basedir + '/' + d):
                    dirs['clean'].remove(d)
        if 'keep' in dirs:
            for d in dirs['keep']:
                if not os.path.exists(self.basedir + '/' + d):
                    dirs['keep'].remove(d)
        return dirs

    def clean_dirs(self,dirs):
        if 'clean' in dirs:
            for d in dirs['clean']:
                shutil.move(self.basedir + '/' + d, self.trashdir + '/' + d)

    def process_dirs(self,dirs):
        # add missing lists
        #if not 'keep' in dirs:
        #    dirs['keep'] = []
        #if not 'clean' in dirs:
        #    dirs['clean'] = []

        rm_list = self.list_remove(dirs)
        cl_list = self.list_clean(dirs)
        f_list = self.list_files(dirs)

        self.trash_files(f_list)

        for d in Path(self.basedir).iterdir():
            if d in rm_list or d in cl_list:
                self.trash_dir(d.as_posix())
            if d in cl_list:
                d.mkdir()

    def list_remove(self,dirs):
        list = []

        # always keep trash
        dirs['keep'].append(Path(self.trashdir).parts[-1])

        for dir in Path(self.basedir).iterdir():
            dirname = dir.parts[-1]
            if not dirname in dirs['keep'] + dirs['clean'] and dirname[0] != '.' and dir.is_dir():
                list.append(dir)
        return list

    def list_clean(self,dirs):
        list = []
        for dir in Path(self.basedir).iterdir():
            dirname = dir.parts[-1]
            if dirname in dirs['clean']:
                list.append(dir)
        return list

    def check_trash(self):
        if not os.path.exists(self.trashdir):
            os.mkdir(self.trashdir)

    def trash_dir(self,dir):
        dirname = Path(dir).parts[-1]
        if os.path.exists(self.trashdir + '/' + dirname):
            number = 0
            while os.path.exists(self.trashdir + '/' + dirname + '_' + str(number)):
                number = number + 1
            dirname = dirname + '_' + str(number)
        shutil.move(dir, self.trashdir + '/' + dirname)

    def trash_files(self,files):
        dirname = self.trashdir + '/Base'
        if os.path.exists(dirname):
            number = 0
            while os.path.exists(self.trashdir + '/Base' + '_' + str(number)):
                number = number + 1
            dirname = dirname + '_' + str(number)
        os.mkdir(dirname)
        for f in files:
            filename = Path(f).parts[-1]
            shutil.move(f.as_posix(), dirname + '/' + filename)

    def list_files(self,dir):
        list = []
        for dir in Path(self.basedir).iterdir():
            dirname = dir.parts[-1]
            if dir.is_file() and dirname[0] != '.':
                list.append(dir)
        return list

def main():
    cf = cleanfolders()
    dirs = cf.parse_file(cf.settingsfile.readlines())
    rlist = cf.list_remove(dirs)
    clist = cf.list_clean(dirs)
    flist = cf.list_files(dirs)
    print("Remove folders:")
    for dir in rlist:
        print(dir.as_posix())
    print("Clean folders:")
    for dir in clist:
        print(dir.as_posix())
    print("Remove files:")
    for file in flist:
        print(file.as_posix())
    if cf.runclean:
        cf.process_dirs(dirs)

if __name__ == '__main__':
    main()
