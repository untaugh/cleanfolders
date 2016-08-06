#!/usr/bin/python3

import argparse
import os, shutil
from pathlib import Path

class cleanfolders:
    trashdir = os.environ['HOME'] + '/TRASH'
    basedir = os.environ['HOME']

    parser = argparse.ArgumentParser(description='clean some folders')
    parser.add_argument('-f', default='settings', type=argparse.FileType('r'))
    args = parser.parse_args()
    settingsfile = args.f

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
        if not 'keep' in dirs:
            dirs['keep'] = []
        if not 'keep' in dirs:
            dirs['clean'] = []

        # always keep trash
        dirs['keep'].append(Path(self.trashdir).parts[-1])

        # loop remove not wanted dirs
        for d in Path(self.basedir).iterdir():
            dirname = d.parts[-1]
            if not dirname in dirs['keep'] and dirname[0] != '.':
                if os.path.exists(self.trashdir + '/' + dirname):
                    number = 0
                    while os.path.exists(self.trashdir + '/' + dirname + '_' + str(number)):
                        number = number + 1
                    dirname = dirname + '_' + str(number)
                shutil.move(d.as_posix(), self.trashdir + '/' + dirname)
            if dirname in dirs['clean']:
                d.mkdir()

    def list_remove(self,dirs):
        list = []
        for dir in Path(self.basedir).iterdir():
            dirname = dir.parts[-1]
            if not dirname in dirs['keep'] + dirs['clean'] and dirname[0] != '.':
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

def main():
    cf = cleanfolders()
    dirs = cf.parse_file(cf.settingsfile.readlines())
    rlist = cf.list_remove(dirs)
    clist = cf.list_clean(dirs)
    print("Remove files:")
    for dir in rlist:
        print(dir.as_posix())
    print("Clean folders:")
    for dir in clist:
        print(dir.as_posix())

if __name__ == '__main__':
    main()
