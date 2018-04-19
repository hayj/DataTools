# coding: utf-8


import csv

# TODO inherit JsonReader with openFunct etc...

class CSVReader():
    def __init__\
    (
        self,
        filePath,
        delimiter='\t',
        quotechar='|',
        quoting=csv.QUOTE_NONNUMERIC,
        strip=True,
        correctQuote=True,
        hasHeader=True,
        blankStringToNone=True
    ):
        """
            If your CSV file has a redaer, you can set hasHeader as True, so the iter will
            yield dicts instead of tuples
            blankStringToNone will set, for each row, all "" elements to None
            strip will strip all elements
            correctQuote will remove quote at the begining and the end of each element if exists
        """
        self.filePath = filePath
        self.delimiter = delimiter
        self.correctQuote = correctQuote
        self.strip = strip
        self.quoting = quoting
        self.quotechar = quotechar
        self.hasHeader = hasHeader
        self.blankStringToNone = blankStringToNone
        self.reader = csv.reader(open(filePath, newline=''),
                                 delimiter=self.delimiter,
                                 quotechar=self.quotechar,
                                 quoting=self.quoting)

    def __iter__(self):
        if not self.hasHeader:
            for row in self.reader:
                newRow = []
                for currentValue in list(row):
                    if self.strip:
                        currentValue = currentValue.strip()
                    if self.correctQuote:
                        if len(currentValue) > 0 \
                        and currentValue[0] == '"' \
                        and currentValue[-1] == '"':
                            currentValue = currentValue[1:-1]
                    if self.blankStringToNone and currentValue == "":
                        currentValue = None
                    newRow.append(currentValue)
                yield tuple(newRow)
        else:
            cols = None
            for row in self.reader:
                if cols is None:
                    cols = row
                else:
                    theDict = {}
                    for currentCol in cols:
                        theDict[currentCol] = None
                    i = 0
                    for i in range(len(row)):
                        if i < len(cols):
                            currentValue = row[i]
                            currentCol = cols[i]
                            if self.strip and isinstance(currentValue, str):
                                currentValue = currentValue.strip()
                            if self.correctQuote:
                                if isinstance(currentValue, str) \
                                and len(currentValue) > 0 \
                                and currentValue[0] == '"' \
                                and currentValue[-1] == '"':
                                    currentValue = currentValue[1:-1]
                            if self.blankStringToNone and currentValue == "":
                                currentValue = None
                            theDict[currentCol] = currentValue
                            i += 1
                    thereIsAtLeastOneValue = False
                    for key, value in theDict.items():
                        if value is not None:
                            thereIsAtLeastOneValue = True
                            break
                    if thereIsAtLeastOneValue:
                        yield theDict


def test1():
    c = CSVReader("/home/hayj/Data/Misc/news-website-list/data/list.csv")
    for row in c:
        print(row)

if __name__ == '__main__':
    test1()
#     from systemtools.basics import *
#     for hasHeader in [True, False]:
#         cr = CSVReader('/home/hayj/Data/Misc/news-website-list/data/list.csv', hasHeader=hasHeader)
#         i = 0
#         for current in cr:
#             printLTS(current)
#             i += 1
#             if i == 5:
#                 break
















