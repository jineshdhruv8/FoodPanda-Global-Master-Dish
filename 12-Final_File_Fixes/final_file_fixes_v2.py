import csv
import en
import sys
import timeit

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')


other_checklist=[]
with open('dessert _checklist.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		other_checklist.append(word)

checklist_subcui_non_alco=[]
with open('checklist_subcui_non_alco.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		checklist_subcui_non_alco.append(word)

subcui_checklist={}
with open('subcuisine_checklist.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		subcui_checklist[word]=row[1].lower().strip()


word_map_list={}
with open('word_map_list.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	for row in reader:
		word = row[0].lower().strip()
		word_map_list[word]=row[1:]


# initial_file={}
initial_file_list=[]
with open('global_master_menu_pl_23_with_count.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		count = row[0].lower().strip()
		menu=row[4]
		prod=row[5]
		t=[]
		t.extend([count,menu,prod])
		initial_file_list.append(t)
		# print initial_file_list
		# break
		# temp=[]
		# temp.extend([menu,prod])
		# initial_file[count]=temp



outputfile=open("Final_file_after_all_fixes_reference_pl.csv",'wb')
wr=csv.writer(outputfile)
wr.writerow(["Count","vendor_id","Menu_Cat_Tran","Prod_Tran","Clean_Prod","Variant","Masterdish","flag","Cuisine","cuisine_flag","Subcuisine","subcuisine_flag","Subcategory","subcategory_flag","Ingredient"])

outputfile2=open("Final_file_after_all_fixes_pl.csv",'wb')
wr2=csv.writer(outputfile2)
wr2.writerow(["Count","Original_menu","Oriignal_prod","Menu_Cat_Tran","Prod_Tran","Variant","Masterdish","flag","Cuisine","cuisine_flag","Subcuisine","subcuisine_flag","Subcategory","subcategory_flag","Ingredient"])

with open('complete_ing_file_pl.csv','rb') as csvfile:
	reader=csv.reader(csvfile)
	next(reader)
	for row in reader:
		subcui_flag=row[11]
		subcuisine=row[10]
		cuisine=row[8]
		cuisine_flag=row[9]
		subcat=row[12]
		subcat_flag=row[13]
		md=row[6]
		md_flag=row[7]
		new_row=row[:6]
		ing_list=row[14:]
		length=len(ing_list)
		if length==0:
			ing_list.extend(['','',''])
		elif length==1:
			ing_list.extend(['',''])
		elif length==2:
			ing_list.extend([''])

		check_md=md.split()
		if len(check_md) >=1:
			if 'and' ==check_md[0]:
				check_md.remove('and')
			if 'and' ==check_md[len(check_md)-1]:
				check_md.remove('and')
			md=' '.join(check_md)

		if subcuisine=="desserts":
			subcuisine="dessert"
		if subcuisine=="soups":
			subcuisine="soup"
		if subcuisine=="noodles" or subcuisine=="noodle":
			subcuisine="noodle dish"


			
		###Fix 1
		if subcat=="salad":
			if cuisine =="":
				cuisine="western"
				cuisine_flag=6
			if subcuisine!="salad":
				subcuisine="salad"
				subcui_flag=3

		###Fix 2
		if subcuisine=="american dish":
			if cuisine!="american":
				cuisine="american"
				cuisine_flag=6

		###Fix 3
		if subcuisine=="west indian dish" or subcuisine=="north indian dish" or subcuisine=="south indian dish" or subcuisine=="east indian dish":
			if cuisine != "indian":	
				cuisine="indian"
				cuisine_flag=6

		###Fix 4
		if subcat=="cold beverages" or subcat=="hot beverages":
			if cuisine != "non-alcoholic beverages":
				cuisine="non-alcoholic beverages"
				cuisine_flag=6
			if subcuisine not in checklist_subcui_non_alco:
				subcuisine="other beverages"
				subcui_flag=3

		###Fix 5
		if cuisine=="non-alcoholic beverages":
			if subcat!="cold beverages" and subcat!="hot beverages":
				subcat="cold beverages"
				subcat_flag=3
			if subcuisine not in checklist_subcui_non_alco:
				subcuisine="other beverages"
				subcui_flag=3

		###Fix 6
		if subcat=="bread" and subcuisine=="":
			subcuisine="other bread"
			subcui_flag=3

		###Fix 7
		if subcuisine=="main course" or subcuisine=="fast food" or subcuisine == "snack" or subcuisine =="snacks":
			if subcat!=subcuisine:
				subcat=subcuisine
				subcat_flag=3

		###Fix 8
		if cuisine=="dessert":
			if subcat!="dessert":
				subcat="dessert"
				subcat_flag=3
			if subcuisine not in other_checklist:
				if subcuisine!="dessert":
					subcuisine='dessert'
					subcui_flag=3

		###Fix 9
		if subcat=="dessert" and cuisine !="dessert" and subcuisine in subcui_checklist.keys():
			subcat=subcui_checklist[subcuisine]
			subcat_flag=3


		###Fix 10
		if subcuisine=="dessert" and int(subcui_flag)==1:
			if subcat != "dessert":
				subcat="dessert"
				subcat_flag=3

		if subcuisine=="dessert" and int(subcui_flag)==2:
			if subcat != "dessert":
				subcuisine=""
				subcui_flag=""



		###Fix 11
		if "fries" in md.split() and subcuisine=="":
			if subcuisine!="american dish":
				subcuisine="american dish"
				subcui_flag=3
			if cuisine!="american":
				cuisine="american"
				cuisine_flag=6
			if subcat!="fastfood":
				subcat="fastfood"
				subcat_flag=3

		###Fix 12
		for word in word_map_list:			
			if set(word.split()).issubset(md.split()):
				temp1=word_map_list[word][0]
				temp2=word_map_list[word][1]
				temp3=word_map_list[word][2]
				if cuisine != temp1:
					cuisine=temp1
					cuisine_flag=6
				if subcuisine != temp2:
					subcuisine=temp2
					subcui_flag=3
				if subcat!=temp3:
					subcat=temp3
					subcat_flag=3
				break




		if cuisine == "dessert":
			ing_list=[]
			ing_list.extend(['','',''])

		if cuisine =="non-alcoholic beverages" and subcuisine != 'juice' and subcuisine != 'shake' and subcuisine != 'smoothie' and subcuisine != 'squash':
			ing_list=[]
			ing_list.extend(['','',''])


		if cuisine !="" and subcuisine=="" and cuisine!='dessert' and cuisine!='non-alcoholic beverages' and cuisine!='alcoholic beverages':
			subcuisine="other "+cuisine+" dish"
			subcui_flag=3

		if cuisine=="":
			cuisine_flag=""
		if subcuisine=="":
			subcui_flag=""
		if subcat=="":
			subcat_flag=""

		temp_row=[]
		temp_row=new_row[:]
		new_row.extend([md,md_flag,cuisine,cuisine_flag,subcuisine,subcui_flag,subcat,subcat_flag])
		new_row.extend(ing_list)
		wr.writerow(new_row)

############################################################################
		if cuisine_flag=="1" or cuisine_flag=="2" or cuisine_flag=='3' or cuisine_flag=="4":
			cuisine_flag="0"
		if cuisine_flag=="5" or cuisine_flag==6:
			cuisine_flag="1"
		if subcui_flag=="1":
			subcui_flag="0"
		if subcui_flag=="2" or subcui_flag==3:
			subcui_flag="1"
		if subcat_flag=="1":
			subcat_flag="0"
		if subcat_flag=="2" or subcat_flag==3:
			subcat_flag="1"
		if md_flag=="0" or md_flag=="2" or md_flag=="0_5" or md_flag=="2_5" or md_flag=="3_0":
			md_flag="0"
		if md_flag=="3" or  md_flag=="3_5" or md_flag=="4" or md_flag=="4_5":
			md_flag="1"

		temp_row.extend([md,md_flag,cuisine,cuisine_flag,subcuisine,subcui_flag,subcat,subcat_flag])
		temp_row.extend(ing_list)
		temp_row.pop(1)
		temp_row.pop(3)
		new_temp=temp_row[:1]
		c=int(temp_row[0])-1
		t1=[]

		t1=initial_file_list[c][1:]
		# print t1
		if temp_row[0]==initial_file_list[c][0]:
			new_temp.extend(t1)
		else:
			new_temp.extend(['',''])
			print row
			break
		# if temp_row[0] in initial_file.keys():
		# 	new_temp.extend(initial_file[temp_row[0]])
		# else:
		# 	new_temp.extend(['',''])
		new_temp.extend(temp_row[1:])

		wr2.writerow(new_temp)




stop = timeit.default_timer()

time_taken = stop - start
print " Time taken is ", time_taken