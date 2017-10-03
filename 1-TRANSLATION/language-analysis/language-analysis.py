#!/usr/bin/env python
import csv
import goslate
import codecs
import os
import sys
import string
import timeit
import urllib2
import random

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')

gs = goslate.Goslate()

myfile = open('language-analysis.csv', 'wb')
wr = csv.writer(myfile)
myfile2 = open('language-analysis-data.csv', 'wb')
wr2 = csv.writer(myfile2)
dict1={}

###########################################
with open('global_master_menu_hk_56_with_count.csv', 'rb') as csvfile:
###########################################	
	# print row
	input_list = list(csv.reader(csvfile)) 
	random_choice = random.sample(input_list, 5000)
	# print random_choice
	for list1 in random_choice:
		# print list1
		######################################
		for word in list1[5:6]:
		######################################	
			word=word.strip()
			# print word
			word_language=gs.detect(word)
			# print word_language
			if str(word_language) not in dict1:
				# print "12"
				dict1[str(word_language)]=1
			else:
				# print "34"
				dict1[str(word_language)]+=1
			new_row=[]

			###################################
			new_row.extend([list1[5],word_language])
			###################################

			wr2.writerow(new_row)

					
	print dict1
	key=dict1.keys()
	for word in key:
		myfile.write(word+','+str(dict1[word])+'\n')

stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken