# coding: utf8

import markdown as md
import codecs
import json
import pandas as pd
from systemtools.logger import *

def mdFileToText(inputPath):
    with codecs.open(inputPath, 'r', encoding='utf8') as mdFile:
        mdText = mdFile.read()
        return mdText

def mdFileToHtml(inputPath):
    with codecs.open(inputPath, 'r', encoding='utf8') as mdFile:
        mdText = mdFile.read()
        htmlText = md.markdown(mdText)
        return htmlText

def mdToHtml(mdText):
    return md.markdown(mdText)


def htmlToHtmlFile(outputPath, htmlText):
    with codecs.open(outputPath, "w", encoding="utf-8", errors="xmlcharrefreplace") as htmlFile:
        htmlFile.write(htmlText)


def csvToDictList(path, logger=None, verbose=True, **kwargs):
    try:
        df = pd.read_csv(path, **kwargs)
        return list(df.T.to_dict().values())
    except Exception as e:
        logException(e, logger, location="csvToDictList")
    return None


def dictListToCSV(dictList, path, logger=None, verbose=True, **kwargs):
    """
        quoting=csv.QUOTE_NONNUMERIC
    """
    try:
        if "delimiter" in kwargs:
            kwargs["sep"] = kwargs["delimiter"]
            del kwargs["delimiter"]
        df = pd.DataFrame(dictList)
        df.to_csv(path, index=False, **kwargs)
    except Exception as e:
        logException(e, logger, location="dictListToCSV")
