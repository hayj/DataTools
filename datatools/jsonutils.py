import json
import bz2
from systemtools.basics import *
from systemtools.location import *
from systemtools.duration import *
from systemtools.file import * 

def toJsonFile(data, path):
    if "/" not in path and "/" in data:
        data, path = path, data
    with open(path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

def fromJsonFile(filePath, logger=None, verbose=True):
    if isFile(filePath):
        with open(filePath) as f:
            return json.load(f)
    else:
        logError(str(filePath) + " not found.", logger=logger, verbose=verbose)
    return None

class NDJson:
	"""
		Newline Delimited Json http://jsonlines.org/

		a basic dataset of 3.9 Go (with extra data in) will take 74 Go of RAM
		so *19
	"""
	def __init__(self, filenameOrPath, dirPath=None, compresslevel=9, logger=None, verbose=True, indent=None, closeAtEachAppend=True):
		"""
			fileNameOrPath can be a full path or fileName (with or without extension)
			dirPath can be None or a dir path

			According to a benchmark in unit test, set closeAtEachAppend as True will increase speed, but set closeAtEachAppend as False will better compress the file
			use getEstimatedMoSize instead of getMoSize
		"""
		self.closeAtEachAppend = closeAtEachAppend
		self.writeFile = None
		self.indent = indent
		self.logger = logger
		self.verbose = verbose
		self.compresslevel = compresslevel
		self.alreadyWarnedAboutMoSize = False
		if self.compresslevel is None:
			self.compresslevel = 0
		if filenameOrPath is None:
			raise Exception("filenameOrPath param is None")
		if "/" in filenameOrPath and dirPath is not None:
			raise Exception("Don't use a path in bot fileNameOrPath and dirPath")
		if "/" in filenameOrPath and not (filenameOrPath[-4:] == ".bz2" or filenameOrPath[-7:] == ".ndjson"):
			raise Exception("Please use bz2 or ndjson extensions")
		if "/" in filenameOrPath and not (filenameOrPath.startswith("/") or filenameOrPath.startswith("~")):
			raise Exception("Please give an absolute path")
		if "/" in filenameOrPath:
			(dirPath, filename, ext, _) = decomposePath2(filenameOrPath)
		else:
			if dirPath is None:
				dirPath = tmpDir()
			if len(filenameOrPath) > 4 and filenameOrPath[-4:] == ".bz2":
				filename = filenameOrPath[:-4]
				ext = "bz2"
			elif len(filenameOrPath) > 7 and filenameOrPath[-7:] == ".ndjson":
				filename = filenameOrPath[:-7]
				ext = "ndjson"
			else:
				filename = filenameOrPath
				if self.compresslevel > 0:
					ext = "bz2"
				else:
					ext = "ndjson"
		self.path = dirPath + "/" + filename + "." + ext
		if ext != "bz2":
			if self.compresslevel > 0:
				logWarning("We will not compress " + self.path, self)
			self.compresslevel = 0
		self.estimatedSizeRefreshCount = 0
		self.previousMoSize = None

	def getPath(self):
		return self.path

	def reset(self):
		removeFile(self.path)

	def readlines(self):
		try:
			if isFile(self.path):
				self.close()
				if self.compresslevel > 0:
					f = bz2.open(self.path, "r")
				else:
					f = open(self.path, "r")
				for line in f.readlines():
					content = None
					try:
						content = json.loads(line)
					except TypeError as e:
						content = json.loads(line.decode('utf-8'))
					if content is not None:
						yield content
				f.close()
		except Exception as e:
			logException(e, self, message=str(self.path))

	def __iter__(self):
		return self.readlines()

	def write(self, *args, **kwargs):
		return self.append(*args, **kwargs)
	def append(self, items):
		if items is None:
			return
		if isinstance(items, dict):
			items = [items]
		elif isinstance(items, set):
			items = list(items)
		try:
		    items = iter(items)
		except:
		    items = [items]
		if self.writeFile is None:
			if self.compresslevel > 0:
				self.writeFile = bz2.open(self.path, "at", compresslevel=self.compresslevel)
			else:
				self.writeFile = open(self.path, "a")
			# print("a" * 100)
		# if self.compresslevel > 0:
		# 	def jsonYielder(items):
		# 		for current in items:
		# 			yield json.dumps(current)
		# 	f.writelines(jsonYielder(items))
		# else:
		for o in items:
			self.writeFile.write(str(json.dumps(o, indent=self.indent)) + "\n")
		if self.closeAtEachAppend:
			self.close()

	def close(self):
		if self.writeFile is not None:
			self.writeFile.close()
			self.writeFile = None

	def getSize(self):
		try:
			return os.path.getsize(self.path)
		except FileNotFoundError as e:
			return 0.0
		except Exception as e:
			logException(e, self)
			return 0.0

	def getMoSize(self):
		return self.getSize() / (1000 * 1000)

	def getEstimatedMoSize(self, refreshEach=100):
		if self.closeAtEachAppend and not self.alreadyWarnedAboutMoSize:
			logWarning("WARNING You use closeAtEachAppend, it can result to a wrong getEstimatedMoSize...", self)
			self.alreadyWarnedAboutMoSize = True
		if self.previousMoSize is None or \
			self.estimatedSizeRefreshCount == 0 or \
			self.estimatedSizeRefreshCount % refreshEach == 0:
			self.previousMoSize = self.getMoSize()
		self.estimatedSizeRefreshCount += 1
		return self.previousMoSize

if __name__ == '__main__':
	path = sortedGlob("/home/hayj/tmp/mbti-datasets/mbti-dataset-2019.05.15-19.14/0*")[0]
	f = NDJson(path)
	print(f.getEstimatedMoSize())
	# print(list(NDJson(tmpDir() + "/a9.bz2").readlines()))
	







