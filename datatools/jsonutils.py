import json
import bz2
from systemtools.basics import *
from systemtools.location import *
from systemtools.duration import *
from systemtools.file import * 
from enum import Enum
import numpy as np

def ndarrayToList(*args, **kwargs):
    return ndarray2list(*args, **kwargs)
def ndarray2list(data):
    data = list(data)
    for i in range(len(data)):
        if isinstance(data[i], np.float32) or isinstance(data[i], np.float64):
            data[i] = float(data[i])
        elif isinstance(data[i], np.int32) or isinstance(data[i], np.int64):
            data[i] = int(data[i])
    return data


DUMP_STRATEGIES = Enum("DUMP_STRATEGIES", "none counterpart serialize")
DUMP_CONVERSION = \
{
	'set': \
	{
		'type': set,
		'key': '__set_type__',
		'isFunct': lambda x: isinstance(x, set),
		'serFunct': lambda x: list(x),
		'deserFunct': lambda x: set(x),
	},
	'tuple': \
	{
		'type': tuple,
		'key': '__tuple_type__',
		'isFunct': lambda x: isinstance(x, tuple),
		'serFunct': lambda x: list(x),
		'deserFunct': lambda x: tuple(x),
	},
	'ndarray': \
	{
		'type': np.ndarray,
		'key': '__ndarray_type__',
		'isFunct': lambda x: isinstance(x, np.ndarray),
		'serFunct': lambda x: ndarray2list(x),
		'deserFunct': lambda x: np.array(x),
	},
	'enum': \
	{
		'type': Enum,
		'key': '__enum_type__',
		'isFunct': lambda x: isinstance(x, Enum) and hasattr(x, 'name'),
		'serFunct': lambda x: serializeToStr(x),
		'deserFunct': lambda x: deserializeFromStr(x),
	},
	'float32': \
	{
		'type': np.float32,
		'key': '__float32_type__',
		'isFunct': lambda x: isinstance(x, np.float32),
		'serFunct': lambda x: float(x),
		'deserFunct': lambda x: np.float32(x),
	},
	'float64': \
	{
		'type': np.float64,
		'key': '__float64_type__',
		'isFunct': lambda x: isinstance(x, np.float64),
		'serFunct': lambda x: float(x),
		'deserFunct': lambda x: np.float64(x),
	},
	'unknown': \
	{
		'type': None,
		'key': '__unknown__',
		'isFunct': None,
		'serFunct': lambda x: serializeToStr(x),
		'deserFunct': lambda x: deserializeFromStr(x),
	},
}
DUMP_CONVERSION_KEYS = set([e['key'] for e in DUMP_CONVERSION.values()])

defaultMongoDollarEscape = "__doll__"
defaultMongoPointEscape = "__doll__"

def toJsonSerializable(*args, **kwargs):
	return toSerializableJson(*args, **kwargs)
