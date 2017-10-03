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

######################
myfile = open('prod_unique_CL.csv', 'wb')
######################

wr = csv.writer(myfile)


list1=[]

###################################
with open('global_master_menu_CL_12_with_count.csv', 'rb') as csvfile:
###################################	

	reader=csv.reader(csvfile)
	count= 0
	# punctuations=[',','.','&','/','\\','\'','\"','-','!','(',')','=',':',';','<','>','?','{','}','[',']']
	wr.writerow(['Unique-Prod'])
	next(reader)
	for row in reader:
		# print row
		count+=1

##############################		
		word=row[5]
##############################		

		word=word.strip()
		list1.append(word)

	list1=	list(set(list1))
	for item in list1:
		tag=[]
		tag.extend([item])
		wr.writerow(tag)
		# myfile.write(item+"\n")
	# wr.writerow(list(set(list1)))
myfile.close()



dict_prod={}
gs = goslate.Goslate()

#############################
myfile2 = open('prod_unique_translation_CL.csv', 'wb')
#############################

wr2 = csv.writer(myfile2)

#############################
with open('prod_unique_CL.csv', 'rb') as csvfile:
#############################

	reader2=csv.reader(csvfile)
	count= 0
	wr2.writerow(['Unique-Prod','Unique-Prod-Translation','Match'])
	next(reader2)
	for row in reader2:
		count+=1
		tag=[]
		tag.extend([row[0]])
		prod=row[0]

		if ',' in prod:
			prod=prod.replace(','," ")

		prod=' '.join(prod.split())

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
				og=prod.strip()
				og_dish=og
				lang=gs.detect(og_dish)

#########################################				
				if lang !='it' and lang !='pt':
					lang='es'
#########################################

				og_trans=gs.translate(og_dish,'en',lang)
				# print og_trans

				if og_dish.islower():
					new_tran=og_trans
					tag.extend([new_tran,str(101)])
					dict_prod[prod]=new_tran
				else:
					og_trans_rev=gs.translate(og_trans,lang,'en')
					og_match=0
					# print "ORIGINAL =",str(og)
					# print "ORIGINAL_Trans =",str(og_trans)
					# print "REV =",str(og_trans_rev)
					og_match=SequenceMatcher(None,str(og),str(og_trans_rev)).ratio()
					# print "Match =",og_match
					lower=prod.lower().strip()
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
#################################################
					dict_prod[row[0]]=new_tran
#################################################


	 		except:
	 			dict_prod[row[0]]="ERROR"
	 			# print count
	 			pass	
	 		# print tag
			wr2.writerow(tag)

myfile2.close()


# print dict_prod

########################
myfile3 = open('CL-prod-translation-mapping.csv', 'wb')
########################

wr3 = csv.writer(myfile3)

############################
with open('global_master_menu_CL_12_with_count.csv', 'rb') as csvfile:
############################

	reader=csv.reader(csvfile)
	count= 0
	wr3.writerow(['count','Product','Translation'])
	next(reader)
	for row in reader:
###############################
		prod=row[5].strip()
###############################		
		prod_tran='NOT FOUND'
		new_row=[]
		# print dict_menu.keys()
		if prod in dict_prod.keys():
			# print menu
			prod_tran=dict_prod[prod]
			# print menu_tran
			
		new_row.extend([row[0],prod,prod_tran])		
		wr3.writerow(new_row)



stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken
