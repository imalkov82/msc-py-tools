__author__ = 'imalkov'

TP_FILE_LINE_NUM = 11


def is_valid_line_num(str_file):
    global TP_FILE_LINE_NUM

    if len(str_file) <= (TP_FILE_LINE_NUM + 1):
        print  "FALSE :", str_file
        return False
    if str.isdigit(str_file[6]) is False:
        print "FALSE :", str_file
        return False
    return (len(str_file) - (int(str_file[6]) + 1)) == TP_FILE_LINE_NUM


def tp_arange(ll):
    ll = [a[0] if len(a) == 1 else a for a in ll]
    return map(lambda l: l.strip() if isinstance(l, str) else map(str.strip, l), ll)


def dyn_parse(ll):
    if (ll[0].find(' ')) != -1:
        ll[0] = ll[0].replace(' ', ',')
    return tp_arange([a.split(',') for a in ll])


def const_parse(ll):
    return tp_arange([a.split(' ') for a in ll])


def tp_parse(str_file):
    if is_valid_line_num(str_file) is False:
        return None
    pivot = 9 + int(str_file[6])
    ll = const_parse(str_file[:pivot]) + dyn_parse(str_file[pivot:])
    ll = [el if isinstance(el, str) else ",".join(el) for el in ll]
    return ",".join(ll)

