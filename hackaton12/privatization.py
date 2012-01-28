
from csv import reader
from pprint import pprint
import matplotlib.pyplot as plot 
from datetime import date, datetime

a = datetime.now()

not_needed = 'from.id,from.name,from.taxonomy,id,sector.id,sector.taxonomy,time.day,time.id,time.label,time.month,time.name,time.quarter,time.taxonomy,time.week,time.year,time.yearmonth,to.id,to.taxonomy'.split(',')

def iter_data(path):
    with open(path, 'r') as f:
        fcsv = reader(f)
        labels = fcsv.next()
        for record in fcsv:
            data = dict(zip(labels, record))
            if 'Macedonia' not in data['from.label']: continue
            data['date']=datetime.strptime(data['time.name'], '%Y-%m-%d').date()
            for key in not_needed: del data[key]
            yield data

path = 'data/privatization_[world_bank].csv'

amounts_year = {}
counts_year = {}
for record in iter_data(path):
    amounts_year[record['date'].year] = amounts_year.get(record['date'].year, 0) + float(record['amount'])
    counts_year[record['date'].year] = counts_year.get(record['date'].year, 0) + 1

x = range(1989, 2008)
am = [amounts_year.get(year, 0)/1000000 for year in x]
cnts = [counts_year.get(year, 0) for year in x]

plot.bar(x, am)
plot.show()

#pprint(amounts_year)
#pprint(counts_year)

    