import csv
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

cold_list=['ice','iced','cold','frost','chilled','icecream','icecreams','ice-cream','ice-creams']

# other_check_words_non_alco=['ice cream','ice creams','ice-cream','ice-creams']

other_stopwords=['ice cream','ice creams','icecream','icecreams','ice-cream','ice-creams']

punctuations=[',','.','&','\\','\"','-','!','(',')','=',':',';','<','>','?','{','}','[',']','@','#','$','%','^','&','*','+',"'",'"','_','!','~','`','|']

quantity=['v.','big','small','large','medium','can','cans','per','l','L','glass','ly','ml','litre','gram','grams','gm','gms','kg','kgs','cl','pcs','pieces','piece','bottle','bottles']

search = " abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=+_<>?,./:\";\'{}[]\'*\\"

list_7up_cocacola=['7 Up','7 UP','7 up','7 uP','7-Up','7-UP','7-up','7-uP','7up','7UP','7Up','7uP','coca cola','COCA COLA','coca-cola','COCACOLA','cocacola']

cola_list=['cola','coca','coke']

soft_drink=['soft-drink','soft-drinks','soft drink','soft drinks']
# softdrink_list=['pepsi','mirinda','cocacola','thumbs up','coca cola','7up','mirinda','sprite','fanta','limca','coke','twister']

def isnonalpha(char):
	if char.isdigit() or char in punctuations:
		return True
	else:
		return False

def number_cleanup(word):
	cleaned_word = []
	for each_word in word.split():
		if not any(isnonalpha(char) for char in each_word) or (str(each_word) == '555' or str(each_word) == '333' or str(each_word) == '65'):
			if len(each_word)<=1:
				each_word=""
			cleaned_word.append(each_word)				
	return ' '.join(word for word in cleaned_word)


