__author__ = 'imalkov'


from pecutils import prepare_to_parse


class TopoParse:
    def __init__(self):
        self._TP_FILE_LINE_NUM = 11

    def __call__(self, str_file):
        str_file = prepare_to_parse(str_file)
        if self._is_valid_line_num(str_file) is False:
            return None
        pivot = 9 + int(str_file[6])
        ll = self._const_parse(str_file[:pivot]) + self._dyn_parse(str_file[pivot:])
        ll = [el if isinstance(el, str) else ",".join(el) for el in ll]
        return ",".join(ll)

    def _is_valid_line_num(self, str_file):

        if len(str_file) <= (self._TP_FILE_LINE_NUM + 1):
            print  "FALSE :", str_file
            return False
        if str.isdigit(str_file[6]) is False:
            print "FALSE :", str_file
            return False
        return (len(str_file) - (int(str_file[6]) + 1)) == self._TP_FILE_LINE_NUM

    def _tp_arange(self, ll):
        ll = [a[0] if len(a) == 1 else a for a in ll]
        return map(lambda l: l.strip() if isinstance(l, str) else map(str.strip, l), ll)


    def _dyn_parse(self, ll):
        if (ll[0].find(' ')) != -1:
            ll[0] = ll[0].replace(' ', ',')
        return self._tp_arange([a.split(',') for a in ll])


    def _const_parse(self, ll):
        return self._tp_arange([a.split(' ') for a in ll])

topo_parser = TopoParse()