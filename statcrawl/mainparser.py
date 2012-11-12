
import os
from statcrawl import conf, parser

ENC = 'cp1251' # encoding of text in datafiles
VAL_KEYS = parser.VAL_KEYS


def traverse_files():
    """Iterator with all filenames with stats"""
    for filename in os.listdir(conf.datapath):
        if filename.endswith('.px'):
            yield conf.datapath + '/' + filename


def iter_dims(parsed):
    for key, val in parsed.iteritems():
        if not key.endswith('_key'): continue
        yield val, parsed[key[:-4] + '_values']


def main():
    all_dims = {}
    for file_ in traverse_files():
        parsed = parser.parse(open(file_).read().decode(ENC), skip_data = True)
        for dim, vals in iter_dims(parsed):
            try:
                all_dims[dim].update(set(vals))
            except KeyError:
                all_dims[dim] = set(vals)

    int_dims = set()
    float_dims = set()
    for dim in all_dims.keys():
        vals = all_dims[dim]
        try:
            new_vals = set(map(int, vals))
        except ValueError:
            try:
                new_vals = set(map(float, vals))
            except ValueError:
                # text
                print dim
                print ', '.join(vals)
                pass

            else:
                # floats
                float_dims.add(dim)
                all_dims[dim] = new_vals

        else:
            # ints
            int_dims.add(dim)
            all_dims[dim] = new_vals

    """
    dims_ = set()
    for dim, values in all_dims.iteritems():
        if len(values) < 10:
            dims_.add(dim)


    for d in sorted(all_dims.keys()):print d
    print len(all_dims)
    """



if __name__ == '__main__':
    main()