def toSerializableJson\
(
	data,
	
	# Set the global strategy here:
	globalDumpStrategy=None,
	
	# Type conversion:
	unknownDumpStrategy=DUMP_STRATEGIES.serialize, # For objects that are not serializable
	tuplesDumpStrategy=DUMP_STRATEGIES.counterpart,
	setsDumpStrategy=DUMP_STRATEGIES.counterpart,
	ndarrayDumpStrategy=DUMP_STRATEGIES.counterpart,
	float32DumpStrategy=DUMP_STRATEGIES.counterpart,
	float64DumpStrategy=DUMP_STRATEGIES.counterpart,
	enumsDumpStrategy=DUMP_STRATEGIES.counterpart,
	
	# For mongodb:
	mongoStorable=False,
	gt8bIntegersAsStr=None, # Integers that are greater than 8 bytes
	escapeMongoKeys=None, # "." in keys will be replaced by "_", "$" are replaced by a specific str
	mongoDollarEscape=None,
	mongoPointEscape=None,
	
	# Misc:
	logger=None,
	verbose=True,
):
	"""
		This function convert any object in a JSON serializable version of it.
		It serialize unknown objects and convert known objets to its counterpart.
		You can then use `json.dump` to store the object.
		After a json load, you can use `fromSerializableJson` to deserialize the object.
	
		For mongodb, set gt8bIntegersAsStr and escapeMongoKeys booleans to True.
		
		If you choose serialize as the strategy for object that is not serializeable,
		it will create a list containing 2 elements :
		 * the first one is a specifi key related to the type
		 * the second is the base64 serialized object (see `systemtools.file.serializeAsStr`)
		
		If you choose `counterpart` as the strategy for set and tuples, it will be converted in list
		If you choose `counterpart` as the strategy for enum items, it will be converted in the name of the item
		
		DUMP_STRATEGIES.serialize allow you to totally reconstruct the object but you cannot read it easily in json format.
		DUMP_STRATEGIES.counterpart is more readable but you will loose structures like sets, tuples, enums...
		DUMP_STRATEGIES.none will raise exceptions in case an item is not serializable
	"""
	global defaultMongoDollarEscape
	if mongoDollarEscape is None:
		mongoDollarEscape = defaultMongoDollarEscape
	global defaultMongoPointEscape
	if mongoPointEscape is None:
		mongoPointEscape = defaultMongoPointEscape
	if globalDumpStrategy is not None:
		unknownDumpStrategy = globalDumpStrategy
		tuplesDumpStrategy = globalDumpStrategy
		setsDumpStrategy = globalDumpStrategy
		ndarrayDumpStrategy = globalDumpStrategy
		float32DumpStrategy = globalDumpStrategy
		float64DumpStrategy = globalDumpStrategy
		enumsDumpStrategy = globalDumpStrategy
	if unknownDumpStrategy == DUMP_STRATEGIES.counterpart:
		logWarning("You cannot set DUMP_STRATEGIES.counterpart as the strategy for unknown objects.",
				   logger=logger, verbose=verbose)
		unknownDumpStrategy = DUMP_STRATEGIES.none
	if mongoStorable and gt8bIntegersAsStr is None:
		gt8bIntegersAsStr = True
	if mongoStorable and escapeMongoKeys is None:
		escapeMongoKeys = True
	kwargs = \
	{
		'globalDumpStrategy': globalDumpStrategy,
		'unknownDumpStrategy': unknownDumpStrategy,
		'tuplesDumpStrategy': tuplesDumpStrategy,
		'setsDumpStrategy': setsDumpStrategy,
		'ndarrayDumpStrategy': ndarrayDumpStrategy,
		'float32DumpStrategy': float32DumpStrategy,
		'float64DumpStrategy': float64DumpStrategy,
		'enumsDumpStrategy': enumsDumpStrategy,
		'gt8bIntegersAsStr': gt8bIntegersAsStr,
		'escapeMongoKeys': escapeMongoKeys,
		'mongoDollarEscape': mongoDollarEscape,
		'mongoPointEscape': mongoPointEscape,
		'logger': logger,
		'verbose': verbose,
	}
	if data is None:
		return None
	elif isinstance(data, str) or \
	   isinstance(data, float) or \
	   isinstance(data, bool):
		return data
	elif isinstance(data, int):
		if gt8bIntegersAsStr and intByteSize(data) >= 8:
			return str(data)
		else:
			return data
	elif isinstance(data, list):
		newList = []
		for current in data:
			newList.append(toSerializableJson(current, **kwargs))
		return newList
	elif isinstance(data, dict):
		newData = {}
		for key, value in data.items():
			if not isinstance(key, str):
				raise Exception("dict keys must be str")
			value = toSerializableJson(value, **kwargs)
			if escapeMongoKeys and isinstance(key, str):
				key = key.replace(".", mongoPointEscape)
				if key.startswith("$"):
					key = mongoDollarEscape + key[1:]
			newData[key] = value
		return newData
	elif isinstance(data, tuple):
		if tuplesDumpStrategy == DUMP_STRATEGIES.none:
			raise Exception("tuple type is not JSON serializable", logger=logger, verbose=verbose)
		else:
			obj = []
			for current in data:
				current = toSerializableJson(current, **kwargs)
				obj.append(current)
			if tuplesDumpStrategy == DUMP_STRATEGIES.serialize:
				obj = [DUMP_CONVERSION['tuple']['key'], obj]
			return obj
	elif isinstance(data, set):
		if setsDumpStrategy == DUMP_STRATEGIES.none:
			raise Exception("set type is not JSON serializable", logger=logger, verbose=verbose)
		else:
			obj = []
			for current in data:
				current = toSerializableJson(current, **kwargs)
				obj.append(current)
			if setsDumpStrategy == DUMP_STRATEGIES.serialize:
				obj = [DUMP_CONVERSION['set']['key'], obj]
			return obj
	elif DUMP_CONVERSION['float32']['isFunct'](data):
		if float32DumpStrategy == DUMP_STRATEGIES.none:
			raise Exception("np.float32 type is not JSON serializable", logger=logger, verbose=verbose)
		else:
			obj = DUMP_CONVERSION['float32']['serFunct'](data)
			if float32DumpStrategy == DUMP_STRATEGIES.serialize:
				obj = [DUMP_CONVERSION['float32']['key'], obj]
			return obj
	elif DUMP_CONVERSION['ndarray']['isFunct'](data):
		if ndarrayDumpStrategy == DUMP_STRATEGIES.none:
			raise Exception("np.ndarray type is not JSON serializable", logger=logger, verbose=verbose)
		else:
			obj = DUMP_CONVERSION['ndarray']['serFunct'](data)
			if ndarrayDumpStrategy == DUMP_STRATEGIES.serialize:
				obj = [DUMP_CONVERSION['ndarray']['key'], obj]
			return obj
	elif DUMP_CONVERSION['float64']['isFunct'](data):
		if float64DumpStrategy == DUMP_STRATEGIES.none:
			raise Exception("np.float64 type is not JSON serializable", logger=logger, verbose=verbose)
		else:
			obj = DUMP_CONVERSION['float64']['serFunct'](data)
			if float64DumpStrategy == DUMP_STRATEGIES.serialize:
				obj = [DUMP_CONVERSION['float64']['key'], obj]
			return obj
	elif DUMP_CONVERSION['enum']['isFunct'](data):
		if enumsDumpStrategy == DUMP_STRATEGIES.none:
			raise Exception("enum type is not JSON serializable", logger=logger, verbose=verbose)
		else:
			if enumsDumpStrategy == DUMP_STRATEGIES.serialize:
				obj = DUMP_CONVERSION['enum']['serFunct'](data)
				obj = [DUMP_CONVERSION['enum']['key'], obj]
			elif enumsDumpStrategy == DUMP_STRATEGIES.counterpart:
				obj = data.name
			return obj
	else:
		try:
			obj = json.dumps(data)
			logWarning("The type " + str(type(data)) + " is JSON serializable but not taken into account in the toSerializableJson funct", logger=logger, verbose=verbose)
			return data
		except:
			assert unknownDumpStrategy != DUMP_STRATEGIES.counterpart
			if unknownDumpStrategy == DUMP_STRATEGIES.none:
				raise Exception(str(type(data)) + " type is not JSON serializable", logger=logger, verbose=verbose)
			try:
				obj = DUMP_CONVERSION['unknown']['serFunct'](data)
				return [DUMP_CONVERSION['unknown']['key'], obj]
			except Exception as e:
				logException(e, logger=logger, verbose=verbose)
				raise Exception("Cannot serialize " + str(data))


