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



def load_db(input_dict):
	freq = {}
	for k in input_dict.keys():
		if input_dict[k] in freq.keys():
			freq[input_dict[k]] += 1
		else:
			freq[input_dict[k]] = 1
	freq_list = []
	for k,v in freq.iteritems():
		freq_list.append([k,v])
	change_list = []
	sorted_list = sorted(freq_list,key=lambda x:(x[1],x[0]))
	rm_freq_list = []
	for each_row in sorted_list:
		rm_freq_list.append(each_row[0])
	count = 0
	for row in rm_freq_list:
		count += 1
		for find_row in rm_freq_list[count:]:
			if ' '.join(sorted(row.lower().split())) == ' '.join(sorted(find_row.lower().split())):
				change_list.append([row,find_row])
	for k in input_dict.keys():
		for r in change_list:
			if input_dict[k] == r[0]:
				input_dict[k] = r[1]
	return input_dict







ing = []
with open('check_words.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		word = row[0].lower().strip()
		ing.append(word)

stopwords_prod = []
with open('stopwords_prod.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		word = row[0].lower().strip()
		stopwords_prod.append(word)



#Dict of non-alcoholic drinks
classifier_menu= {}
with open('classifier_menu.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		key = row[0].lower().strip()
		value=row[1].lower().strip()
		classifier_menu[key]=value

# print menu_dict





alpha = "abcdefghijklmnopqrstuvwxyz"
prep_check_words=['fried rice','noodle soup','rice noodle','rice noodles','fried noodle','fried noodles','soup noodle','soup noodles','stewed noodle','stewed noodles','baked rice','stirred instant noodle','stirred instant noodles','fried flat noodle','fried flat noodles']
punctuations=[',','.','/','&','\\','\"','-','!','(',')','=',':',';','<','>','?','{','}','[',']','@','#','$','%','^','&','*','+',"'",'"','_','!','~','`','|']		

list_7up_cocacola=['7 Up','7 UP','7 up','7 uP','7-Up','7-UP','7.up','7-up','7-uP','7up','7UP','7Up','7uP','coca cola','COCA COLA','coca-cola','COCACOLA']

cola_list=['cola','coca','coke']

softdrink_list=['pepsi','mirinda','cocacola','thumbs up','coca-cola','7up','mirinda','sprite','fanta','limca','twister']

prep=['with','in','over','by','above','at','from','on','about']

list_bbq=['b b q','b l t']

quantity=['lb','oz','ozs','lbs''plate','seasonal','little','per','v.','big','small','large','medium','can','cans','per','l','L','glass','ly','ml','litre','gram','grams','gm','gms','kg','kgs','cl','pcs','pieces','piece','bottle','bottles','large','medium','med','small','inch','inches','g']

phrase=['small bottle of','small bottles of','large bottle of','large bottles of','per glass','per bottle','big bowl of','bowl of','bottle of','bottles of']

stopwords = list(set(stopwords.words('english')))
stopwords.remove('and')
stopwords.extend(['light','extra','addon','add-on','extras','spare','day','spare','double','alacarte','regular','fresh','homemade','bowl','plate','little','hs','HS','add','cup','however','often','widest','special','children','review','reviews','authentic'])
# print stopwords
remove_phrase=['freshly brewed','ala carte','add on']
menu_phrase_remove=[]

def punct(menu,punctuations):
	for char in menu:
		if char in punctuations:
			menu=menu.replace(char,' ')
	menu=' '.join(menu.split())	
	return menu


outputfile = open("output.csv","wb")
writer = csv.writer(outputfile)

count=1
with open('HU-full-Translation-output-1.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	# writer.writerow(['count','masterdish','flag','new-masterdish','new-variant','variant'])
	writer.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat'])
	# Vendor, vendor_id, menu,count,menu-category,product,Menu-Category-translated,Product-translated,Master dish,New-masterdish,Cuisine
	next(reader)
	for row in reader:	
		count+=1
		new_row=[]
		new_master=""
		new_variant=""
		product=""
		variant=""
		product=row[4].lower().strip()
		og_product=product
		cuisine=row[7]
		subcuisine=row[8]
		subcat=row[9]

		new_row.extend([row[0],row[2],row[4]])
		# print row
		# print cuisine
		if cuisine != "alcoholic beverages":
		
			# print product
			# print row[0]
			# Replace '&' by 'and' to avoid removal of '&' from punctuation	
			if "&" in product.split():
				product=product.replace('&',' and ')
				product=' '.join(product.split())

	        
			# Replace words like 7 up by 7up and coca Cola by coca cola,etc.
			flag_7up=False
			new_prod=product
			# print "P =",product
			for word in list_7up_cocacola:
				if word in new_prod:
					if "7" in word:
						new_prod=new_prod.replace(word,"7up")
						flag_7up=True
					else:
						new_prod=new_prod.replace(word,"cocacola")	
			product=new_prod
			# print "p_new -",product
			pt=""
			for word in product.split():
				if word in cola_list:
					word='cocacola'
					pt=pt+' '+word
				else:
					pt=pt+' '+word
			product=pt


			# To move bracket contents to variant and remove it from product
			alpha_flag=False
			for word  in product:
				if '(' in word:
					if '(' in product and ')' in product:
						index1=product.find('(')
						index2=product.find(')')

###########################
						if index2 < index1:
							product=product.replace(')',"",1)
							index1=product.find('(')
							index2=product.find(')')
###########################

						for char in product[(index1+1):index2]:
							if char in alpha:
								alpha_flag=True
						#if bracket does not contains only numbers than below code will be run else not.
						if alpha_flag:
							new_variant = new_variant + product[(index1+1):index2]
							remove=product[(index1):(index2+1)]
							product=product.replace(remove," ")
							product=' '.join(product.split())
							alpha_flag=False
							index3=product.find('(')
							index4=product.find(')')


#######################################
							if index4 < index3:
								product=product.replace(')',"",1)
								index3=product.find('(')
								index4=product.find(')')
#######################################


							if index3 > 0 and index4 > 0:
								for char in product[(index3+1):index4]:					
									if char in alpha:
										alpha_flag=True
								
								if alpha_flag:
									new_variant = new_variant +' '+ product[(index3+1):index4]
									remove=product[(index3):(index4+1)]
									product=product.replace(remove," ")
									product=' '.join(product.split())
								else:
									remove=product[(index3):(index4+1)]
									product=product.replace(remove," ")
									product=' '.join(product.split())
						else:
							remove=product[(index1):(index2+1)]
							product=product.replace(remove," ")
							product=' '.join(product.split())
			#Remove '/' from product 
			high1=0
			high2=0
			index=0
			animal_flag=False
			new_list=[]
			if '/' in product:
				slash_list=product.lower().strip().split('/')
				for word in slash_list:
					ing_flag=False
					word=word.lower().strip()
					for item in word.split():		
						if item in ing:
							ing_flag=True
					length=len(word.split())

					if ing_flag:
						if length > high1:
							high1=length
							product=word
							animal_flag=True
							# print "p1 =",product
					if not animal_flag:				
						if length > high2:
							high2=length
							product=word
							# print "p2 =",product
					new_list.append(word)
						# print product
				new_list.remove(product)
				new_variant=new_variant+' '+'/'.join(new_list)

###########################################
				
			if "+" in product:
				plus_list=product.split('+')
				product=plus_list[0]+"combo"
				temp_var=' '.join(plus_list[1:])
				new_variant=new_variant+' '+temp_var



###########################################
			
			
			for char in product:
				if char in punctuations:
					product=product.replace(char,' ')
			product=' '.join(product.split())			

			for word in list_bbq:
				if word in product:
					if word=='b b q':
						product=product.replace(word,'bbq')
					else:
						product=product.replace(word,'blt')



			for word in phrase:
					if word in product:
						product=product.replace(word,'')
						new_variant=new_variant+" "+word

			# print product			
			if not flag_7up:
				for num in product.split():
					num_flag=True
					for char in num:
						if not char.isdigit():
							num_flag=False
							break
					if num_flag and num != '65':
						product=product.replace(num,'')
						new_variant=new_variant+" "+num

				for char in product:
					if char.isdigit():
						product=product.replace(char,'')
						new_variant=new_variant+" "+char

				print product
				if '65' in og_product.split():
					product=product+" 65"
					if '65' in new_variant.split():
						new_variant=new_variant.replace('65',"")
				print product			

			temp=""
			for word in product.split():
				if word in quantity:
					new_variant=new_variant+" "+word
				else:
					temp=temp+" "+word

			product=temp
			product=' '.join(product.split())

			
			temp_prod=""
			for item in product.split():
				if len(item) ==1:
					pass
				else:
					temp_prod=temp_prod+" "+item
					


			product=temp_prod
			product=' '.join(product.split())
			masterdish=product
			master_list=masterdish.split()
			index_list=[]
			flag=False
			check_flag=False

			for prepo in prep:
				if prepo in master_list:
					index=master_list.index(prepo)
					index_list.append(index)
					flag=True
			if flag:
				index=sorted(index_list)[0]
				string1=master_list[:index]
				string2=master_list[index+1:]
				len_flag=False
				
				if len(string1) ==1:
					new_master=' '.join(string1)+' '+' '.join(string2)
					len_flag=True
					check_flag=True
				
				if len(string1)<1 and len(string2) >=1:
					new_master=' '.join(string2)
					check_flag=True

				if not len_flag:
					for item_check in prep_check_words:
						temp_string1=' '.join(string1)
						if item_check == temp_string1:
							for word in string2:
								if word in ing:
									new_master=word+" "+' '.join(string1)
									for item in string2:
										if item == word:
											pass
										else:
											new_variant=new_variant+' '+item

									check_flag=True
									break

				if not check_flag:
					new_master=' '.join(string1)
					new_variant=new_variant+' '+' '.join(string2)
				
				if new_master=="" and new_variant !="":
					new_master=new_variant
					new_variant=""		
				
				temp_1=''	
				for word in new_master.split():
					if word in stopwords:
						pass
					else:
						temp_1=temp_1+" "+word 
				new_master=temp_1
				new_master=' '.join(new_master.split())	
				new_master=new_master.strip()	
				
###################################
				for word in remove_phrase:
					if word in new_master:
						new_master=new_master.replace(word," ")
				new_master=' '.join(new_master.split()) 
###################################



				new_row.extend([new_master,new_variant,cuisine,subcuisine,subcat])
				writer.writerow(new_row)

			else:
				
				temp_2=''	
				for word in masterdish.split():
					if word in stopwords:
						pass
					else:
						temp_2=temp_2+" "+word 
				masterdish=temp_2
				masterdish=' '.join(masterdish.split())
				masterdish=masterdish.strip()	


				new_row.extend([masterdish,new_variant,cuisine,subcuisine,subcat])
				writer.writerow(new_row)


		else:
			new=[]
			new.extend([row[0],row[2],row[4],row[5],row[6],row[7],row[8],row[9]])
			# print "n =",new
			writer.writerow(new)
outputfile.close()



freq_prod=[]
counter={}
with open('output.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		word=row[3].strip()
		freq_prod.extend([word])
	# print freq_prod	
	counter=dict(collections.Counter(freq_prod))



outputfile2 = open("output-new.csv","wb")
wr2 = csv.writer(outputfile2)
word_dict={}
prod_dict={}
full_map={}
with open('output.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	wr2.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat','To_be_pinged'])
	next(reader)
	for row in reader:
		# print row
		prod=row[3]
		menu=row[1].lower().strip()
		# print "P =",prod
		
		for item in prod.split():
			if item not in word_dict:
				word_dict[item]=1
			else:
				word_dict[item]+=1

##################################################
		if len(prod.split())==1:
			if prod in stopwords_prod:
				prod=prod	
			else:
				menu=punct(menu,punctuations)
				# classifier_list=[]
				if prod in classifier_menu.keys():
					prod=prod
				else:
					menu_flag=False
					for word in menu.split():
						for k in classifier_menu.keys():
							if word == k:
								prod=prod+" "+classifier_menu[k]
								menu_flag=True
								break
						if menu_flag:
							break	
###################################################


##################
		prod_dict[row[0]+"-->"+prod]=prod #mapping of product with prod+menu
##################
		

		new_row=[]
		new_row=row[:]
		# print "R1 =",row
		new_row.append(prod)
		# print "N =",new_row
#################		
		full_map[row[0]+"-->"+prod]=new_row
#################


		wr2.writerow(new_row)
outputfile2.close()
# print prod_dict
# print "len =",len(prod_dict)

word_list=sorted(word_dict.items(), key=lambda x: (x[1], x[0]))
item_list_all_keys=[]
for item in word_list:
	item_list = list(item)
	item_list_all_keys.append(item_list[0])
# print word_list

for f in range(0,3):
	count=0
	item_dict={}
	for item in item_list_all_keys:
		count+=1
		new_item=""
##################################		
		new_item=difflib.get_close_matches(item,item_list_all_keys[count:],cutoff =0.90)
##################################
		if len(new_item) > 0:
			item_dict[item]=new_item[0]

	for k,v in prod_dict.iteritems():
		for value in v.split():
			if value in item_dict.keys():
				v=v.replace(value,item_dict[value])
			prod_dict[k]=v


# print "len =",len(prod_dict)
# print "prod_dict NEW =",prod_dict
op_file = open("output-new-updated.csv","wb")
wr_file = csv.writer(op_file)

op_file2 = open("output-new-updated-2.csv","wb")
wr_file2 = csv.writer(op_file2)


prod_word_sort={}
counter_dict={}

# print len(prod_dict)
with open('output-new.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	wr_file.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat','To_be_pinged','To_be_pinged_updated'])
	next(reader)	
	for row in reader:
		word_sort=[]
		# print "R =",row
		prod=row[8]
		prod=row[0]+"-->"+prod
		# print "p =",prod
		new_row=row[:]
		new_prod=""

		if prod in prod_dict.keys():
			new_prod=prod_dict[prod]
			# count_freq_prod.append(new_prod)
			# print 1

		if new_prod != "":
			for word in new_prod.split():
				word_sort.append(word)


		# print word_list
		temp=' '.join(sorted(word_sort))
		prod_word_sort[new_prod]=temp ##All prod as key and sorted prod words as values
		# print "temp =",temp
		new_row.append(new_prod)
		# print new_row
		wr_file.writerow(new_row)

		



# print full_map

###################    write below code outside file or inside ????????
wr_file2.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat','prod-1','prod-2','prod-3'])

counter_dict=dict(collections.Counter(prod_word_sort.values()))
# print prod_word_sort
# print counter_dict
temp_list=sorted(counter_dict.items(), key=lambda x: (x[1], x[0]))

store_item=[]
for item in temp_list:
	item=list(item)[0]
	store_item.append(item)

count=0
for word in store_item:
	# print "word =",word
	count+=1
	new_item=""
##################################		
	new_item=difflib.get_close_matches(word,store_item[count:],cutoff =0.90)
##################################
	if len(new_item) > 0:
		for k,v in prod_word_sort.iteritems():
			if v == word:
				for x,y in prod_word_sort.iteritems():
					if y == new_item[0]:
						prod_word_sort[k]=x
							# print "K =",k
							# print "X =",x
# print prod_dict
		
	# print "len =",len(prod_dict)
flag_1=True
final_dict={}
for k,v in prod_dict.iteritems():
	final=""
	for x,y in prod_word_sort.iteritems():
		if v == x:
			intemediate=y
			# print k
			final=x
			new_key=k
			initial_data=full_map[k]
			new_tag=[]
			new_tag.extend(initial_data)
			new_tag.extend([intemediate,final])
			final_dict[new_tag[0]]=new_tag
			flag_1=False
			break

temp_new=sorted(final_dict.items(), key=lambda x: (int(x[0])))
for word in temp_new:
	word=list(word)[1]
	wr_file2.writerow(word)

op_file2.close()



correction_file = csv.reader(open('list_of_words_tense_correction.csv'), delimiter=',', quotechar='"')
correction_list = []
correction_count=0
for row in correction_file:
	correction_count += 1
	if correction_count > 0:
		correction_list.append(row)

op_file3 = open("output-new-updated-3.csv","wb")
wr_file3 = csv.writer(op_file3)


prod_freq_dict={}
count_freq_prod=[]
with open('output-new-updated-2.csv','rb') as csvfile:
	master_file = csv.reader(csvfile)
	wr_file3.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat','prod-1','prod-2','prod-3','prod-4'])
	next(master_file)
	for row in master_file:
		flag=True
		for each_list in correction_list:
			if flag:
				a = row[10].split()
				for n,i in enumerate(a):
					if i == each_list[0]:
						a[n] = each_list[1]
						flag=False
						break
				temp = " ".join(a)


		prod_freq_dict[row[0]]=temp

		new_row=row[:]
		new_row.extend([temp])
		wr_file3.writerow(new_row)

op_file3.close()


op = open("output-new-updated-4.csv","wb")
wr_op = csv.writer(op)
wr_op.writerow(['Count','Menu_Cat','Original_Prod','Clean_Prod','Variant','Cuisine','Subcuisine','Subcat','prod-1','prod-2','prod-3','prod-4','prod-5'])
new_dict=load_db(prod_freq_dict)
with open('output-new-updated-3.csv','rb') as dbfile:
	db_reader = csv.reader(dbfile)
	next(db_reader)
	for row in db_reader:
		# input_dict[row[0]] = row[1]
		if row[0] in new_dict.keys():
			temp=new_dict[row[0]]
			new_r=row[:]
			new_r.append(temp)
		wr_op.writerow(new_r)
op.close()



outputfile3 = open("output-new-updated-5.csv","wb")
wr3 = csv.writer(outputfile3)

unique=[]
with open('output-new-updated-4.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	wr3.writerow(['To_be_pinged'])
	next(reader)
	for row in reader:
		cuisine=row[5]
		prod=row[12]
		if cuisine != "alcoholic beverages":
			unique.append(row[12])

	list1=	list(set(unique))
	for item in list1:
		tag=[]
		tag.extend([item])
		wr3.writerow(tag)

stop = timeit.default_timer()
time_taken = stop - start
print "Total time to run =",time_taken	