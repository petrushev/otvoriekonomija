import os.path
import csv

import pandas as pd
import xlrd

FILENAME = 'neplateni_obvrski.xlsx'


def main():
    dirname_ = os.path.dirname(__file__)
    full_path = os.path.join(dirname_, FILENAME)

    xls = xlrd.open_workbook(full_path)

    for sheet_name in xls.sheet_names():
        sheet = xls.sheet_by_name(sheet_name)
        fout_name = sheet_name.encode('utf-8') + '.csv'
        full_path_out = os.path.join(dirname_, 'csv', fout_name)

        with open(full_path_out, 'wb') as csv_f:
            wr = csv.writer(csv_f, quoting=csv.QUOTE_ALL)

            for row_id in range(sheet.nrows):
                row = []
                for col in sheet.row_values(row_id):
                    if isinstance(col, unicode):
                        col = col.encode('utf-8')
                    else:
                        col = str(col)
                    row.append(col)

                wr.writerow(row)


if __name__ == '__main__':
    main()
