#!/usr/bin/env python
import csv
import codecs
import os
import sys
import string
import timeit
import urllib2


start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')

# ######################
# myfile = open('final_output_unique.csv', 'wb')
# ######################
# wr = csv.writer(myfile)


# list1=[]
# ###################################
# with open('final_output_bg.csv', 'rb') as csvfile:
# ###################################	
# 	reader=csv.reader(csvfile)
# 	wr.writerow(['Unique-Prod'])
# 	next(reader)
# 	for row in reader:
# ##############################		
# 		word=row[6]
# ##############################		
# 		list1.append(word)

# 	# list1=	list(set(list1))
# 	# for item in list1:
# 	# 	tag=[]
# 	# 	tag.extend([item])
# 	# 	wr.writerow(tag)

# myfile.close()


db_dict={}
db_list=[]
with open('db_v2.csv','rb') as csvfile:
	reader=csv.reader(csvfile)
	next(reader)
	for row in reader:
		db_list.extend([row[0]])


######################
op_file = open('final_output_stat.csv', 'wb')
######################
wr2 = csv.writer(op_file)
# wr2.writerow(["Masterdish",'DB_flag'])
wr2.writerow(["Count","vendor_id","Menu_Cat_Tran","Prod_Tran","Clean_Prod","Variant","Masterdish","flag","Cuisine","cuisine_flag","Subcuisine","subcuisine_flag","Subcategory","subcategory_flag","DB_flag"])
with open('Algeria.csv','rb') as csvfile:
	count=1
	total=0
	reader=csv.reader(csvfile)
	next(reader)
	for row	in reader:
		total+=1

		md=row[6]

		if md in db_list:
			count+=1
			row.append("1")
		else:
			row.append('0')
		wr2.writerow(row)


	print "count =",count
	print "total =",total
	percent=(float(count)/total)*100
	print "Percentage Match With Database =",percent





op_file.close()



stop = timeit.default_timer()
total=stop-start
print "Time taken =",total