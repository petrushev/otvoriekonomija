# -*- coding: utf-8 -*-

import os
from statcrawl import conf, parser
from operator import itemgetter

ENC = 'cp1251' # encoding of text in datafiles
VAL_KEYS = parser.VAL_KEYS

TOP_DIMS = {u"година": 'godina',
            u"регион": 'region',
            u"варијабли": 'vars',
            u"општина": 'opstina',
            u"земја": 'zemja',
            u"тарифа": 'tarifa',
            u"пол": 'pol',
            u"мерка": 'merka',
            u"сектор на дејност": 'sektor',
            u"индикатор": 'indikator',
            u"месец": 'mesec',
            u"возраст": 'vozrast',
            u"стапка": 'stapka'}



def traverse_files():
    """Iterator with all filenames with stats"""
    for filename in os.listdir(conf.datapath):
        if filename.endswith('.px'):
            yield conf.datapath + '/' + filename


def compile_all_dimensions():
    """Get all dimensions in all stats, along with all their possible values"""
    all_dims = {}
    for file_ in traverse_files():
        parsed = parser.parse(open(file_).read().decode(ENC), skip_data=True)
        if 'outter_dim_key' not in parsed: continue
        for dim, vals in parser.iter_dims(parsed):
            try:
                all_dims[dim].update(set(vals))
            except KeyError:
                all_dims[dim] = set(vals)

    return all_dims

def filter_by_dims(dimensions):
    """Iterate through files and skip any that has dimensions not included in `dimensions`,
       yields content"""
    for file_ in traverse_files():
        content = open(file_).read().decode(ENC)
        parsed = parser.parse(content, skip_data=True)

        # skip flat file
        if 'outter_dim_values' not in parsed: continue

        dims = set(dim for dim, _ in parser.iter_dims(parsed))
        if len(dims) > len(dims.intersection(dimensions)):
            # it has some dimensions not specified in arg, skip it
            continue

        yield content



if __name__ == '__main__':
    main()


