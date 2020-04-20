import json
from datetime import datetime, timedelta
import csv

def date_convertor(start):
	year = int(start)
	rem = start - year

	base = datetime(year, 1, 1)
	result = base + timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
	return result.strftime("%Y-%m-%d")

def traverse_tree(node,country_source):
	if 'children' in node:
		country = node['node_attrs']['country']['value'].lower() 
		for child in node['children']:
			traverse_tree(child,country)
	else:
		global writer,counter
		num_date = node['node_attrs']['num_date']['value']
		country  = node['node_attrs']['country']['value'].lower()
		
		if country_source != country and country_source != None:
			print(country_source,country,date_convertor(num_date))
			writer.writerow([country_source,country,date_convertor(num_date)])
			counter = counter + 1
		#x = int(input('Enter a number: '))

output_file=open( 'country_tran.csv', "w")
writer = csv.writer(output_file, delimiter=',')
writer.writerow(['source','destination','date'])
fi = open('ncov.json')
data = json.load(fi)
node = data['tree']
counter = 0
traverse_tree(node,None)
print(counter)
fi.close()
output_file.close()
