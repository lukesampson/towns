'''
download and extracts gazetteer data
'''

import util, requests, os.path, zipfile
import xml.etree.ElementTree as ET

GML_NS = '{http://www.opengis.net/gml}'
FME_NS = '{http://www.safe.com/gml/fme}'

def download_file(url, save_as):
	r = requests.get(url, stream=True)
	with open(save_as, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()

def fme(gml, name):
	el = gml.find(FME_NS + name)
	if el is None:
		return None

	return el.text


# ensure output directory exists
if not os.path.exists(util.relpath('output')):
	os.makedirs(util.relpath('output'))

# download gazeteer
url = 'http://www.ga.gov.au/corporate_data/76695/GazetteerOfAustralia2012Package.zip'
zip_path = util.relpath('cache', url.split('/')[-1])

if not os.path.exists(zip_path):
	print(zip_path)
	print('downloading {}...'.format(url, zip_path), end='', flush=True)
	download_file(url, zip_path)
	print('done')
else:
	print('using cached {}'.format(zip_path))

# extract Gazetteer2012_GML.zip from GazetteerOfAustralia2012Package.zip
unzip_dir = util.relpath('cache', 'gazetteer')
gml_zip_path = os.path.join(unzip_dir, 'Gazetteer2012_GML.zip')
if not os.path.exists(gml_zip_path):
	print('unzipping {}...'.format(zip_path), end='', flush=True)
	z = zipfile.ZipFile(zip_path)
	z.extract(member='Gazetteer2012_GML.zip',path=unzip_dir)
	print('done')
else:
	print('using cached Gazetteer2012_GML.zip')

# extract Gazetteer2012GML.gml from Gazetteer2012_GML.zip
gml = os.path.join(unzip_dir, 'Gazetteer2012GML.gml')
if not os.path.exists(gml):
	print('unzipping {}...'.format(gml_zip_path), end='')
	z = zipfile.ZipFile(gml_zip_path)
	z.extract(member='Gazetteer2012GML.gml',path=unzip_dir)
	print('done')

# parse to CSV
csv_path = util.relpath('output', 'gazetteer.csv')

if not os.path.exists(csv_path):
	print('parsing {}...'.format(gml), end='', flush=True)

	with open(csv_path, 'w') as f:
		f.write('name,state,feat_code,lat,lng,postcode\n')
		for event, el in ET.iterparse(gml):
			if(el.tag == GML_NS + 'featureMember'):
				gml = el.find(FME_NS + 'GML')
				
				name = fme(gml, 'NAME')
				if(name):
					state     = fme(gml, 'STATE_ID')
					feat_code = fme(gml, 'FEAT_CODE')
					lat       = fme(gml, 'LATITUDE')
					lng       = fme(gml, 'LONGITUDE')
					postcode  = fme(gml, 'POSTCODE')

					f.write('{},{},{},{},{},{}\n'.format(name.strip(), state, feat_code, lat, lng, postcode or ''))
				
				el.clear() # release memory
	print('done')
else:
	print('CSV already exists, skipping')

print('Gazetteer data import complete')