#!/usr/bin/env python
import csv
import goslate
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


def map_ing(md,ing_dict,common_list,animal_list,unique_db,row,wr3,ing):
	if md in ing_dict.keys():
		ing=ing_dict[md]


	ing_list=ing.split(',')

	blank_list=[]
	for q in ing_list:
		q=q.lower().strip()
		blank_list.extend([q])
	ing_list=blank_list

	# print ing_list
	new_list=[]

	for item in ing_list:
		flag1=True
		flag2=True
		# print "i =",item
		for word in common_list:
			if set(item.split()).issubset(word.split()):
				flag1=False
				break

		for word in animal_list:
			if set(item.split()).issubset(word.split()):
				if item in ing_list:
					flag2=False
					break
		if flag1 and flag2:
			new_list.append(item)
	ing_list=new_list


	if ing_list:
		temp=[]
		for word in ing_list:
			word=word.strip()
			for list_item in recipe_list:
				if list_item[0]==word:
					word=list_item[1]
			temp.append(word)

		new=[]
		new.append(md)
		new.append(','.join(temp))
		ing_list=temp
		if md not in unique_db:
			unique_db.append(md)
			w.writerow(new)

	row.extend(ing_list)


	check=row[14:]
	t=[]
	for word in check:
		if word not in t:
			t.append(word)
	check=t
	if len(check)>=3:
		check=check[:3]

	new_row=row[:14]
	new_row.extend(check)
	length=len(new_row)
	# print length
	if length < 17:
		if length ==14:
			new_row.extend(['','',''])
		elif length == 15:
			new_row.extend(['',''])
		elif length == 16:
			new_row.extend([''])

	wr3.writerow(new_row)
	return ""


input1=csv.reader(open('commoningredient_v2.csv','rb'))
common_list=[]
for row in input1:
	common_list.append(row[0].lower().strip())

db_dict={}
input1=csv.reader(open('db_ing.csv','rb'))
for row in input1:
	if row[0] not in db_dict.keys():
		db_dict[row[0]]=row[1]


animal_list=[]
input2=csv.reader(open('animallist.csv','rb'))
next(input2)
for row in input2:
	animal_list.append(row[0].lower().strip())


recipe_file = csv.reader(open('recipes_list_v4.csv'), delimiter=',', quotechar='"')
recipe_list = []
for row in recipe_file:
	recipe_list.append(row)



f = open('output.csv','w')
writer = csv.writer(f)
writer.writerow(["Count","vendor_id","Menu_Cat_Tran","Prod_Tran","Clean_Prod","Variant","Masterdish","flag","Cuisine","cuisine_flag","Subcuisine","subcuisine_flag","Subcategory","subcategory_flag","Ingredient"])

with open('final_output_pl.csv','r') as csvfile:
	master_file = csv.reader(csvfile)
	next(master_file)
	for row in master_file:
		
		if "alcoholic beverages" != row[8] and "dessert" != row[8]:
			cuisine=row[8]
			if cuisine == "non-alcoholic beverages":				
				subcuisine=row[10]
				if subcuisine == 'juice' or subcuisine == 'shake' or subcuisine == 'smoothie' or subcuisine == 'squash':
					for list_item in recipe_list:
						if set(list_item[0].split()).issubset(row[6].split()) or set(list_item[0].split()).issubset(row[3].split()) or set(list_item[0].split()).issubset(row[2].split()):
							row.append(list_item[1])
					md=row[6]
					if md in db_dict.keys():
						temp = db_dict[md].split(',')
						new_temp=temp[:3]
						x=[]
						for word in new_temp:
							word=word.strip()
							x.append(word)
						new_temp=x	
						row.extend(new_temp)
			else:
				for list_item in recipe_list:
						if set(list_item[0].split()).issubset(row[6].split()) or set(list_item[0].split()).issubset(row[3].split()) or set(list_item[0].split()).issubset(row[2].split()):
							row.append(list_item[1])
				md=row[6]
				if md in db_dict.keys():
					temp = db_dict[md].split(',')
					new_temp=temp[:3]
					x=[]
					for word in new_temp:
						word=word.strip()
						x.append(word)
					new_temp=x	
					row.extend(new_temp)
		writer.writerow(row)			
