import csv
import collections
import string
import sys
from nltk.corpus import wordnet, stopwords
import difflib	
import timeit
reload(sys)
sys.setdefaultencoding('utf-8')


outputfile = open("AZ_entries_to_be_added.csv","wb")
writer = csv.writer(outputfile)
writer.writerow(['masterdish',"frequency"])


outputfile2 = open("single_words_AZ.csv","wb")
writer2 = csv.writer(outputfile2)
writer2.writerow(['masterdish',"frequency"])


outputfile3 = open("single_freq_AZ.csv","wb")
writer3 = csv.writer(outputfile3)
writer3.writerow(['masterdish',"frequency"])


outputfile1 = open("masterdish_final_db_output_after_AZ.csv","wb")
writer1 = csv.writer(outputfile1)
writer1.writerow(['masterdish',"freq"])


db_list = []
search = " abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=+_<>?,./:\";\'{}[]\'*\\\\\\"
weird_words = ['type','style','wala','main','add','carte','like','extra','flavour']
single_words= {}


stopwords_prod = []
with open('stopwords_prod.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		word = row[0].lower().strip()
		stopwords_prod.append(word)


classifier_menu= {}
single_freq= {}
db = {}
with open('db.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		db[row[0].lower().strip()] = int(row[1])
 		





with open('az_input.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		word=row[0].lower().strip()
		value=row[1]
		length= len(word.split())
		if length <5:
			key = row[0].lower().strip()
			masterdish_list=key.split()
			temp=[]
			for word in masterdish_list:

				if word not in temp:
					temp.append(word)
			length1=len(temp)
			
			if length1 >=1:
				if temp[0]=='and' or temp[length1-1]=='and':
					temp.remove('and')
				masterdish=' '.join(temp)
			else:
				masterdish=' '.join(masterdish_list)

			stopword_flag=True
			single_frequency=False
			single_word_flag=False
			temp_md=masterdish.split()
			for word in temp_md:

				if word in stopwords_prod:
					stopword_flag=False
					break
				if len(temp_md) == 2 and word in weird_words:
					stopword_flag=False
					break
				if len(temp_md) == 1:
					stopword_flag=False
					single_word_flag=True
					break
				if value =='1':
					stopword_flag=False
					single_frequency=True
					break

				# print "F =",stopword_flag
			if stopword_flag and single_frequency==False and single_word_flag==False:								
				classifier_menu[masterdish]=value
			elif single_frequency and single_word_flag==False:
				single_freq[masterdish]=value
			elif single_word_flag:
				single_words[masterdish]=value
	
				

	print len(classifier_menu)
	print len(single_words)
	print len(single_freq)
	for k,v in classifier_menu.iteritems():
		# print k+"----"+v
		if k in db.keys():
			# print k+"--"+str(db[k])
			db[k] = db[k] + int(v)
			# print k+"--"+str(db[k])
			
		else:
			new_row=[]
			flag=True
			for char in k:
				if search.find(char) < 0:
					flag=False
					break
			if flag:				
				new_row.extend([k,v])
 				writer.writerow(new_row)

for k,v in db.iteritems():
	new_db=[]	
	new_db.extend([k,v])
	writer1.writerow(new_db)

for k,v in single_words.iteritems():
	new_db1=[]	
	new_db1.extend([k,v])
	writer2.writerow(new_db1)

for k,v in single_freq.iteritems():
	new_db2=[]	
	new_db2.extend([k,v])
	writer3.writerow(new_db2)

