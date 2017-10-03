import csv
import collections
import string
import sys
from nltk.corpus import wordnet, stopwords
import difflib	
import timeit

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')

punctuations=[',','.','/','&','\\','\"','-','!','(',')','=',':',';','<','>','?','{','}','[',']','@','#','$','%','^','&','*','+',"'",'"','_','!','~','`','|']		


def punct(menu,punctuations):
	for char in menu:
		if char in punctuations:
			menu=menu.replace(char,' ')
	menu=' '.join(menu.split())	
	return menu

def add_classifier(product,menu,classifier_menu,classifier_list,stopwords_prod):
	prod=product
	if len(prod.split()) > 1:
		classifier_flag=True
		for word in classifier_list:
			# print word
			if set(word.split()).issubset(prod.split()):
				# print "www =",word
			 	if word in classifier_menu.keys():
					# print word
					if len(word.split())>1:
						prod=prod.replace(word,classifier_menu[word])				
						classifier_flag=False
					else:
						temp=''
						for item in prod.split():
							if item == word:
								item=classifier_menu[word]
							temp=temp+' '+item
						prod=' '.join(temp.split())
						classifier_flag=False
				else:
					return prod
			if not classifier_flag:
				return prod

		if classifier_flag:
			menu_flag=True
			menu=punct(menu,punctuations)
			for word in classifier_list:
				if set(word.split()).issubset(menu.split()):
					if word in classifier_menu.keys():
						prod=prod+" "+classifier_menu[word]
						menu_flag=False
						return prod
						break
			if menu_flag:
				return prod
		else:
			return prod	
	else:
		stopwords_flag=True
		for word in stopwords_prod:
			if set(word.split()).issubset(prod.split()):
				prod=prod
				stopwords_flag=False
				return prod
		# print "W =",product
		if stopwords_flag:
			menu=punct(menu,punctuations)
			classifier_flag=True
			for word in classifier_list:
				if set(word.split()).issubset(prod.split()):
					if word in classifier_menu.keys():
						if len(word.split())>1:
							prod=prod.replace(word,classifier_menu[word])				
							classifier_flag=False
						else:
							temp=''
							for item in prod.split():
								if item == word:
									item=classifier_menu[word]
								temp=temp+' '+item
							prod=' '.join(temp.split())
							classifier_flag=False
					else:
						return prod
				if not classifier_flag:
					return prod
			if classifier_flag:
				menu_flag=True
				menu=punct(menu,punctuations)
				for word in classifier_list:
					if set(word.split()).issubset(menu.split()):
						if word in classifier_menu.keys():
							prod=prod+" "+classifier_menu[word]
							menu_flag=False
							return prod
							break
				if menu_flag:
					return prod
			else:
				return prod





#Dict of Classifier for menu
classifier_menu= {}
classifier_list=[]
with open('classifier_menu_ashish_with_order.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		key = row[0].lower().strip()
		value=row[1].lower().strip()
		classifier_list.append(key)
		classifier_menu[key]=value

stopwords_prod = []
with open('stopwords_prod.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		word = row[0].lower().strip()
		stopwords_prod.append(word)


outputfile = open("PO-output-1.csv","wb")
writer = csv.writer(outputfile)

count=1
with open('output-new-updated-4.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	writer.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat','prod-1','prod-2','prod-3','prod-4','prod-5','Correct_MD'])
	next(reader)
	for row in reader:	
		product=row[12].lower().strip()
		
		tp=[]
		for word in product.split():
			if word in classifier_menu.keys():
				word=classifier_menu[word]
			tp.append(word)
		product=' '.join(tp)

##########################################################	
		prod_list=product.split()
		temp=[]	
		for word in prod_list:
			if word not in temp:
				temp.append(word)
		length=len(temp)
		if length >1:
			if temp[0]=='and' or temp[length-1]=='and':
				temp.remove('and')
		elif length == 1 and temp[0]=='and':
			temp.remove('and')
		product=' '.join(temp)

###########################################################

		clean_prod=row[3].lower().strip()
		menu=row[1].lower().strip()
		new_prod=add_classifier(product,clean_prod,classifier_menu,classifier_list,stopwords_prod)
		
		new_prod=add_classifier(new_prod,menu,classifier_menu,classifier_list,stopwords_prod)

		new_prod=' '.join(new_prod.split())
		
		prod_list=new_prod.split()
		temp=[]	
		for word in prod_list:
			if word not in temp:
				temp.append(word)
		new_prod=' '.join(temp)	
		
		row.extend([new_prod])
		# if new_prod != product:
		# 	row.append("1")
		# else:
		# 	row.append("0")
		writer.writerow(row)

stop = timeit.default_timer()
time_taken = stop - start
print "Total time to run =",time_taken	

