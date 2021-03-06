
# DataTools

This project gathers useful modules on url parsing, csv reading, html parsing etc.

## Installation (Python 3)

	git clone https://github.com/hayj/DataTools.git
	pip install ./DataTools/wm-dist/*.tar.gz

## NDJson

This class will allow you to read and write (append mode) objects as [Newline Delimited Json](http://jsonlines.org/) which is used to stream files (and do not load it all at once). It will automatically compress (or will not compress, according to the extension you give, or the compresslevel you give) using bz2.

	from datatools.jsonutils import *
	ndj = NDJson("/home/foo/mydata.ndjson.bz2")
	for currentDict in ndj: # Read line by line huge files as a stream
		print(currentDict)
	for i in range(10):
		ndj.append({"id": i}) # Append new objects (can be an iterable object or a dict)
	ndj.reset() # delete the file

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

This class is a wrapper over the `csv` lib, but it strip all lines (rows), handle the first line where we find column names (the csv lib doesn't take into account the first line as the header) and yield rows in dict structures.

	>>> from datatools.csvreader import *
	>>> c = CSVReader("data.csv")
	>>> for row in c:
	...     print(row)
	{'user_id': 1, 'name': 'a'}

Init parameters are `filePath, delimiter='\t', quotechar='|', strip=True, correctQuote=True, hasHeader=True, blankStringToNone=True`. `correctQuote` try to delete useless quotes in cells, to prevent this kind of cell: `'"a"'`.

## html2Text

This function convert html to text by taking benefit of both `html2text` and `BeautifulSoup`.

	>>> from datatools.htmltools import *
	>>> html2text("<html>...")