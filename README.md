
# DataTools

This project gathers useful modules on url parsing, csv reading, html parsing etc.

## Installation (Python 3)

	git clone https://github.com/hayj/DataTools.git
	pip install ./DataTools/wm-dist/*.tar.gz

## URLParser

This class use [public suffix list](https://publicsuffix.org/) (which is cached and reloaded every 10 days) to find "sub-domain" and "domain" parts of an url so you can compare urls:

	>>> from datatools.csvreader import *
	>>> u = URLParser()
	>>> u.getDomain('https://amazon.co.uk/aaa')
	'amazon.co.uk'
	>>> u.getDomain('https://www.amazon.co.uk/aaa')
	'amazon.co.uk'
	>>> u.getDomain('https://www.google.fr/aaa')
	'google.fr'

It also provide some useful methods like `URLParser.normalize(url)` which normalize a malformed url:

	>>> u.normalize("amazon.com")
	'http://amazon.com/'
	>>> u.normalize("https://amazon.com//")
	'https://amazon.com/'

The method `URLParser.strToUrls(text)` extract all urls from a string:

	>>> u.strToUrls("test1 http://test.com test2 http://test2.com")
	['http://test.com', 'http://test2.com']

See the code for more informations (`URLParser.join`, `URLParser.parse`...).

## CSVReader

This class is a wrapper over the `csv` lib, but it strip all lines (rows), handle the the first line where we find column names (the csv lib doesn't take into account the first line as the header) and yield row in dict structures.

	>>> from datatools.csvreader import *
	>>> c = CSVReader("data.csv")
	>>> for row in c:
	...     print(row)
	{'user_id': 1, 'name': 'a'}

See the code for init params.

## html2Text

This function convert html to text by taking benefit of both `html2text` and `BeautifulSoup`.

	>>> from datatools.htmltools import *
	>>> html2text("<html>...")