f.close()

myfile = open('unique-ing.csv', 'wb')
wr = csv.writer(myfile)


list1=[]
with open('output.csv', 'rb') as csvfile:
	reader=csv.reader(csvfile)
	wr.writerow(['Unique-Prod'])
	next(reader)
	for row in reader:
		word=row[6]
		if len(row) >= 17:
			pass
		elif "alcoholic beverages" != row[8] and "dessert" != row[8]:
			cuisine=row[8]
			if cuisine == "non-alcoholic beverages":				
				subcuisine=row[10]
				if subcuisine == 'juice' or subcuisine == 'shake' or subcuisine == 'smoothie' or subcuisine == 'squash':
					list1.append(word)
			else:
				list1.append(word)

	list1=	list(set(list1))
	for item in list1:
		tag=[]
		tag.extend([item])
		wr.writerow(tag)
myfile.close()



outputfile = open('unique-ing-result.csv','wb')
wr2=csv.writer(outputfile)
logfile = open('log.txt','wb')

ing_dict={}
with open("unique-ing.csv",'rb') as inputfile:
	reader = csv.reader(inputfile)
	count=1	
	wr2.writerow(['masterdish','rp-dish','Ingredient'])
	next(reader)
	for row in reader:
		tag=[]
		product = row[0]
		tag.extend([row[0]])
		query = product.lower().strip()
		count+=1
		if count >0:
			flag = False
			while not flag:		
				try:
					url = urlopen('http://www.recipepuppy.com/api/?q={0}'.format(query)).read()
					flag = True
				except:
					sleep(300)
			try:
				result = json.loads(url)
				content = result['results']

				if content:
					item = content[0]
					dish = []
					title = item['title'].strip().lower().replace('-',' ').replace(',','')
					ingr = item['ingredients']
					ing_dict[row[0]]=ingr
					tag.extend([title,ingr])
					wr2.writerow(tag)
			except:
				a=str(count)
				logfile.write(a + '\n')
				tag.extend(["",""])
				ing_dict[row[0]]=""
				wr2.writerow(tag)
				pass


myfile3 = open('ing-mapping.csv', 'wb')
wr3 = csv.writer(myfile3)
wr3.writerow(["Count","vendor_id","Menu_Cat_Tran","Prod_Tran","Clean_Prod","Variant","Masterdish","flag","Cuisine","cuisine_flag","Subcuisine","subcuisine_flag","Subcategory","subcategory_flag","Ingredient"])

dbfile = open('db_ing.csv', 'ab')
w = csv.writer(dbfile)

unique_db=[]
with open('output.csv', 'rb') as csvfile:
	reader=csv.reader(csvfile)
	count= 0
	next(reader)
	for row in reader:
		md=row[6]
		ing=''
		cuisine=row[8]
		subcuisine=row[10]
		new_row=[]
		if "alcoholic beverages" != cuisine and "dessert" != cuisine:
			if cuisine == "non-alcoholic beverages":								
				if subcuisine == 'juice' or subcuisine == 'shake' or subcuisine == 'smoothie' or subcuisine == 'squash':
					map_ing(md,ing_dict,common_list,animal_list,unique_db,row,wr3,ing)
				else:
					empty_dict={}
					map_ing(md,empty_dict,common_list,animal_list,unique_db,row,wr3,ing)
			else:
				map_ing(md,ing_dict,common_list,animal_list,unique_db,row,wr3,ing)
		else:
			empty_dict={}
			map_ing(md,empty_dict,common_list,animal_list,unique_db,row,wr3,ing)

stop = timeit.default_timer()
time_taken = stop - start
print " Time taken is ", time_taken