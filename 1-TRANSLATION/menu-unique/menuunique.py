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

################################
myfile = open('menu_unique_CL.csv', 'wb')
################################
wr = csv.writer(myfile)
list1=[]
##################################
with open('global_master_menu_CL_12_with_count.csv', 'rb') as csvfile:
##################################
	reader=csv.reader(csvfile)
	count= 0
	wr.writerow(['Unique-Menu'])
	next(reader)
	for row in reader:
		count+=1
###############################		
		word=row[4]
###############################		
		word=word.strip()
		list1.append(word)

	list1=	list(set(list1))
	for item in list1:
		tag=[]
		tag.extend([item])
		wr.writerow(tag)
myfile.close()



dict_menu={}
gs = goslate.Goslate()

#####################################
myfile2 = open('menu_unique_translation_CL.csv', 'wb')
#####################################

wr2 = csv.writer(myfile2)

#####################################
with open('menu_unique_CL.csv', 'rb') as csvfile:
#####################################

	reader2=csv.reader(csvfile)
	count= 0
	wr2.writerow(['Unique-Menu','Unique-Menu-Translation','Match'])
	next(reader2)
	for row in reader2:
		count+=1
		tag=[]
		tag.extend([row[0]])
		menu_cat=row[0]
		# print menu_cat

		if ',' in menu_cat:
			menu_cat=menu_cat.replace(','," ")

		menu_cat=' '.join(menu_cat.split())

		if count > 0:		
			try:

				og=''
				og_trans=''
				og_dish=''
				og_match=''
				og_trans_rev=''
				lower=''
				lower_trans=''
				lower_trans_rev=''
				lower_trans_rev=''
				lower_dish=''
				new_tran=''
				f_check=True
				og=menu_cat.strip()
				og_dish=og
				lang=gs.detect(og_dish)

##############################################				
				if lang !='it' and lang !='pt':
					lang='es'				
###############################################

				og_trans=gs.translate(og_dish,'en',lang)
				# print og_trans

				if og_dish.islower():
					new_tran=og_trans
					tag.extend([new_tran,str(101)])
					dict_menu[menu_cat]=new_tran
				else:
					og_trans_rev=gs.translate(og_trans,lang,'en')
					og_match=0
					# print "ORIGINAL =",str(og)
					# print "ORIGINAL_Trans =",str(og_trans)
					# print "REV =",str(og_trans_rev)
					og_match=SequenceMatcher(None,str(og),str(og_trans_rev)).ratio()
					# print "Match =",og_match
					lower=menu_cat.lower().strip()
					lower_trans=gs.translate(lower,'en',lang)
					lower_trans_rev=gs.translate(lower_trans,lang,'en')
					lower_match=0
					lower_match=SequenceMatcher(None,str(lower),str(lower_trans_rev)).ratio()
					# print "Lower =",str(lower)
					# print "lower_trans =",str(lower_trans)
					# print "lower_trans_rev =",str(lower_trans_rev)
					# print "Match =",lower_match

					if lower_match == 1.0 and og_match == 1.0 and og.lower()==og_trans.lower():
						new_tran=lower_trans
						tag.extend([new_tran,str(int(lower_match *100))])
						f_check=False

					if f_check:
						if lower_match >= og_match:
							new_tran=lower_trans
							tag.extend([new_tran,str(int(lower_match *100))])

						else:
							new_tran=og_trans
							tag.extend([new_tran,str(int(og_match*100))])

					# print 'New =',new_tran
#############################################
					dict_menu[row[0]]=new_tran
##############################################					

	 		except:
	 			# print count
	 			dict_menu[row[0]]="ERROR"
	 			pass	
	 		# print tag
			wr2.writerow(tag)

myfile2.close()



######################################
myfile3 = open('CL-menu-translation-mapping.csv', 'wb')
######################################

wr3 = csv.writer(myfile3)

#########################################
with open('global_master_menu_CL_12_with_count.csv', 'rb') as csvfile:
#########################################

	reader=csv.reader(csvfile)
	count= 0
	wr3.writerow(['count','Menu-Category','Translation'])
	next(reader)
	for row in reader:

###################################		
		menu=row[4].strip()
###################################

		menu_tran='NOT FOUND'
		new_row=[]
		# print dict_menu.keys()
		if menu in dict_menu.keys():
			# print menu
			menu_tran=dict_menu[menu]
			# print menu_tran
		new_row.extend([row[0],menu,menu_tran])
		wr3.writerow(new_row)


stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken

