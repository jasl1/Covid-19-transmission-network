import json
from datetime import datetime, timedelta
import csv

def date_convertor(start):
	year = int(start)
	rem = start - year

	base = datetime(year, 1, 1)
	result = base + timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
	return result.strftime("%Y-%m-%d")

def traverse_tree(node,country_source,location_source,cs,ls,pp):
	if 'children' in node:

		country = node['node_attrs']['country']['value'].lower()
		#print(country,len(node['children']))
		#print('--------',country,country_source,location_source,len(node['children']),pp)
		location = location_source
		country_location = country_source 
		locs={}
		jj = 0
		for child in node['children']:
			jj += 1
			_location_, _country_ = traverse_tree(child,country_location,location,country_source,location_source,jj)
			if country == _country_:
				if _location_ in locs:
					locs[_location_] += 1
				else:
					locs[_location_] = 1
				location = max(locs, key=locs.get)
				country_location = country
				if location_source == None:
					country_source = country
					location_source = location
			'''else:
				print(country,_country_,len(node['children']),country_source,location_source)
				#for child in node['children']:
				#	print(child['node_attrs']['division']['value'].lower())
				x = int(input('Enter a number: '))'''	
				
		return location, country_location
	else:
		global writer,counter
		num_date = node['node_attrs']['num_date']['value']
		country  = node['node_attrs']['country']['value'].lower()
		
		age = None
		sex = None
		city = None
		division = None
		location_destination = None
		if 'age' in node['node_attrs']:
			age = node['node_attrs']['age']['value']
		if 'division' in node['node_attrs']:
			division  = node['node_attrs']['division']['value'].lower()
		if 'sex' in node['node_attrs']:
			sex = node['node_attrs']['sex']['value'].lower()
		if 'location' in node['node_attrs']:
			city  = node['node_attrs']['location']['value'].lower()
		
		if city == None and division == None: 
			location_destination = country
		elif city == None:
			location_destination = division
		else:
			location_destination = city
		if ls != location_destination and ls != None:
			print(ls,location_destination,date_convertor(num_date),pp)
			writer.writerow([ls,location_destination,date_convertor(num_date)])
			counter = counter + 1
		return location_destination, country
		#x = int(input('Enter a number: '))

output_file=open( 'city_tran.csv', "w")
writer = csv.writer(output_file, delimiter=',')
writer.writerow(['source','destination','date'])
fi = open('ncov.json')
data = json.load(fi)
node = data['tree']
counter = 0
traverse_tree(node,None,None,None,None,1)
print(counter)
fi.close()
output_file.close()
