import os

def relpath(*path):
	basedir = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(basedir, *path)

def readtext(*path):
	path = relpath(*path)
	if not os.path.exists(path):
		return None

	f = open(path, 'r')
	text = f.read()
	f.close()
	return text

def writetext(text, *path):
	path = relpath(*path)
	dir = os.path.dirname(path)
	if not os.path.exists(dir):
		os.makedirs(dir)

	f = open(path, 'w')
	f.write(text)
	f.close()