## Exporting suburb data from the Australian Gazetteer 2012

These are the steps to generate data/gazetteer2012_suburbs.csv, described here in case you want to re-generate
this data from scratch.

1. Install [mdbtools](https://github.com/brianb/mdbtools)

	`brew install mdbtools # Mac OS X`

2. Download and extract MDB for the [Gazetteer of Australia 2012](https://www.ga.gov.au/products/servlet/controller?event=GEOCAT_DETAILS&catno=76695)

3. Extract MDB data to CSV

Documentation for mdb-sql is [here](https://github.com/brianb/mdbtools/blob/master/doc/mdb-sql.txt).

 	```
 	mdb-sql -p -F -o data/gazetteer2012_suburbs.csv scratch/Gazetteer2012_mdb.mdb
 	```

	```sql
	select name, state_id, postcode, latitude, longitude, variant_name, status from tblmain where feat_code = 'SUB'
	go
	```