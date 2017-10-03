#!/usr/bin/env python
import csv
import codecs
import os
import sys
import string
import timeit
import urllib2
from difflib import SequenceMatcher
from urllib import urlopen
import json
from random import randint
from time import sleep

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')



f = open('complete_ing_file_pl.csv','w')
writer = csv.writer(f)
writer.writerow(["Count","vendor_id","Menu_Cat_Tran","Prod_Tran","Clean_Prod","Variant","Masterdish","flag","Cuisine","cuisine_flag","Subcuisine","subcuisine_flag","Subcategory","subcategory_flag","Ingredient"])

with open('ing-mapping.csv','r') as csvfile:
	master_file = csv.reader(csvfile)
	next(master_file)
	for row in master_file:
		subcuisine=row[10]
		if subcuisine=="pizza":
			row.extend(['pizza crust','mozzarella cheese','plum tomato'])
		elif subcuisine=="pasta":
			row.extend(['pasta','artichoke','olive oil'])

		check=row[14:]
		t=[]
		for word in check:
			if word!='':
				if word not in t:
					t.append(word)
		check=t
		# print check
		if len(check)>=3:
			check=check[:3]
		new_row=row[:14]
		new_row.extend(check)
			
		writer.writerow(new_row)

stop = timeit.default_timer()
time_taken = stop - start
print " Time taken is ", time_taken