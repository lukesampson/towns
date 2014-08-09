import wp, re, util

cats = wp.subcats('Towns in Australia by state or territory')
print('found {} top-level categories'.format(len(cats)))

def extractdata(data, pagetitle):
	name = data.get('name')
	state = wp.striplinks(wp.striptags(data.get('state'))) # should only have abbreviation, strip anything else
	pop = wp.striplinks(wp.striptags(data.get('pop')))

	if(pop):
		pop = re.match(r'\d+', pop)
		if(pop):
			pop = int(pop.group(0))
		else:
			pop = None
	else:
		pop = None

	return name, state, pop

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
			name, state, pop = extractdata(data, title)
			csv.append("{},{},{}".format(state,name,pop))

			if not name:
				print('DEBUG: {} (page id {}) doesn''t have town name in infobox'.format(title, pageid))
		else:
			print('skipped {}'.format(title))

util.writetext('\n'.join(csv), 'output', 'towns.csv')
