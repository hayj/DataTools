# coding: utf-8

import publicsuffix
from publicsuffix import PublicSuffixList
from urllib.parse import urlparse
from enum import Enum
from systemtools.file import *
from systemtools.location import *
from systemtools.basics import *
from datatools.csvreader import *
import codecs
import re
from url_normalize import url_normalize
from systemtools.logger import *
import re
from urllib.parse import urljoin

URLLEVEL = Enum('URLLEVEL', 'ALL SMART ONE TWO')

WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

# import urltools
# def normalizeUrl(url):
#     return urltools.normalize(url)

# def strToUrls(text):
#     urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
#     if urls is None:
#         return []
#     return urls


class URLParser():
    def __init__(self, pslCachePath=None, timeSpentMax=10, verbose=True, logger=None):
        self.logger = logger
        self.verbose = verbose
        self.pslCachePath = pslCachePath
        if self.pslCachePath is None:
            self.pslCachePath = tmpDir() + "/psl.txt"
        self.timeSpentMax = timeSpentMax
        self.psl = None
        # self.initPublicSuffixList()
        self.urlEnhanceRegex = re.compile('^(?:http|ftp|https)://.*')
        self.urlRegex = None
        # self.normalizeExceptionAlreadyPrinted = False

    def isNormalizable(self, *args, **kwargs):
        return self.canBeNormalized(*args, **kwargs)

    def canBeNormalized(self, url):
        try:
            if url is None:
                return False
            url = url.strip()
            normalizedUrl = url_normalize(url)
        except:
            return False
        return True


    def normalize(self, url):
        if url is None:
            return None
        url = url.strip()
        if url == "":
            return ""
        try:
            normalizedUrl = url_normalize(url)
            return normalizedUrl
        except Exception as e:
            # if not self.indexExceptionAlreadyPrinted:
            logException(e, self, message=url, location="URLParser.normalize()")
            return url

        # if not self.urlEnhanceRegex.match(url):
        #     url = "http://" + url
        # return url

    def join(self, baseUrl, relativeUrl):
        """
            use http://... or https://... for baseUrl
        """
        if relativeUrl is not None and relativeUrl.startswith("http"):
            return relativeUrl
        if baseUrl is None or len(baseUrl) < 5 or not baseUrl.startswith("http"):
            return relativeUrl
        baseUrl = self.normalize(baseUrl)
        result = relativeUrl
        try:
            result = urljoin(baseUrl, relativeUrl)
        except Exception as e:
            logException(e, self, location="URLParser join")
        return result


    def strToUrls(self, text):
        if self.urlRegex is None:
            self.urlRegex = re.compile(WEB_URL_REGEX)
        if text is None or text == "":
            return []
        else:
            urls = self.urlRegex.findall(text)
            for i in range(len(urls)):
                urls[i] = self.normalize(urls[i])
            return urls

    def isImage(self, url):
        parsedUrl = self.parse(url)
        path = parsedUrl.path
        if re.match(".*\.(jpg|png|gif)$", path):
            return True
        return False

    def isDocument(self, url):
        parsedUrl = self.parse(url)
        path = parsedUrl.path
        if re.match(".*\.(pdf|doc|docx|odt)$", path):
            return True
        return False

    def isMedia(self, url):
        parsedUrl = self.parse(url)
        path = parsedUrl.path
        if re.match(".*\.(mp3|mp4|mkv|ogg|wav|avi|flac|oga)$", path):
            return True
        return False

    def initPublicSuffixList(self):
        if self.psl is not None:
            return self.psl
        try:
            if fileExists(self.pslCachePath) and getLastModifiedTimeSpent(self.pslCachePath, TIMESPENT_UNIT.DAYS) < self.timeSpentMax:
                pslFile = codecs.open(self.pslCachePath, encoding='utf8')
                self.psl = PublicSuffixList(pslFile)
                pslFile.close()
                return self.psl
            else:
                (dir, filename, ext, filenameExt) = decomposePath(self.pslCachePath)
                mkdirIfNotExists(dir)
                pslData = list(publicsuffix.fetch())
                removeIfExists(self.pslCachePath)
                strToFile(pslData, self.pslCachePath)
                self.psl = PublicSuffixList(pslData)
                return self.psl
        except Exception as e:
            logException(e, self, location="initPublicSuffixList")
            return None

    def getSmartDomain(self, domain):
        """
            PRIVATE
            This method return a smart domain given a domain.
            It remove subdomains and take into account public suffix list.
            Examples : "www.newsnow.co.uk" gives "newsnow.co.uk", "www.google.com"
            gives "google.com" and "test.com" gives "test.com"
        """
        if domain is None:
            logError("The domain is None", self)
            return None
        if domain.startswith("http:/") or domain.startswith("https:/"):
            logError("The domain can't be an url", self)
            return None
        domain = domain.strip()
        if domain == "":
            return None
        domain = domain.lower()
        self.initPublicSuffixList()
        try:
            return self.psl.get_public_suffix(domain)
        except Exception as e:
            logException(e, self, location="getSmartDomain")
            return None

    def getDomain(self, url, urlLevel=URLLEVEL.SMART):
        """
            This method gives a domain from an url. URLLEVEL.SMART refer to getSmartDomain.
        """
        if url is None or not isinstance(url, str):
            return None
        url = self.normalize(url)
        parsedUri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsedUri)
        domain = domain.lower()
        if urlLevel == URLLEVEL.ALL:
            return domain
        elif urlLevel == URLLEVEL.ONE:
            theSplit = domain.split(".")
            if len(theSplit) > 0:
                return theSplit[-1]
            else:
                return None
        elif urlLevel == URLLEVEL.TWO:
            theSplit = domain.split(".")
            if len(theSplit) > 1:
                return ".".join(theSplit[-2:])
            else:
                return None
        elif urlLevel == URLLEVEL.SMART:
            return self.getSmartDomain(domain)

    def parse(self, url):
        if url is None:
            return None
        url = self.normalize(url)
        try:
            theParse = urlparse(url)
            return theParse
        except Exception as e:
            logError("Exception location: URLParser.parse()", self)
            logError(str(e), self)
            return None



