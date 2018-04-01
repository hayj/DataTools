


import re
import html2text
from bs4 import BeautifulSoup
def html2Text(html):
    """
        https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python/47994071#47994071
    """
    def removeMarkdown(text):
        for current in ["^[ #*]{2,30}", "^[ ]{0,30}\d\\\.", "^[ ]{0,30}\d\."]:
            markdown = re.compile(current, flags=re.MULTILINE)
            text = markdown.sub(" ", text)
        return text
    def removeAngular(text):
        angular = re.compile("[{][|].{2,40}[|][}]|[{][*].{2,40}[*][}]|[{][{].{2,40}[}][}]|\[\[.{2,40}\]\]")
        text = angular.sub(" ", text)
        return text
    h = html2text.HTML2Text()
    h.images_to_alt = True
    h.ignore_links = True
    h.ignore_emphasis = False
    h.skip_internal_links = True
    text = h.handle(html)
    soup = BeautifulSoup(text, "html.parser")
    text = soup.text
    text = removeAngular(text)
    text = removeMarkdown(text)
    return text






if __name__ == '__main__':
    import glob
    from systemtools.file import *
    files = glob.glob("/home/hayj/Data/Misc/error404/from-newslist/ok/*.html")
    files = files[0:10]
    for filePath in files:
        print(html2Text(fileToStr(filePath)))




