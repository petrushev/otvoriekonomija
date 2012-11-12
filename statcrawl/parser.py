# -*- coding: utf-8 -*-

from decimal import Decimal

ENC = 'cp1251' # encoding of text in datafiles

VAL_KEYS = ('row_dim', 'outter_dim', 'inner_dim', 'btm_dim', '4th_dim')
NULLS = set(('..', '-', '...'))


def parse(content, skip_data = False):
    entries = content.split(';')
    del content
    entries.pop()
    data = {}
    iter_val_keys = iter(VAL_KEYS)
    for entry in entries:
        val = entry.split('=')
        key = val[0]
        val = '='.join(val[1:])
        key = key.strip()

        if key == 'TITLE':
            data['stat'] = val.strip('"')

        elif key == 'SUBJECT-AREA':
            data['area'] = val.strip('"')

        elif key.startswith('VALUES'):
            val_key = next(iter_val_keys)
            key_name = key.replace("VALUES", "").strip('"()').lower().replace("  "," ")
            if key_name == u"година": key_name = u"години" 
            data[val_key + "_key"] = key_name
            data[val_key + "_values"] = [item.strip('"\n\r') for item in val.split(',')]

        elif key == 'DATA' and skip_data is False:
            values = val.strip().split('\n')
            clean = []
            for row in values:
                current = []
                for v in row.strip().split(' '):
                    v=v.strip('"')
                    if v in NULLS:
                        v = None
                    else:
                        v = Decimal(v)
                    current.append(v)
                clean.append(current)
            data['data'] = clean

    return data

def iter_data(parsed):
    if 'inner_dim_values' in parsed:
        if 'btm_dim_values' in parsed:
            if '4th_dim_values' in parsed:
                # 5D data
                for i, row_val in enumerate(parsed['row_dim_values']):
                    i_row_data = iter(parsed['data'][i])
                    for outter_val in parsed['outter_dim_values']:
                        for inner_val in parsed['inner_dim_values']:
                            for btm_val in parsed['btm_dim_values']:
                                for frth_val in parsed['4th_dim_values']:
                                    val = next(i_row_data)
                                    if val is None: continue
                                    yield row_val, outter_val, inner_val, btm_val, frth_val, val
            else:
                # 4D data
                for i, row_val in enumerate(parsed['row_dim_values']):
                    i_row_data = iter(parsed['data'][i])
                    for outter_val in parsed['outter_dim_values']:
                        for inner_val in parsed['inner_dim_values']:
                            for btm_val in parsed['btm_dim_values']:
                                val = next(i_row_data)
                                if val is None: continue
                                yield row_val, outter_val, inner_val, btm_val, val

        else:
            # 3D data
            for i, row_val in enumerate(parsed['row_dim_values']):
                i_row_data = iter(parsed['data'][i])
                for outter_val in parsed['outter_dim_values']:

                    for inner_val in parsed['inner_dim_values']:
                        val = next(i_row_data)
                        if val is None: continue
                        yield row_val, outter_val, inner_val, val

    else:
        # 2D data
        for i, row_val in enumerate(parsed['row_dim_values']):
            i_row_data = iter(parsed['data'][i])
            for outter_val in parsed['outter_dim_values']:
                val = next(i_row_data)
                if val is None: continue
                yield row_val, outter_val, val


if __name__ == '__main__':
    from statcrawl import conf
    with open(conf.datapath + '/VsObr_reg_00_10_ZapSt_mk.px', 'r') as f:
        parsed = parse(f.read().decode(ENC))
        for entry in iter_data(parsed):
            print ' '.join(map(str, entry))

