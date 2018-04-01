from datatools.url import *
from systemtools.basics import *
from systemtools.system import *
from systemtools.location import *
from systemtools.logger import *
from datastructuretools.hashmap import *
import requests

class BashScripts:
    def __init__(self, logger=None, verbose=True, sdName="bashsripts", limit=100,
                scriptsLink=None,
                scriptExt="sh"):
        if not scriptExt.startswith("."):
            scriptExt = "." + scriptExt
        self.logger = logger
        self.verbose = verbose
        self.scriptsLink = scriptsLink
        if self.scriptsLink is None:
            self.scriptsLink = "https://raw.githubusercontent.com/" + getUser() + "/Bash/master/"
        self.scriptExt = scriptExt
        self.urlParser = URLParser()
        self.bashScriptsSD = SerializableDict\
        (
            sdName,
            limit=limit,
            funct=self.downloadScript,
            cleanNotReadOrModifiedSinceNDays=10,
            serializeEachNAction=1,
            cleanEachNAction=1,
            cacheCheckRatio=0.0,
        )

    def get(self, scriptName):
        if self.bashScriptsSD.has(scriptName) and \
        (self.bashScriptsSD[scriptName] is None or \
         len(self.bashScriptsSD[scriptName]) < 2):
            del self.bashScriptsSD[scriptName]
        return self.bashScriptsSD[scriptName]

    def downloadScript(self, scriptName):
        try:
            log("Downloading " + scriptName + self.scriptExt + " file on " +
                str(self.urlParser.getDomain(self.scriptsLink)), self)
            url = self.scriptsLink + scriptName + self.scriptExt
            result = requests.get(url).text
            return result
        except Exception as e:
            logException(e, self, location="downloadScript")
            return None

