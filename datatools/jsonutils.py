import json
import bz2
from systemtools.basics import *
from systemtools.location import *
from systemtools.duration import *
from systemtools.file import *

class NDJson:
	"""
		Newline Delimited Json http://jsonlines.org/
	"""
	def __init__(self, filenameOrPath, dirPath=None, compresslevel=9, logger=None, verbose=True):
		"""
			fileNameOrPath can be a full path or fileName (with or without extension)
			dirPath can be None or a dir path
		"""
		self.logger = logger
		self.verbose = verbose
		self.compresslevel = compresslevel
		if self.compresslevel is None:
			self.compresslevel = 0
		if filenameOrPath is None:
			raise Exception("filenameOrPath param is None")
		if "/" in filenameOrPath and dirPath is not None:
			raise Exception("Don't use a path in bot fileNameOrPath and dirPath")
		if "/" in filenameOrPath and not (filenameOrPath[-4:] == ".bz2" or filenameOrPath[-7:] == ".ndjson"):
			raise Exception("Please use bz2 or ndjson extensions")
		if "/" in filenameOrPath and not filenameOrPath.startswith("/"):
			raise Exception("Please give an absolute path")
		if "/" in filenameOrPath:
			(dirPath, filename, ext, _) = decomposePath(filenameOrPath)
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

	def getPath(self):
		return self.path

	def reset(self):
		removeFile(self.path)

	def readlines(self):
		if isFile(self.path):
			if self.compresslevel > 0:
				f = bz2.open(self.path, "r")
			else:
				f = open(self.path, "r")
			for line in f.readlines():
				yield json.loads(line)
			f.close()

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
		if self.compresslevel > 0:
			f = bz2.open(self.path, "at", compresslevel=self.compresslevel)
		else:
			f = open(self.path, "a")
			# print("a" * 100)
		# if self.compresslevel > 0:
		# 	def jsonYielder(items):
		# 		for current in items:
		# 			yield json.dumps(current)
		# 	f.writelines(jsonYielder(items))
		# else:
		for o in items:
			f.write(str(json.dumps(o)) + "\n")
		f.close()





if __name__ == '__main__':
	print(list(NDJson(tmpDir() + "/a9.bz2").readlines()))
	




