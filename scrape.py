import wp, re, util

cats = wp.subcats('Towns in Australia by state or territory')
print('found {} top-level categories'.format(len(cats)))

def extractdata(data, pagetitle):
	name = data.get('name')
	state = wp.striplinks(wp.striptags(data.get('state'))) # should only have abbreviation, strip anything else
	pop = wp.striplinks(wp.striptags(data.get('pop')))
	latlng = data.get('coordinates')

	if(pop):
		pop = re.match(r'\d+', pop)
		if(pop):
			pop = int(pop.group(0))
		else:
			pop = None
	else:
		pop = None

	return name, normalize(state), pop, latlng

def normalize(state):
	if state is None or state == '':
		return state

	state = state.lower()

	repl = {
		'queensland': 'qld',
		'western australia': 'wa',
		'new south wales': 'nsw'
	}

	if state in repl:
		state = repl[state]

	return state

def sort_state_then_pop(row):
	state,name,pop,latlng = row

	if state is None:
		state = ''

	if pop is None:
		pop = 0

	return (state, pop)

csv = []

for cat, catid in cats:
	print("Category: %s" % cat)
	pages = wp.catpages(catid)
	print('found {} pages for {}'.format(len(pages), cat))
	for title, pageid in pages:
		if title.startswith('Template:'):
			print("skipping template {}".format(title))
			continue

		text = wp.pagetext(pageid)
		try:
			infotype, data = wp.parseinfo(text)
		except:
			raise Exception("error parsing info for {} ({}):\n{}".format(title, pageid, text))

		if infotype:
			name, state, pop, latlng = extractdata(data, title)
			csv.append([state,name,pop,latlng])

			if not name:
				print('DEBUG: {} (page id {}) doesn''t have town name in infobox'.format(title, pageid))
		else:
			print('skipped {}'.format(title))

csv.sort(key=sort_state_then_pop)

rows = [','.join([str(col or '') for col in cols]) for cols in csv]
util.writetext('\n'.join(rows), 'output', 'towns.csv')
