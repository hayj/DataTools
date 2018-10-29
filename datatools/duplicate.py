from systemtools.basics import *
from systemtools.logger import *
from datastructuretools.hashmap import *

class Duplicate:
    def __init__ \
    (
        self,
        limit=None,
        maxMoSize=None, # 15000
        logger=None,
        verbose=True,
        maxDuplicates=1,
        name="duplicates",
        cleanEachNAction=None,
        doSerialize=False,
        ramAmountDivider=None,
        # user=None, password=None, host="localhost",
    ):
        """
            maxDuplicates is the max number of occurence for one element.
            If you give 2 same elements and the maxDuplicates is 2, the isDuplicate method will return False. But If you give 3 same elements, the method will return true.
            If you give identifier to the isDuplicate method, it will check if the element already exists and will not inc the count if it exists.

            By default, this datastructure will not growth more than ramAmount / (3 * cpuCount())

            TODO implement mongodb
        """
        self.ramAmountDivider = ramAmountDivider
        if self.ramAmountDivider is None:
            self.ramAmountDivider = cpuCount() * 3
        self.limit = limit
        self.maxMoSize = maxMoSize
        if self.limit is None and self.maxMoSize is None:
            self.maxMoSize = int(ramAmount() / self.ramAmountDivider * 1000)
        self.cleanEachNAction = cleanEachNAction
        if self.cleanEachNAction is None:
            if self.limit is not None:
                self.cleanEachNAction = int(self.limit / 4)
            elif self.maxMoSize is not None:
                # 5000000 correspond to 2Go of RAM, so we find the number f element for maxMoSize of ram and we clean each 1/4 of this value:
                self.cleanEachNAction = int(((self.maxMoSize / 1000) * 5000000 / 2) / 4)
            else:
                self.cleanEachNAction = int((2 * 5000000 / 2) / 4)
        self.doSerialize = doSerialize
        self.name = name
        self.maxDuplicates = maxDuplicates
        self.logger = logger
        self.verbose = verbose
        self.data = SerializableDict\
        (
            name=self.name,
            logger=self.logger,
            verbose=self.verbose,
            limit=self.limit,
            cleanMaxSizeMoReadModifiedOlder=self.maxMoSize,
            cacheCheckRatio=0.0,
            useMongodb=False,
            cleanEachNAction=self.cleanEachNAction,
            doSerialize=self.doSerialize,
        )

    def __md5(self, text):
        try:
            return md5(text)
        except:
            try:
                return md5(text.encode("utf-8"))
            except Exception as e:
                try:
                    logException(e, self, message=text)
                    return text
                except:
                    pass

    def __hash(self, l):
        if isinstance(l, list):
            lString = ""
            for current in l:
                lString += str(current)
            return self.__md5(lString)
        elif isinstance(l, str):
            return self.__md5(l)
        else:
            return self.__md5(objectAsKey(l))

    def setMaxDuplicates(self, maxDuplicates):
        self.maxDuplicates = maxDuplicates

    def duplicateCount(self, l):
        theHash = self.__hash(l)
        if self.data.has(theHash):
            return self.data[theHash]["count"]
        else:
            return 0

    def isDuplicate(self, l, identifier=None, addElement=True):
        theHash = self.__hash(l)
        if self.data.has(theHash):
            row = self.data[theHash]
            if identifier is None:
                row["count"] += 1
            else:
                if identifier in row["identifiers"]:
                    pass
                else:
                    row["count"] += 1
                    if addElement:
                        row["identifiers"].add(identifier)
            self.data[theHash] = row
        else:
            row = {"count": 0, "identifiers": set()}
            row["count"] += 1
            if identifier is not None and addElement:
                row["identifiers"].add(identifier)
            self.data[theHash] = row
        return row["count"] > self.maxDuplicates


if __name__ == '__main__':
    d = Duplicate()





