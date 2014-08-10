import util, csv

# load region_id, name, state from .MID
# load region_id, Tot_P_M, Tot_P_F, Tot_P_P from BO1
# load region_id, Median_age_persons, Median_rent_weekly, Median_Tot_prsnl_inc_weekly, Median_Tot_hhd_inc_weekly, Median_rent_weekly, Average_household_size from B02

region_headers, region_rows = csv.read('data', 'UCL_2011_AUST.MID', headers=['region_id','name','state_id','state','area'])
regions = csv.index(region_rows, region_headers, 'region_id', ['name','state','area'])

b01_headers, b01_rows = csv.read('data', '2011Census_B01_AUST_UCL_short.csv')
b01 = csv.index(b01_rows, b01_headers, 'region_id', ['Tot_P_M','Tot_P_F','Tot_P_P'])

b02_headers, b02_rows = csv.read('data', '2011Census_B02_AUST_UCL_short.csv')
b02 = csv.index(b02_rows, b02_headers, 'region_id', ['Median_Tot_prsnl_inc_weekly', 'Median_Tot_hhd_inc_weekly', 'Median_rent_weekly_', 'Average_household_size'])

# combine into one csv
rows = [['region_id', 'name', 'state', 'area', 'pop_total', 'pop_male', 'pop_female', 'med_weekly_personal_income', 'med_weekly_household_income', 'med_weekly_rent', 'avg_household_size']]

state_abbrev = {
	'Queensland': 'qld',
	'New South Wales': 'nsw',
	'Australian Capital Territory': 'act',
	'South Australia': 'sa',
	'Western Australia': 'wa',
	'Victoria': 'vic',
	'Northern Territory': 'nt',
	'Tasmania': 'tas',
	'Other Territories': 'ot'
}

for region_id, r in regions.items():
	b01_row = b01[region_id]
	b02_row = b02[region_id]

	rows.append([
		region_id,
		r['name'],
		state_abbrev[r['state']],
		r['area'],
		b01_row['tot_p_p'],
		b01_row['tot_p_m'],
		b01_row['tot_p_f'],
		b02_row['median_tot_prsnl_inc_weekly'],
		b02_row['median_tot_hhd_inc_weekly'],
		b02_row['median_rent_weekly_'],
		b02_row['average_household_size']
	])

csvrows = [','.join(row) for row in rows]
util.writetext('\n'.join(csvrows), 'output', 'census.csv')
	