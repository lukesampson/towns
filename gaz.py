'''
download and extracts gazetteer data
'''

import util

def download_file(url, save_as):
	save_as = url.split('/')[-1]
	# NOTE the stream=True parameter
	r = requests.get(url, stream=True)
	with open(save_as, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				print('.', end='', flush = True)
				f.write(chunk)
				f.flush()


url = 'http://www.ga.gov.au/corporate_data/76695/GazetteerOfAustralia2012Package.zip'
save_as = relpath('cache', 'gazetteer.zip')

# todo: skip if save_as already exists

print('downloading...')
download_file(url, save_as)