def fromJsonSerializable(*args, **kwargs):
	return fromSerializableJson(*args, **kwargs)
def fromSerializableJson\
(
	data,
	unescapeMongoKeys=True,
	mongoDollarEscape=None,
	mongoPointEscape=None,
	logger=None,
	verbose=True,
):
	"""
		This function takes an object that was loaded from a json serialized by the function `toJsonSerializable`.
		Thus it remove type metion in 2 elements lists.
	"""
	global defaultMongoDollarEscape
	if mongoDollarEscape is None:
		mongoDollarEscape = defaultMongoDollarEscape
	global defaultMongoPointEscape
	if mongoPointEscape is None:
		mongoPointEscape = defaultMongoPointEscape
	kwargs = \
	{
		'logger': logger,
		'verbose': verbose,
	}
	if data is None:
		return None
	elif isinstance(data, str) or \
	   isinstance(data, float) or \
	   isinstance(data, int) or \
	   isinstance(data, bool):
		return data
	elif isinstance(data, list) and len(data) == 2 and isinstance(data[0], str) and data[0] in DUMP_CONVERSION_KEYS:
		if data[0] == DUMP_CONVERSION['set']['key']:
			obj = data[1]
			for i in range(len(obj)):
				obj[i] = fromSerializableJson(obj[i], **kwargs)
			return set(obj)
		elif data[0] == DUMP_CONVERSION['tuple']['key']:
			obj = data[1]
			for i in range(len(obj)):
				obj[i] = fromSerializableJson(obj[i], **kwargs)
			return tuple(obj)
		elif data[0] == DUMP_CONVERSION['float32']['key']:
			return DUMP_CONVERSION['float32']['deserFunct'](data[1])
		elif data[0] == DUMP_CONVERSION['float64']['key']:
			return DUMP_CONVERSION['float64']['deserFunct'](data[1])
		elif data[0] == DUMP_CONVERSION['ndarray']['key']:
			return DUMP_CONVERSION['ndarray']['deserFunct'](data[1])
		elif data[0] == DUMP_CONVERSION['enum']['key']:
			return DUMP_CONVERSION['enum']['deserFunct'](data[1])
		elif data[0] == DUMP_CONVERSION['unknown']['key']:
			return DUMP_CONVERSION['unknown']['deserFunct'](data[1])
	elif isinstance(data, dict):
		newData = {}
		for key, value in data.items():
			if key.startswith(mongoDollarEscape):
				key = '$' + key[len(mongoDollarEscape):]
			if mongoPointEscape in key:
				key = key.replace(mongoPointEscape, '.')
			value = fromSerializableJson(value, **kwargs)
			newData[key] = value
		return newData
	elif isinstance(data, list):
		newList = []
		for current in data:
			newList.append(fromSerializableJson(current, **kwargs))
		return newList
	else:
		# logWarning("The type " + str(type(data)) + " is not taken into account in the fromSerializableJson funct", logger=logger, verbose=verbose)
		return data








def toJsonFile(data, path):
	if "/" not in path and "/" in data and '\n' not in data:
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
	







