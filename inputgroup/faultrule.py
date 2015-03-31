__author__ = 'imalkov'

from pecutils import prepare_to_parse

class FaultParser():
    def __call__(self, arr_location):
        return ','.join([','.join(el.split(' ')) for el in prepare_to_parse(arr_location)])

fault_parser = FaultParser()