#Dict of non-alcoholic drinks
subcat_dict = {}
subcat_list=[]
with open('non-alcoholic-drinks.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		cat = row[0].lower().strip()
		for elem in row[1:]:
			elem=elem.lower().strip()
			subcat_list.append(elem)
			if len(elem) > 1 and elem not in subcat_dict:
				subcat_dict.update({elem:cat})

#List of ignore words for non-alcoholic drinks
non_alco_ignore=[]
with open('ignore-non-alcoholic.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		non_alco_ignore.append(word)


#List of softdrinks for non-alcoholic drinks
softdrink_list=[]
with open('soft drink.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		softdrink_list.append(word)

#List of waters for non-alcoholic drinks
water_list=[]
with open('water.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		water_list.append(word)

#List of sigular names for non-alcoholic drinks
non_alco_sing={}
with open('non-alco-singular.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		non_alco_sing[word]=row[1]

#List of other check words for non-alcoholic drinks
non_alco_other=[]
with open('nonalco-other-check-words.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		non_alco_other.append(word)


#List of alcoholic drinks
alcohol_name=[]
with open('alcoholic-drinks.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		alcohol_name.append(word)




#singular alcohol drink name
alcohol_singular_name=[]
with open('alcoholic-drinks-singular.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		alcohol_singular_name.append(word)

alco_dict={}
alco_dict = dict(zip(alcohol_name,alcohol_singular_name))




#List of beer for alcoholic drinks
alco_beer=[]
with open('alco-beer-list.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		alco_beer.append(word)





#List of ignore words for alcoholic drinks
alco_ignore=[]
with open('ignore-alcoholic.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		alco_ignore.append(word)




def masterdish_clean(org_prod,classifier,alco_dict,punctuations,quantity,cuisine,subcui,subcat):
	masterdish=org_prod
	variant=""	

	cuisine="alcoholic beverages"	
	master_list=masterdish.lower().split()
	newdish=""
	newdish=masterdish.lower()
	masterdish_flag=False
	for word in masterdish.lower().split():
		if classifier == word:
 			newdish=newdish.replace(word,alco_dict[classifier])
			masterdish_flag=True
	if not masterdish_flag:
		newdish=newdish+" "+alco_dict[classifier]

	#Finding Variant from masterdish
	if '(' in newdish and ')' in newdish:
		index1=newdish.find('(')
		index2=newdish.find(')')
		variant = variant + newdish[(index1+1):index2]
		newdish=newdish.replace(variant," ")
		# print variant

	#Remove punctuation from masterdish
	for char in newdish:
		if char in punctuations:
			if char != '.' and char != '%':
				newdish=newdish.replace(char," ")

	newdish=newdish.strip()		
	list1=newdish.split()
	for word in list1:
		if word != "333" and word != "555": 
			for char in word:
				if char.isdigit():
					variant=variant+" "+word
					newdish=newdish.replace(word,"")
					break
	list2=[]
	list2=newdish.split()
	for word in list2:
		if word in quantity:
			variant=variant+" "+word
			newdish=newdish.replace(word,"")
	
	#Again removing single words from masterdish after above cleaning
	list3=[]
	list3==newdish.split()
	for word in list3:
		if len(word)==1:
			newdish=newdish.replace(word,"")

	list1=newdish.split()
	newdish=' '.join(list1)
	masterdish=newdish	
	alco_flag=True		
	# print 'variant=',variant
	new_list=[]
	new_list.extend([masterdish,variant,cuisine,subcui,subcat])
	return new_list
	# writer.writerow(new_row)

def check_non_alco(search_list,subcat_list,subcat_dict,softdrink_list,non_alco_sing):
	masterdish=""
	variant=""	
	cuisine=""
	subcat=""
	subcui=""
	for word in subcat_list:
		word=word.lower()
		if set(word.split()).issubset(search_list):
			subcat=subcat_dict[word]
			if word =="cola":
				word="coca cola"
			if word in softdrink_list:
				subcui="soft drinks"
			elif word in list_7up_cocacola:
				subcui="soft drinks"
			else:
				subcui=word
				# print subcui
			for word in softdrink_list:	
				if set(word.split()).issubset(search_list):
					subcui="soft drinks"

			if subcui in non_alco_sing.keys():
				subcui= non_alco_sing[subcui]

			#Removes punctuation from entire product
			search_list=' '.join(search_list)	#convert from list to string

			if subcat == "hot beverages":
				for word in cold_list:
					if word in search_list:
						subcat="cold beverages"
			
			for word in soft_drink:
				if word in search_list:
					subcui="soft drinks"
					subcat="cold beverages"


			for char in search_list:
				if char in punctuations:
					search_list=search_list.replace(char," ")
			search_list=' '.join(search_list.split())

			if "cold" in search_list.split():
				subcat="cold beverages"
			elif "hot" in search_list.split():
				subcat="hot beverages"

			cuisine="non-alcoholic beverages"
			alco_flag=True
			non_alco_flag=False
			new_list=[]
			new_list.extend([masterdish,variant,cuisine,subcui,subcat])
			return new_list



def handle_soft_drink_cases(list_7up_cocacola,item,cola_list):
	masterdish=""
	variant=""	
	subcat=""
	subcui=""
	cuisine=""	
	cola_list_flag=True
	for word in list_7up_cocacola:
		if word in item.strip():
			if "7" in word:
				word="7up"
			else:
				word="coca cola"
				
			cuisine="non-alcoholic beverages"
			subcui="soft drinks"
			subcat="cold beverages"
			non_alco_flag=False
			new_list=[]
			new_list.extend([masterdish,variant,cuisine,subcui,subcat])
			cola_list_flag=False
			return new_list

		if cola_list_flag:
			for word in item.strip().split():
				if word in cola_list:
					cuisine="non-alcoholic beverages"
					subcat="cold beverages"
					subcui="soft drinks"
					# new_row.extend([masterdish,variant,cuisine,subcui,subcat])
					# writer.writerow(new_row)
					non_alco_flag=False
					new_list=[]
					new_list.extend([masterdish,variant,cuisine,subcui,subcat])
					return new_list
	blank_list=[]
	return blank_list


# Output File
op = open('output.csv','wb')
writer = csv.writer(op)

#Input File
with open('RU-full-Translation_error.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	
	writer.writerow(['count','Menu-category','Menu-Translated','Product','Product-Translated','Master-Dish','Variant','Cuisine','Sub-Cuisine','Sub-Category'])
	count = 0
	for i,row in enumerate(reader):
		try:
			count+=1
			new_row = row[:]
			prod = row[4].lower().strip()
			menu = row[2].lower().strip()	
			untran_prod=row[4].strip()
			org_prod=prod
			org_menu=menu	
			cuisine=""
			subcat=""
			subcui=""
			variant=""
			masterdish=""
			classifier=""
			alco_flag=False
			

			#Removes punctuation from entire product	
			for char in prod:
				if char in punctuations:
					prod=prod.replace(char," ")
			
			list1=prod.split()
			list2=[]
			flag = False
			temp =True
			alco_ignore_flag=False
			if flag == False:
				new_prod = number_cleanup(prod).strip()
				new_menu = number_cleanup(menu).lower().strip()

				################################################################################
				#######################check for alcoholic beverages############################
				################################################################################

				for alcohol in alcohol_name:
					alcohol=alcohol.lower()
					if alcohol in new_prod.split():
						
						for word in alco_ignore:
							if set(word.split()).issubset(new_prod.split()):
								alco_ignore_flag=True
								break
							if set(word.split()).issubset(new_menu.split()):
								alco_ignore_flag=True
								break
						
						if alco_ignore_flag:
							break
						
						cuisine = 'alcoholic beverages'
						subcui = alco_dict[alcohol]
						classifier=alcohol
						subcat='alcoholic beverages'
						flag = True
						break

					elif alcohol in new_menu.split():
						
						for word in alco_ignore:
							if set(word.split()).issubset(new_prod.split()):
								alco_ignore_flag=True
								break
							if set(word.split()).issubset(new_menu.split()):
								alco_ignore_flag=True
								break
						if alco_ignore_flag:
							break
						cuisine = 'alcoholic beverages'
						subcui = alco_dict[alcohol]
						classifier=alcohol
						subcat='alcoholic beverages'
						flag = True
						break


			#Below code for finding masterdish and variant for alcoholic beverages
			if flag:
				new_list=masterdish_clean(org_prod,classifier,alco_dict,punctuations,quantity,cuisine,subcui,subcat)
				new_row.extend(new_list)
				writer.writerow(new_row)
				alco_flag=True


		# #####################################################################################
		# #######################check for Non-Alcoholic beverages#############################
		# #####################################################################################
			
			non_alco_flag=True
			non_alco_ignore_flag=True
			if not alco_flag: 
				masterdish=""
				variant=""
				prod=row[4].lower().strip()
				menu=row[2].lower().strip()
				
				#Removes punctuation from entire product	
				for char in prod:
					if char in punctuations:
						prod=prod.replace(char," ")
				prod=' '.join(prod.split())

				#Removes punctuation from entire menu	
				for char in menu:
					if char in punctuations:
						menu=menu.replace(char," ")
				menu=' '.join(menu.split())


				#Below code will ignore those rows that have non-alcoholic stopwords
				prod_plus_menu=prod.split()+menu.split()
				for item in prod_plus_menu:
					if item in non_alco_ignore:
						non_alco_ignore_flag=False
						break
				
				#if ignore words are absent then below code will run
				if non_alco_ignore_flag:
					
					#First search in product
					search_list =  prod.split()
					new_list=check_non_alco(search_list,subcat_list,subcat_dict,softdrink_list,non_alco_sing)
					if new_list:
						new_row.extend(new_list)
						# print "N =",new_list
						writer.writerow(new_row)
						non_alco_flag=False
						cuisine="non-alcoholic beverages"


					flag1=True
					if non_alco_flag:
						temp_prod=prod.split()+menu.split()
						for word in temp_prod:
							if word in softdrink_list:

								cuisine="non-alcoholic beverages"
								subcat="cold beverages"
								subcui="soft drinks"
								flag1=False
								non_alco_flag=False
								new_row.extend([masterdish,variant,cuisine,subcui,subcat])
								writer.writerow(new_row)
								break
							elif word in water_list:
								cuisine="non-alcoholic beverages"
								subcat="cold beverages"
								subcui="other beverages"
								flag1=False
								non_alco_flag=False
								new_row.extend([masterdish,variant,cuisine,subcui,subcat])
								writer.writerow(new_row)
								break

						

						if flag1:
							for word in softdrink_list:
								if set(word.split()).issubset(temp_prod):
									# print "1"
									# print "temp_prod =",temp_prod
									cuisine="non-alcoholic beverages"
									subcat="cold beverages"
									subcui="soft drinks"
									flag1=False
									non_alco_flag=False
									new_row.extend([masterdish,variant,cuisine,subcui,subcat])
									writer.writerow(new_row)
									break

							if flag1:

								for word in water_list:
									if set(word.split()).issubset(temp_prod):
										cuisine="non-alcoholic beverages"
										subcat="cold beverages"
										subcui="other beverages"
										flag1=False
										non_alco_flag=False
										new_row.extend([masterdish,variant,cuisine,subcui,subcat])
										writer.writerow(new_row)
										break


					#Below code for to handle cases like 7 Up, 7 UP,etc. in product
					if non_alco_flag:
						check_prod=prod
						output_list=handle_soft_drink_cases(list_7up_cocacola,check_prod,cola_list)
						if output_list:
							non_alco_flag=False
							cuisine="non-alcoholic beverages"
							new_row.extend(output_list)
							writer.writerow(new_row)

					if non_alco_flag:

						#search in menu
						search_list =menu.split()
						new_list=check_non_alco(search_list,subcat_list,subcat_dict,softdrink_list,non_alco_sing)
						if new_list:
							new_row.extend(new_list)
							writer.writerow(new_row)
							non_alco_flag=False
							cuisine="non-alcoholic beverages"
							

						#Below code for to handle cases like 7 Up, 7 UP,etc. in menu
						if non_alco_flag:
							check_menu=menu
							output_list=handle_soft_drink_cases(list_7up_cocacola,check_menu,cola_list)
							if output_list:
								cuisine="non-alcoholic beverages"
								non_alco_flag=False
								new_row.extend(output_list)
								writer.writerow(new_row)

				checklist=['soft-drink','soft-drinks','soft drink','soft drinks']
				drink_flag=False
				non_alco_other_flag=True
				beer_flag=False
				other_stopwords_flag=True
				if non_alco_flag and non_alco_ignore_flag:
					# print "123"

					# prod=row[4].lower().strip()
					# menu=row[2].lower().strip()
					
					prod_menu=prod+" "+menu
					for word in other_stopwords:
						if word in prod_menu:
							other_stopwords_flag=False
							break




					if other_stopwords_flag:
						for name in alco_beer:
							if set(name.split()).issubset(prod.lower().split()):
								beer_flag=True
								cuisine="alcoholic beverages"
								subcui="beer"
								subcat="alcoholic beverages"

								new_list=masterdish_clean(org_prod,'beer',alco_dict,punctuations,quantity,cuisine,subcui,subcat)
								# print "N =",new_list
								new_row.extend([new_list[0],new_list[1],cuisine,subcui,subcat])
								writer.writerow(new_row)

								break

						if not beer_flag:		
							for word in non_alco_other:
								if non_alco_other_flag:
									if word == menu:

										#Removes punctuation from entire product	
										for char in prod:
											if char in punctuations:
												prod=prod.replace(char," ")
										prod=' '.join(prod.split())


										
										for item in checklist:
											if item in prod:
												cuisine="non-alcoholic beverages"
												subcui="soft drinks"
												subcat="cold beverages"
												new_row.extend([masterdish,variant,cuisine,subcui,subcat])
												writer.writerow(new_row)
												non_alco_other_flag=False
												drink_flag=True
												break

										if not drink_flag:
											# print "prod =",prod
											cuisine="non-alcoholic beverages"
											subcui="other beverages"
											if 'hot' in prod.split():
												subcat="hot beverages"
											elif 'cold' in prod.split():
												subcat='cold beverages'
											elif 'cold' in menu.split():
												subcat="cold beverages"
											elif 'hot' in menu.split():
												subcat='hot beverages'
											else:
												subcat='cold beverages'

											new_row.extend([masterdish,variant,cuisine,subcui,subcat])
											writer.writerow(new_row)

			if cuisine != "alcoholic beverages" and cuisine != "non-alcoholic beverages":
				new_row.extend([masterdish,variant,cuisine,subcui,subcat])
				writer.writerow(new_row)
		except Exception as e:
			print e
			print "error =",row[0]


		