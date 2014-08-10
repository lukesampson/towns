import util, csv, re
# combine ABS data with lat/lng from gazetteer

gaz_headers, gaz_rows = csv.read('output', 'gazetteer.csv')
gaz = csv.index(gaz_rows, gaz_headers, 'name')

census_headers, census_rows = csv.read('output', 'census.csv')

def lookup(name, state):
	key = re.sub(' *\([^\)]*\)', '', name.lower())
	key = re.sub(' - .*', '', key) # 2-part names, will use coordinates for first town
	if key not in gaz:
		# raise Exception('Couldn''t find {} in {}'.format(name,state))
		return None

	matches = gaz[key]
	if type(matches) is not list:
		matches = [matches]

	matches = [m for m in matches if m['state'] == state.upper()]

	if len(matches) == 0:
		# raise Exception('Couldn''t find {} in {}'.format(name,state))
		return None
	elif len(matches) == 1:
		return matches[0]

	pref = ['LOCB','URBN','PRSH','POPL','SUB','HMSD','LOCU']
	for p in pref:
		x = [m for m in matches if m['feat_code'] == p]
		if len(x) > 0:
			return x[0]

	raise Exception("Couldn't find '{}' in '{}'. Possible feature codes were {}".format(name, state, [m['feat_code'] for m in matches]))


outrows = [census_headers + ['lat','lng']]

for r in census_rows:
	cols = csv.row(r, census_headers)

	name = cols['name']
	state = cols['state']

	match = lookup(name, state)

	if match is not None:
		lat = match['lat']
		lng = match['lng']

		outrows.append(r + [lat,lng])
	else:
		print("Couldn't find {} in {}".format(name, state))


csvrows = [','.join(row) for row in outrows]
util.writetext('\n'.join(csvrows), 'output', 'combo.csv')
