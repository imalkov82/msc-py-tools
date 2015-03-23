__author__ = 'imalkov'


from toporule import topo_parse

def gen_parse(path):
    res = []
    with open(path) as file:
        lines = file.readlines()
        #remove empty lines and full file comments
        res = map(lambda line: (line.lstrip())[:-1] ,lines)
        res = filter(lambda line: False if (len(line) == 0 or line[0] in ['$', '\n']) else True, res)
        res = map(lambda line: line.split('$')[0].strip(), res)
    # return res
    return topo_parse(res)