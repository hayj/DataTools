# coding: utf8

import markdown as md
import codecs
import json

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





