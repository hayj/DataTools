import json
import bz2
import os

path = "test.bz2"
try:
	os.remove(path)
except OSError:
	pass

l = []
l.append({"a": 1})
l.append({"b": 2})

try:
	with bz2.open("test.bz2", "wt", compresslevel=9, encoding="utf-8") as f:
		for o in l:
			data = json.dumps(o)
			print("Trying to append to the file: " + data)
			f.write(data)
except Exception as e:
	print("Exception: " + str(e))





exit()
try:
	with bz2.open("test.bz2", "r") as f:
		for o in f.readlines():
			o = json.loads(o)
			print("A line in the bz2 file: " + str(o))
except Exception as e:
	print(str(e))

