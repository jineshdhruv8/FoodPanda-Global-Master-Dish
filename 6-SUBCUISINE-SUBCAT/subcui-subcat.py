import csv
import en
import sys
import timeit

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')


def dessert_check(dessert_list,word):
	if word in dessert_list.keys():
		new_subcuisine=dessert_list[word]
		return new_subcuisine
	else:
		return ""		



fruit_list=[]
with open('List of Fruits.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		fruit_list.append(word)

dessert_list={}
with open('dessert _wordlist_new.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[1].lower()
		dessert_list[word]=row[0].lower()


subcat_dict = {}
with open('subcat_list.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	subcat_list=[]
	for row in reader:
		cat = row[0].lower()
		for elem in row[1:]:
			elem=elem.lower().strip()
			subcat_list.append(elem)
			if elem not in subcat_dict:
				subcat_dict.update({elem:cat})

animal_file = csv.reader(open('animal_dish_subcuisine_list.csv'), delimiter=',', quotechar='"')
animal_list = []
for row in animal_file:
	l1 = []
	for item in row:
		if item != "":
			item = en.noun.singular(item.lower())
			l1.append(item)
	animal_list.append(l1)


cooking_method_file = csv.reader(open('cooking_method.csv'), delimiter=',', quotechar='"')
cooking_method_list = []
for row in cooking_method_file:
	l1 = []
	for item in row:
		if item != "":
			item = en.noun.singular(item.lower())
			l1.append(item)
	cooking_method_list.append(l1)	


sub_cuisine_file = csv.reader(open('sub_cuisine_v6.csv'), delimiter=',', quotechar='"')
sub_cuisine_list = []
for row in sub_cuisine_file:
	l1=[]
	for k,item in enumerate(row):
		if item !="":
			if k < 2:
				item = item.lower()
			else:
				item = en.noun.singular(item.lower())
			l1.append(item)
	sub_cuisine_list.append(l1)
# print sub_cuisine_list

f = open('Poland_subcui_subcat_file.csv','w')
writer = csv.writer(f)
writer.writerow(['Count','Menu_Cat_Tran','Prod_Tran','Clean_Prod','Variant','Masterdish','flag','Cuisine','Subcuisine','Subcategory'])
count = 0
with open('Poland-masterdish-output-with-remain.csv','r') as csvfile:
	master_file = csv.reader(csvfile)
	next(master_file)
	for row in master_file:

###########################################################		

#Used for finding Subcategory

		masterdish_list= (row[14].lower().strip()).split()
		masterdish=row[14].lower().strip()
		masterdish_flag=row[15]
		prod_list= (row[2].lower().strip()).split()
		menu_list= (row[1].lower().strip()).split()
		flag=True
		
###########################################################		
		count += 1
		if count > 0:

			new_cuisine = ""
			new_sub_cuisine = ""
			if "alcoholic beverages" not in row[5]:
				c2 = en.noun.singular(row[14].lower()).split()
				c1 = en.noun.singular(row[2].lower()).split()
				c0 = en.noun.singular(row[1].lower()).split()
				flag = True
				for each_list in sub_cuisine_list:
					check_list = each_list[2:]
					for word in check_list:
						if word in c2 or word in c1 or word in c0:
							new_cuisine = each_list[0]
							new_sub_cuisine = each_list[1]
							flag = False
							break
					
					if flag == False:
						break

				if new_sub_cuisine == "":
					c0_new = en.noun.singular(row[14].lower()).split(" ")
					for each_list in animal_list:
						flist = each_list[0].split()
						if set(flist).issubset(set(c0_new)):
							new_sub_cuisine = each_list[1]

				if new_sub_cuisine=="":
					c0_3 = en.noun.singular(row[14].lower()).split(" ")
					for each_list in cooking_method_list:
						if each_list[0] in c0_3:
							new_sub_cuisine = each_list[1].lower()


#############################################

#For finding Subcategory
				subcat=""
				subcat_flag=False
				search_list = masterdish_list + prod_list  
				for word in subcat_list:
					word=word.lower()					
					if set(word.split()).issubset(search_list):
						subcat_flag=True
						subcat=subcat_dict[word]
						flag=False
						# print word
						if subcat=="dessert":
							new_sub_cuisine=dessert_check(dessert_list,word)
							new_cuisine="dessert"
						break

				if flag:

					search_list = menu_list
					for word in subcat_list:
						word=word.lower()
						if set(word.split()).issubset(search_list):
							subcat_flag=True
							subcat=subcat_dict[word]
							flag=False
							if subcat=="dessert":
								new_sub_cuisine=dessert_check(dessert_list,word)
								new_cuisine="dessert"
							break

##############################################
				


########### FRUIT HANDLING
				if new_sub_cuisine =="" and subcat =="":
					search_list_fruit=masterdish_list + prod_list + menu_list
					for word in fruit_list:
						if set(word.split()).issubset(search_list_fruit):
							new_cuisine="western"
							new_sub_cuisine="salad"
							subcat="salad"

###########


				new_row=row[:5]
				new_row.extend([masterdish,masterdish_flag,new_cuisine.lower(),new_sub_cuisine.lower(),subcat])
				writer.writerow(new_row)
			else:

				new_row=row[:5]
				new_row.extend([masterdish,masterdish_flag,row[5],row[6],row[7]])
				writer.writerow(new_row)
f.close()



stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken