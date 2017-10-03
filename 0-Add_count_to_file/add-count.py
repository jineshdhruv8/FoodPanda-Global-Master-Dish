#!/usr/bin/env python
import csv
import os
import sys
import string
import timeit

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')

myfile = open('global_master_menu_ph_51_with_count.csv', 'wb')
wr = csv.writer(myfile)

list1=[]
with open('global_master_menu_ph_51.csv', 'rb') as csvfile:

	reader=csv.reader(csvfile)
	count= 0
	wr.writerow(['Count','Vendor','vendor_id','Menu','Menu_Category','Product'])
	next(reader)
	for row in reader:
		count+=1
		new_row=[]
		new_row.extend([count,row[1],row[2],row[3],row[4],row[5]])
		wr.writerow(new_row)