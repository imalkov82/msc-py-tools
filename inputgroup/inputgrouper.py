__author__ = 'imalkov'

import os
import subprocess
from argparse import ArgumentParser
from parser import gen_parse


def collect_tffs(top, name):
    arr = []
    for dirpath, dirname, filename in os.walk(top):
        if name in filename:
            arr.append(os.path.join(dirpath, name))
    return arr

def create_dirs(merged, dirpath, outpath):
    i = 0
    lotlen = len(merged)
    dtnow = 0.0
    print("LET START!\n\n ------------------ \n\n")
    for key, group in merged.items():
        i += 1
        print "{0}% - DONE:".format(int((dtnow/lotlen) * 100))
        dpath = os.path.join(outpath, "TOPO_TYPE{0}".format(i))
        os.mkdir(dpath)
        for item in group:
            locdir , inpt = os.path.split(os.path.split(item)[0])
            dtnow +=1
            if inpt.find('input') != -1:
                rpwkrdir = item.replace('/home/imalkov/Documents/_University/M.s/Research/BigData/','')
                rpwkrdir = os.path.split(os.path.split(rpwkrdir)[0])[0]
                rpwkrdir = os.path.join(dpath,rpwkrdir.replace('/','_'))
                subprocess.call(["ln", "-s", locdir, os.path.join(dpath, rpwkrdir)])
                # print locdir, '->', os.path.join(dpath,rpwkrdir)
            else:
                print 'BAD DIR:', item
    print("\n\n     YES - DONE 100% !!!")

def main():
        # dirpath = '/home/imalkov/Documents/_University/M.s/Research/BigData/data'+ str(datnum)+'/'
        # outpath = '/home/imalkov/Dropbox/M.s/Research/DATA/RiP_LookBack/BDiSTRIP2/MAPEDiDATA/'
        dirpath = '/home/imalkov/Documents/_University/M.s/Research/BigData/'
        if not os.path.isdir(dirpath):
            print("missing {0}".format(dirpath))

        topo_fls = collect_tffs(dirpath, 'topo_parameters.txt')
        topo_fls = map(lambda mpath: (gen_parse(mpath), mpath), topo_fls)

        topo_fls = filter(lambda (el, path):  el is not None and el is not '', topo_fls)
        topo_info = filter(lambda (el, path):  el[6:9] in ['Nil' ,'tf,'], topo_fls)

        mydict = {}

        for el, path in topo_info:
            arr = []
            if el in mydict:
                arr = mydict[el]
            arr.append(path)
            mydict[el] = arr

        create_dirs(merged = mydict, dirpath = dirpath, outpath = '/home/imalkov/Documents/COMBINE_DOC_GDRIVE_DBOX/BDTOPO/')

if __name__ == "__main__":
    main()
