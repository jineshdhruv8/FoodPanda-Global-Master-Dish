#!/usr/bin/env python
import csv
import goslate
import codecs
import os
import sys
import string
import timeit
import urllib2

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')

gs = goslate.Goslate()
def contains_number(string): return any(char.isdigit() for char in string)

with open('global_master_menu_VN.csv', 'rb') as csvfile:
	myfile = codecs.open('new-translation.csv', 'ab','utf-8')
	wr = csv.writer(myfile)
	reader=csv.reader(csvfile)
	count= 1
	punctuations=[',','.','&','/','\\','\'','\"','-','!','(',')','=',':',';','<','>','?','{','}','[',']']
	# wr.writerow(['# Vendor', 'vendor_id', 'menu', 'Menu_Category', 'Product', 'Variation','Cuisine'])
	next(reader)
	for row in reader:
		
		count+=1
		tag=[]
		# tag.extend([row[0],row[1],row[2]])
		tag.extend([str(count),row[3],row[4]])
		menu_cat=row[3]
		prod=row[4]
		if count > 43924 and count <= 60000:
			#print "row =",row
			for word in row[3:5]:
				#print "word11 =",word

				list1 = word.strip()
				# print "strip word =",word
				for char in list1:
					if char in punctuations:
						word=word.replace(char," ")
						# print "Punctuation word =",word
				split_word=word.split()
				#print "split=",split_word
				full_list=[]
				for data in split_word:
					#print "DATA =",data
					if not contains_number(data):
						try:
							language=gs.detect(data)
							#print "language =",language
							if language!="en":
								#if language=="pt":
									#language="pt_PT"
								code="echo "+data+" | aspell --master="+language+" pipe"
								# code = code.encode('utf-8')
								os.system(code) 
								a= os.popen(code).readlines()[1]
								#print "a=",a[0]
								#print a
								if a[0]=='*' or a[0]=='#':
									pass
									#print "* =",data
								elif a[0]=="&": 
									#print a
									#print "uncorrect =",data
									data=a.split(":")[1]
									data=data.split(",")[0].strip()
									# print "correct =",data
							else:
								#print "passed word =",data
								pass
						except:
							#print "except =",data
							print "spell check error in line number for language other than english =",count 
							pass
						full_list.append(data)
					else:
						#print "NUMBER =",data
						full_list.append(data)
						pass
					#print "FULL =",full_list
				
				word=' '.join(word for word in full_list)
				#print "final =",word
				try:
					word_language=gs.detect(word)
					#print "final language =",word_language
					if word_language!="en":
						#print "IN IF LOOP"
						word=gs.translate(word,'en',word_language)
		 		except:
		 			print "translate error in the line number =",count
		 			pass	
	 			tag.append(word)

			final_string = ','.join(word for word in tag)
			
			myfile.write(final_string + '\n')
			# wr.writerow(tag)
 		
print "Final count= ",count
myfile.close()

stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken