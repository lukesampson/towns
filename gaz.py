'''
download and extracts gazetteer data
'''

import util, requests, os.path, zipfile

def download_file(url, save_as):
	r = requests.get(url, stream=True)
	with open(save_as, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()


# download gazeteer
url = 'http://www.ga.gov.au/corporate_data/76695/GazetteerOfAustralia2012Package.zip'
zip_path = util.relpath('cache', url.split('/')[-1])

if not os.path.exists(zip_path):
	print(zip_path)
	print('downloading {}...'.format(url, zip_path), end='')
	download_file(url, zip_path)
	print('done')
else:
	print('using cached {}'.format(zip_path))

# extract Gazetteer2012_GML.zip from GazetteerOfAustralia2012Package.zip
unzip_dir = util.relpath('cache', 'gazetteer')
gml_zip_path = os.path.join(unzip_dir, 'Gazetteer2012_GML.zip')
if not os.path.exists(gml_zip_path):
	print('unzipping {}...'.format(zip_path), end='')
	z = zipfile.ZipFile(zip_path)
	z.extract(member='Gazetteer2012_GML.zip',path=unzip_dir)
	print('done')
else:
	print('using cached Gazetteer2012_GML.zip')

# extract Gazetteer2012GML.gml from Gazetteer2012_GML.zip
if not os.path.exists(os.path.join(unzip_dir, 'Gazetteer2012GML.gml')):
	print('unzipping {}...'.format(gml_zip_path), end='')
	z = zipfile.ZipFile(gml_zip_path)
	z.extract(member='Gazetteer2012GML.gml',path=unzip_dir)
	print('done')
