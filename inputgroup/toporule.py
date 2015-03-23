__author__ = 'imalkov'

def is_valid_line_num(strfile):
    TOPO_LINE_NUM = 11
    if len(strfile) <= (TOPO_LINE_NUM + 1):
        print  "FALSE :", strfile
        return False

    if str.isdigit(strfile[6]) is False:
        print  "FALSE :", strfile
        return False

    return (len(strfile) - (int(strfile[6]) + 1)) == TOPO_LINE_NUM

def topo_arange(ll):
    ll = [a[0] if len(a) == 1 else a for a in ll]
    return map(lambda l: l.strip() if isinstance(l, str) else map(str.strip, l), ll)

def dynparse(ll):
    if (ll[0].find(' ')) != -1:
        ll[0] = ll[0].replace(' ', ',')

    return topo_arange([a.split(',') for a in ll])

def constparse(ll):
    return topo_arange([a.split(' ') for a in ll])

def topo_parse(strfile):
    if is_valid_line_num(strfile) is False:
        return None
    pivot  = 9 + int(strfile[6])
    ll =  constparse(strfile[:pivot]) + dynparse(strfile[pivot:])
    ll = [el if isinstance(el, str) else ",".join(el) for el in ll]
    return ",".join(ll)

