import csv
import urllib2
import json

API_KEY = 'AIzaSyD3FgGc1u0uA8nCy1DemLvUC1t0XRTo1Sw'
BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?components=postal_code:'

def convert_to_lat_long(filename):
	with open('new_hampshire_final.csv', 'w') as final_data:
		
		with open(filename) as f:
			reader = csv.DictReader(f)
			fieldnames = reader.fieldnames + ["latlong"]
			writer = csv.DictWriter(final_data, fieldnames = fieldnames)
			writer.writeheader()	
			zips = get_unique_zips(filename)

			codes = get_zips(zips)
			for row in reader:
				new_row = {}
				row_zip = row["contbr_zip"][:5]
				for field in reader.fieldnames:
					new_row[field] = row[field]
				new_row["latlong"] = codes[row_zip]
				print(new_row)
				writer.writerow(new_row)

def get_zips(data):
	rv = {}
	for zip_code in data:
		url = BASE_URL + str(zip_code) + '&key=' + API_KEY
		# req = urllib.request.Request(url) 
		try:
			response = urllib2.urlopen(url)
			print("Calling... " + url)
		except Exception:
			print('URL Error: ' + url )
			continue

		
		
		try:
			data = json.load(response)
			lat_long_dict = data['results'][0]['geometry']['location']
			rv[zip_code] = (lat_long_dict['lat'],lat_long_dict['lng'])


		except Exception:
			print('No json:' + url )
			continue
		# lat_long_dict = data['results'][0]['geometry']['location']
		# rv[zip_code] = (lat_long_dict['lat'],lat_long_dict['lng'])

	return rv

def get_unique_zips(filename):
	zip_codes = set()

	with open(filename) as f: 
		reader = csv.DictReader(f)

		for row in reader:
			x = row["contbr_zip"][:5]
			zip_codes.add(x)

	return zip_codes


