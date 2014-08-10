import util

def read(*path, headers=None):
	csvpath = util.relpath(*path)

	rows = []

	def nextrow(f):
		line = f.readline()
		if line == '':
			return None
		return line.rstrip('\n').split(',')

	def getrows(f):
		while True:
			row = nextrow(f)
			if row is None: return
			yield row

	with open(csvpath) as f:
		if headers is None:
			headers = nextrow(f)

		for row in getrows(f):
			rows.append(row)

	return headers, rows

def row(row, headers):
	csvrow = {}
	for i, header in enumerate(headers):
		try:
			csvrow[header.lower()] = row[i]
		except:
			print(header.lower(), i, row)
			raise 

	return csvrow


def index(rows, headers, index_col, cols = None):
	indexed = {}

	if cols is None:
		cols = [c for c in headers if c != index_col]

	cols = [c.lower() for c in cols]

	for r in rows:
		csvrow = row(r, headers)

		indexrow = {}
		for c in cols:
			indexrow[c] = csvrow[c]

		key = csvrow[index_col].lower()
		if key in indexed:
			if type(indexed[key]) is list:
				indexed[key].append(indexrow)
			else:
				indexed[key] = [indexed[key],indexrow]
		else:
			indexed[key] = indexrow

	return indexed