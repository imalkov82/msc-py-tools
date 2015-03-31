__author__ = 'imalkov'

import os
from os.path import split
import subprocess
from argparse import ArgumentParser
from toporule import topo_parser
from faultrule import fault_parser
from random import randint

def collect_tffs(top, name):
    arr = []
    for dirpath, dirname, filename in os.walk(top, followlinks=True):
        if name in filename:
            arr.append(os.path.join(dirpath, name))
    return arr


def collect_to_dict(tup_arr):
    loc_dict = {}
    for el, path in tup_arr:
        arr = []
        if el in loc_dict:
            arr = loc_dict[el]
        arr.append(path)
        loc_dict[el] = arr
    return loc_dict

class ProgressObserver:
    def __init__(self, dir_creator):
        self.dir_creator = dir_creator

    def __call__(self):
        if self.dir_creator.dtnow != self.dir_creator.lotlen:
            print "{0}% - DONE:".format(int((self.dir_creator.dtnow/self.dir_creator.lotlen) * 100))
        else:
            print("\n\n     YES - DONE 100% !!!")

class DirCreator:
    def __init__(self):
        self.observers = []
        self.dtnow = 0.0
        self.lotlen = 0

    def attach(self, observer):
        self.observers.append(observer)


    def _update_observers(self):
        for observer in self.observers:
            observer()

    def __call__(self, merged, out_path, fldr_name):
        self.dtnow = 0.0
        self.lotlen = reduce(lambda a,b: a+b, [len(i) for i in merged.values()])
        i = 0
        for key, group in merged.items():
            i += 1
            self._update_observers()
            dpath = os.path.join(out_path, "{0}_TYPE{1}".format(fldr_name, i))
            os.mkdir(dpath)
            for loc_dir, name in group:
                self.dtnow +=1
                subprocess.call(["ln", "-s", loc_dir, os.path.join(dpath, name)])
        self._update_observers()

def name_rule_factory(prefix_rule):
    def name_rule(group):
        grp_split = [split(split(item)[0])[0] for item in group]
        return [(item, (item.replace(prefix_rule, '')).replace('/','_')) for item in grp_split]
    return name_rule

def item_rm_rule(group):
    f = filter(lambda (item, input): input.find('input') != -1, [(item, split(split(item)[0])[1]) for item in group])
    return [item for item, dump in f]

class GroupByTemplate:
    def __init__(self, filter_rule, schema_rule):
        self.filter_rule = filter_rule
        self.schema_rule = schema_rule

    def __call__(self, merged):
        flt_mrg = {k: self.filter_rule(g) for k, g in merged.items()}
        return {k: self.schema_rule(g) for k, g in flt_mrg.items()}

def main():
    parser = ArgumentParser()
    #set rules
    parser.add_argument( "-f", action="store_true", dest="fault_act", help="group by fault_parameters.txt", default=False)
    parser.add_argument( "-t", action="store_true", dest="topo_act", help="group by topo_parameters.txt", default=False)
    parser.add_argument( "-d", action="store", dest="dirpath", help="directory full path")
    parser.add_argument( "-o", dest="outpath", help="output directory full path", default=os.getenv("HOME"))
    parser.add_argument( "-rp", dest="topo_pref_rule", help="topography prefix remove rule", default=os.getenv("HOME"))
    parser.add_argument("-p", action="store_true", dest="groups_print", help="print the groupby instead dir creation", default=False)
    #get arguments
    kvargs = parser.parse_args()

    if kvargs.dirpath is None:
        raise ValueError("no search directory specified")
    else:
        dirpath = kvargs.dirpath

    if not os.path.isdir(dirpath):
        raise IOError("missing {0}".format(dirpath))

    if kvargs.topo_act is True:
        print  "handle topo parameter input"
        topo_outpath = os.path.join(kvargs.outpath, "TOPO_{0}".format(os.getppid()))

        if not os.path.isdir(topo_outpath):
            os.mkdir(topo_outpath)

        topo_fls = collect_tffs(dirpath, 'topo_parameters.txt')
        topo_fls = map(lambda mpath: (topo_parser(mpath), mpath), topo_fls)

        topo_fls = filter(lambda (el, path):  el is not None and el is not '', topo_fls)
        topo_info = filter(lambda (el, path):  el[6:9] in ['Nil' ,'tf,'], topo_fls)

        td = collect_to_dict(topo_info)
        template = GroupByTemplate(item_rm_rule, name_rule_factory(prefix_rule=kvargs.topo_pref_rule))
        td = template(td)

        if kvargs.groups_print is False:
            dir_creator = DirCreator()
            dir_creator.attach(ProgressObserver(dir_creator))
            dir_creator(td, topo_outpath, 'TOPO')
        else:
            for k, g in td.items():
                print k, ' ', [i for (i,j) in g]

    if kvargs.fault_act is True:
        print  "fault_act"

        fault_outpath = kvargs.outpath
        # fault_outpath = os.path.join(kvargs.outpath, "FAULT_{0}_{1}".format(os.getppid(),randint(0,os.getppid())))

        if not os.path.isdir(fault_outpath):
            os.mkdir(fault_outpath)

        fault_fls = collect_tffs(dirpath, 'fault_parameters.txt')
        fault_fls = map(lambda mpath: (fault_parser(mpath), mpath), fault_fls)

        fd = collect_to_dict(fault_fls)

        template = GroupByTemplate(lambda x: x, name_rule_factory(prefix_rule=kvargs.outpath))

        dir_creator = DirCreator()
        dir_creator.attach(ProgressObserver(dir_creator))

        dir_creator(template(fd), fault_outpath, 'FAULT')

if __name__ == "__main__":
    main()