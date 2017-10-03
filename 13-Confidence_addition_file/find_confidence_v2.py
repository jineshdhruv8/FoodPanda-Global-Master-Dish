import csv
import en
import sys
import timeit

start = timeit.default_timer()
reload(sys)
sys.setdefaultencoding('utf-8')


def stat(value,stat_dict):
	if value == 1:
		stat_dict['r1']+=1
	elif value < 1 and value >=0.80:
		stat_dict['r2']+=1
	elif value <0.80 and value >=0.60:
		stat_dict['r3']+=1
	elif value <0.60 and value >=0.40:
		stat_dict['r4']+=1
	elif value <0.40 and value >=0.20:
		stat_dict['r5']+=1
	elif value <0.20 and value >0:
		stat_dict['r6']+=1
	return stat_dict

stat_dict_cuisine={'r1':0,'r2':0,'r3':0,'r4':0,'r5':0,'r6':0}
stat_dict_subcuisine={'r1':0,'r2':0,'r3':0,'r4':0,'r5':0,'r6':0}
stat_dict_subcat={'r1':0,'r2':0,'r3':0,'r4':0,'r5':0,'r6':0}
md_dict={}
with open('input.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		md=row[6]
		cuisine=row[8]
		subcuisine=row[10]
		subcat=row[12]
		if md not in md_dict.keys():
			all_list=[]
			cuisine_dict={}
			subcuisine_dict={}
			subcat_dict={}
			if cuisine !="":
				cuisine_dict[cuisine]=1
			if subcuisine != "":
				subcuisine_dict[subcuisine]=1
			if subcat != "":
				subcat_dict[subcat]=1
			all_list.extend([cuisine_dict,subcuisine_dict,subcat_dict])
			md_dict[md]=all_list
		else:
			all_list=[]
			cuisine_dict={}
			subcuisine_dict={}
			subcat_dict={}
			all_list=md_dict[md]
			cuisine_dict=all_list[0]
			subcuisine_dict=all_list[1]
			subcat_dict=all_list[2]
			if cuisine_dict:
				if cuisine != "":
					if cuisine not in cuisine_dict:
						cuisine_dict[cuisine]=1
					else:
						cuisine_dict[cuisine]+=1
			elif cuisine !="":
				if cuisine not in cuisine_dict:
						cuisine_dict[cuisine]=1	


			if subcuisine_dict:
				if subcuisine != "":
					if subcuisine not in subcuisine_dict:
						subcuisine_dict[subcuisine]=1
					else:
						subcuisine_dict[subcuisine]+=1
			elif subcuisine !="":
				if subcuisine not in subcuisine_dict:
						subcuisine_dict[subcuisine]=1	

			if subcat_dict:
				if subcat != "":
					if subcat not in subcat_dict:
						subcat_dict[subcat]=1
					else:
						subcat_dict[subcat]+=1
			elif subcat !="":
				if subcat not in subcat_dict:
						subcat_dict[subcat]=1

inputfile.close()	

# print md_dict

outputfile = open("output.csv","wb")
writer = csv.writer(outputfile)
writer.writerow(["Count","Original_menu","Oriignal_prod","Menu_Cat_Tran","Prod_Tran","Variant","Masterdish","flag","Cuisine","cuisine_flag","cuisine_conf","Subcuisine","subcuisine_flag",'subcui_conf',"Subcategory","subcategory_flag",'subcat_conf',"Ingredient"])

op2=open("stat.csv","wb")
wr2=csv.writer(op2)
wr2.writerow(['Factor','confidence(100%)','confidence(80-100)','confidence(60-80)','confidence(40-60)','confidence(20-40)','confidence(0-20)','Blank %'])
total=0
cuisine_blank=0
subcuisine_blank=0
subcat_blank=0
with open('input.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	for row in reader:
		total+=1
		new_row=row[:10]
		md=row[6]
		cuisine=row[8]
		subcuisine=row[10]
		subcat=row[12]
		if cuisine == "":
			cuisine_blank+=1
		if subcuisine == "":
			subcuisine_blank+=1
		if subcat == "":
			subcat_blank+=1
		c1=0
		c2=0
		c3=0
		cuisine_count=0
		subcuisine_count=0
		subcat_count=0
		cuisine_confidence=0
		subcuisine_confidence=0
		subcat_confidence=0
		if md in md_dict.keys():
			# print row
			all_list=md_dict[md]
			cuisine_dict=all_list[0]
			subcuisine_dict=all_list[1]
			subcat_dict=all_list[2]
			# print cuisine
			for word in cuisine_dict.keys():			
				cuisine_count+=cuisine_dict[word]
			if cuisine in cuisine_dict.keys():
				c1=cuisine_dict[cuisine]
				# print c1
			for word in subcuisine_dict.keys():
				subcuisine_count+=subcuisine_dict[word]
			if subcuisine in subcuisine_dict.keys():
				c2=subcuisine_dict[subcuisine]
			for word in subcat_dict.keys():
				subcat_count+=subcat_dict[word]
			if subcat in subcat_dict.keys():
				c3=subcat_dict[subcat]
			
			if cuisine_count != 0:
				cuisine_confidence=float(c1)/cuisine_count
			if subcuisine_count != 0:
				subcuisine_confidence=float(c2)/subcuisine_count
			if subcat_count !=0:
				subcat_confidence=float(c3)/subcat_count

			new_row.append(cuisine_confidence)
			new_row.extend(row[10:12])
			new_row.append(subcuisine_confidence)
			new_row.extend(row[12:14])
			new_row.append(subcat_confidence)
			new_row.extend(row[14:])
			writer.writerow(new_row)
			
			# print stat_dict_cuisine

			stat_dict_cuisine=stat(cuisine_confidence,stat_dict_cuisine)
			stat_dict_subcuisine=stat(subcuisine_confidence,stat_dict_subcuisine)
			stat_dict_subcat=stat(subcat_confidence,stat_dict_subcat)

new1=[]
new2=[]
new3=[]
new1.extend(['cuisine',(float(stat_dict_cuisine["r1"])/total)*100,(float(stat_dict_cuisine["r2"])/total)*100,(float(stat_dict_cuisine["r3"])/total)*100,(float(stat_dict_cuisine["r4"])/total)*100,(float(stat_dict_cuisine["r5"])/total)*100,(float(stat_dict_cuisine["r6"])/total)*100,(float(cuisine_blank)/total)*100])
new2.extend(['Subcuisine',(float(stat_dict_subcuisine["r1"])/total)*100,(float(stat_dict_subcuisine["r2"])/total)*100,(float(stat_dict_subcuisine["r3"])/total)*100,(float(stat_dict_subcuisine["r4"])/total)*100,(float(stat_dict_subcuisine["r5"])/total)*100,(float(stat_dict_subcuisine["r6"])/total)*100,(float(subcuisine_blank)/total)*100])
new3.extend(['Subcat',(float(stat_dict_subcat["r1"])/total)*100,(float(stat_dict_subcat["r2"])/total)*100,(float(stat_dict_subcat["r3"])/total)*100,(float(stat_dict_subcat["r4"])/total)*100,(float(stat_dict_subcat["r5"])/total)*100,(float(stat_dict_subcat["r6"])/total)*100,(float(subcat_blank)/total)*100])
# print "Confidence_Cuisine(100%)=",(float(stat_dict_cuisine["r1"])/total)*100
# print "Confidence_Cuisine(100%)=",(float(stat_dict_cuisine["r2"])/total)*100
# print "Confidence_Cuisine(100%)=",(float(stat_dict_cuisine["r3"])/total)*100
# print "Confidence_Cuisine(100%)=",(float(stat_dict_cuisine["r4"])/total)*100
# print total
wr2.writerow(new1)
wr2.writerow(new2)
wr2.writerow(new3)
stop = timeit.default_timer()
time_taken = stop - start
print " Time taken is ", time_taken