if __name__ == '__main__':
    urlParser = URLParser()
    print(urlParser.normalize("http://.bellinghamherald.com/news/local/article181035811.html"))
    print(urlParser.normalize("amazon.com"))
    print(urlParser.normalize("amazon.com//"))
#     print(urlParser.getDomain("http://www.newsnow.co.uk/h/", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://www.github.com/test", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://truc.github.com/test", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://truc.gitb.com/test", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("http://decoetart.over-blog.com/", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("http://www.bbc.com/news/world-us-canada-41543631", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("http://www.huffingtonpost.co.za/2017/10/08/zuma-has-dismissed-as-mischievous-claims-that-he-has-preferred-candidates-for-the-sabc-board_a_23236416/?utm_hp_ref=za-homepage", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://www.stuff.co.nz/business/small-business/97687085/wellington-restaurant-closes-after-selling-two-illegal-wines-and-a-beer", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://ipblv.blogspot.fr/", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://mamasworkpresents.tumblr.com/post/166151594535/this-is-a-best-love-quote-from-didnt-know-it", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("https://careers.global/1/2503446/", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("member.nownews.com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("news.china.com.cn", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("news.shm.com.cn", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("tw.trendmicro.com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("www.dffy.com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("www.halonoviny.cz", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("github.com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain(None, urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("com.com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("com.com.com", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("http:/t", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("http://t", urlLevel=URLLEVEL.SMART))
#     print(urlParser.getDomain("http://www.newsnow.co.uk/h/", urlLevel=URLLEVEL.ONE))
#     print(urlParser.getDomain("http://www.newsnow.co.uk/h/", urlLevel=URLLEVEL.TWO))
#     print(urlParser.getDomain("http://www.newsnow.co.uk/h/", urlLevel=URLLEVEL.ALL))


    print(urlParser.parse("http://www.google.com/truc/test.html;param1;parm2;?test=1&truc=2#id1"))


#



#     from proxietest import *
#     taoUrlGenerator = TaoUrlGenerator(dataPath)
#     for theDict in taoUrlGenerator:
#         if len(getDomain(theDict["url"]).split(".")) > 3:
#             print(theDict["url"])
#             print(getSmartDomain(theDict["url"]))
#             print()
#             input()

#     print(getDomain("aaram.net"))
#     print(getDomain("www.aaram.net"))
#     print(getDomain("http://www.aaram.net"))

#     cr = CsvReader('/home/hayj/Dashboard/Notes/Recherche/news-website-list/google-news-sources.csv')
#     for row in cr:
#         print(row["url"])
#         print(getSmartDomain(row["url"]))
#         print()
#         input()

#     print(listToStr2(getPublicSuffixList()))

