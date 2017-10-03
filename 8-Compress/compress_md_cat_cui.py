import csv
import string
import sys
from difflib import SequenceMatcher
# SequenceMatcher(None,str(og),str(og_trans_rev)).ratio()

reload(sys)
sys.setdefaultencoding('utf-8')

def myfun(base,num):
	md = {}
	with open('masterdish_final_pl.csv','rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			if row[base] not in md.keys():
				md[row[base]] = {}
			if row[num] in md[row[base]].keys():
				md[row[base]][row[num]] += 1
			else:
				md[row[base]][row[num]] = 1
	inputfile.close()
	final = []
	for k, v in md.iteritems():
		clist = sorted(md[k].items(), key=lambda x: (-x[1],x[0]))
		klist = []
		vlist = []
		c = ""
		r = 0
		for iset in clist:
			klist.append(list(iset)[0])
			vlist.append(list(iset)[1])
		if len(klist) > 1:
			co = 0
			cou = 0
			num = 0
			for item in klist:
				if item != '':
					c = item
					co = vlist[num]
					break
				num += 1
			num1 = 0
			for item in klist:
				if item == '':
					pass
				else:
					cou += vlist[num1]
				num1 += 1
			if '' in klist:
				r = co/float(cou)
			else:
				r = co/float(cou)
		else:
			c = klist[0]
			r = float(1)
		# print [k,c,r]
		# writer.writerow([k,c,r])
		final.append([k,c,r])
	return final

masterdish_index = 6
cuisine_index = 8
subcuisine_index = 10
subcategory_index = 11

cuisine = myfun(masterdish_index,cuisine_index)
subcuisine = myfun(masterdish_index,subcuisine_index)
subcategory = myfun(masterdish_index,subcategory_index)

main = {}
for entry in cuisine:
	main[entry[0]] = [entry[1],entry[2]]
for entry in subcuisine:
	main[entry[0]].extend([entry[1],entry[2]])
for entry in subcategory:
	main[entry[0]].extend([entry[1],entry[2]])
# print main


outputfile = open("Poland_compress_output.csv","wb")
writer = csv.writer(outputfile)
writer.writerow(['Master dish','Cuisine','Ratio','Subcuisine','Ratio','Subcategory','Ratio'])
with open('masterdish_final_pl.csv','rb') as inputfile:
	reader = csv.reader(inputfile)
	next(reader)
	# for row in reader:
	for k,v in main.iteritems():

		new_row = [k]
		new_row.extend(v)
		# new_row.extend(main[row[masterdish_index]])
		writer.writerow(new_row)
inputfile.close()
outputfile.close()