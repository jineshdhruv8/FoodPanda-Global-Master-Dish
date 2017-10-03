#!/usr/bin/env python
import csv
import goslate
import codecs
import os
import sys
import string
import timeit
import urllib2
import fuzzy
from difflib import SequenceMatcher

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')

####################
myfile = open('CL-full-Translation.csv', 'wb')
####################

wr = csv.writer(myfile)



dict_prod={}

######################
with open('CL-prod-translation-mapping-v2.csv', 'rb') as csvfile1:
######################

	reader1=csv.reader(csvfile1)
	count= 0
	# wr.writerow(['count','Product','Translation'])
	next(reader1)
	for row in reader1:
		prod_list=[]
		if ',' in row[2]:
			row[2]=row[2].replace(","," ")
		row[2]=' '.join(row[2].split())

		prod_list.extend([row[1],row[2]])	
		dict_prod[row[0]]=prod_list


#############################
with open('CL-menu-translation-mapping-v2.csv', 'rb') as csvfile1:
#############################

	reader1=csv.reader(csvfile1)
	count= 0
	wr.writerow(['Count','Menu','Menu-Tran','Product','Prod-Tran'])
	next(reader1)
	for row in reader1:
		if row[0] in dict_prod.keys():
			
			if ',' in row[2]:
				row[2]=row[2].replace(","," ")
			row[2]=' '.join(row[2].split())

			new_row=row[:3]
			new_row.extend(dict_prod[row[0]])
			wr.writerow(new_row)

stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken
