#!/usr/bin/python3

import argparse
import os, shutil

class cleanfolders:

    trashdir = os.environ['HOME'] + '/TRASH'
    homedir = os.environ['HOME']

    parser = argparse.ArgumentParser(description='clean some folders')
    parser.add_argument('-f',  default='settings', type=argparse.FileType('r'))
    args = parser.parse_args()
    settingsfile = args.f
    print(args)

    def main():
        pass
        #args = parser.parse_args()
        #settingsfile = args.infile
        #print(args)
        #print('this is main')

    def parse_file(self,lines):
        dict = {'keep':[], 'clean':[]}
        mode = 'keep'
        for l in lines:
            if l == 'keep:':
                mode = 'keep'
            elif l == 'clean:':
                mode = 'clean'
            elif len(l):
                    dict[mode].append(l)
        return dict

    def check_dirs(self,dirs):
        homedir = os.environ['HOME']
        if 'clean' in dirs:
            for d in dirs['clean']:
                if not os.path.exists(homedir + '/' + d):
                    dirs['clean'].remove(d)
        if 'keep' in dirs:
            for d in dirs['keep']:
                if not os.path.exists(homedir + '/' + d):
                    dirs['keep'].remove(d)
        return dirs

    def clean_dirs(self,dirs):
        if 'clean' in dirs:
            for d in dirs['clean']:
                shutil.move(self.homedir + '/' + d, self.trashdir + '/' + d)

    def check_trash(self):
        if not os.path.exists(self.trashdir):
            os.mkdir(self.trashdir)


if __name__ == '__main__':
    cleanfolders.main()
