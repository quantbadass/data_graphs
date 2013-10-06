from urllib import urlretrieve
from csv import DictReader
from matplotlib import pyplot
from matplotlib.dates import date2num
from datetime import datetime

def fetchstockdata(stockticker, filename):
	url = 'http://ichart.finance.yahoo.com/table.csv?s=%s' % stockticker
	urlretrieve(url, filename)

def importstockdata (filename):
	results = {}
	for row in DictReader(open(filename,'rb')):
		for col in row.keys():
			if col == 'Date':
				coldata = date2num(datetime.strptime(row[col], '%Y-%m-%d'))
			else:
				coldata = row[col]
			results.setdefault(col,[]).append(coldata)
	return results

def plotstockdata(stockdata, stockticker, dates, col1, col2):
	pyplot.plot_date(stockdata[dates], stockdata[col1], '-', xdate=True)
	pyplot.plot_date(stockdata[dates], stockdata[col2], '-', xdate=True)
	pyplot.title('%s - %s / %s' %(stockticker, col1, dates))
	pyplot.xlabel(dates)
	pyplot.ylabel(col1)
	pyplot.savefig('%s.png' % stockticker)
	pyplot.show()

if __name__ == '__main__':
	from sys import argv
	TICKER = argv[1].upper()
	COL1 = argv[2]
	COL2 = argv[3]
	FILENAME = '%s.csv' % TICKER
	fetchstockdata(TICKER, FILENAME)
	DATA = importstockdata(FILENAME)
	plotstockdata(DATA, TICKER, 'Date', COL1, COL2)

