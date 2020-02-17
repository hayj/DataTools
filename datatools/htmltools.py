import re
import html2text
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
from bs4 import BeautifulSoup
from systemtools.logger import logException


def html2Text(html, logger=None, verbose=True):
    """
        https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python/47994071#47994071
    """
    try:
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
    except Exception as e:
        logException(e, logger=logger, location="html2Text", verbose=verbose)
        return html



def getSoupText(soup, cssSelector=None):
    if cssSelector is not None:
        soup = soup.select_one(cssSelector)
    if soup is None:
        return None
    else:
        text = soup.getText()
        if text is None:
            return None
        else:
            text = text.strip()
            if text == "":
                return None
            else:
                return text.strip()

def getSoupAttr(soup, attr, cssSelector=None):
    if cssSelector is not None:
        soup = soup.select_one(cssSelector)
    if soup is None:
        return None
    else:
        if soup.has_attr(attr):
            return soup[attr]
        else:
            return None


if __name__ == '__main__':
    import glob
    from systemtools.file import *
    files = glob.glob("/home/hayj/Data/Misc/error404/from-newslist/ok/*.html")
    files = files[0:10]
    for filePath in files:
        print(html2Text(fileToStr(filePath)))




