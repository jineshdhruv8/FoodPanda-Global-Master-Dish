import csv
import json
import sys
import string
import difflib
from nltk.util import ngrams
import requests
import ast
from collections import OrderedDict
import timeit

reload(sys)
sys.setdefaultencoding('utf-8')

def load_db(database_filename):
	md_db_dict = {}
	with open(database_filename,'rb') as dbfile:
		db_reader = csv.reader(dbfile)
		next(db_reader)
		for row in db_reader:
			md_db_dict[row[0]] = int(row[1])
	return md_db_dict

def get_sorted_list(md_db_dict):
	md_list = []
	for k,v in md_db_dict.iteritems():
		md_list.append([k,int(len(k.split())),int(v)])
	sorted_list = sorted(md_list,key=lambda x:(-x[1],-x[2],x[0]))
	return sorted_list

def load_check_words(check_words_filename):
	check_word_list = []
	with open(check_words_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			word = row[0].lower().strip()
			check_word_list.append(word)
	return check_word_list

def load_cooking_list(cooking_words_filename):
	cooking_list = []
	with open(cooking_words_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			cooking_list.append(row[0])
	return cooking_list

def ngramming(product,i,cooking_list):
	firefox_url = "http://suggestqueries.google.com/complete/search?output=firefox&client=firefox&hl=en-US&q="
	ngram_list = ngrams(product.split(),i)
	output = []
	if ngram_list:
		for elem in ngram_list:
			query = ' '.join(word for word in elem)
			if set(query.split()).issubset(cooking_list):
				continue
			fquery = query.split()[0]
			lquery = query.split()[(len(query.split())-1)]
			if fquery == 'and' or lquery == 'and':
				continue
			query = query+" "+"recipe"
			
			try:
				firefox_output = requests.get(firefox_url + query).content
				firefox_output = ast.literal_eval(firefox_output)
				if firefox_output[1]:
					try:
						if 'recipe' in firefox_output[0]: firefox_output[0] = firefox_output[0].replace(' recipe','')
						
						for i,word in enumerate(firefox_output[1]):
							if 'recipes' in word:
								word = word.replace(' recipes','')
							elif 'recipe' in word:
								word = word.replace(' recipe','')
							firefox_output[1][i]=word

						new_dish = difflib.get_close_matches(firefox_output[0],firefox_output[1])[0]
						if len(new_dish.split()) == len(query.split())-1:
							output.append([' '.join(elem),new_dish])
					except IndexError:
						pass
			except:
				pass
	return output

def google_ping(dish,check_word_list,cooking_list):
	product = dish.lower().strip()
	masterdish=""
	for i in reversed(range(2,5)):
		ngrams_output = ngramming(product,i,cooking_list)
		if len(ngrams_output)>0:
			if len(ngrams_output)==1:
				return ngrams_output[0][1]
			else:
				for k in range(0,len(ngrams_output)):
					for item in check_word_list:
						if item in ngrams_output[k][1].split():
							return ngrams_output[k][1]
				return ngrams_output[0][1]
	return ""

def find_md(md_db_wc_freq,check_word_list,cooking_list,unique_masterdish):
	md_db = []
	for ilist in md_db_wc_freq:
		md_db.append(ilist[0])
	md_sorted_dict = {}
	for md in md_db:
		md_sorted_dict[' '.join(sorted(md.split()))] = md
	final = []
	count = 0
	for row in unique_masterdish:
		count += 1
		print count
		# print row
		dish = row[0]
		new_dish_list = difflib.get_close_matches(' '.join(sorted(dish.split())),md_sorted_dict.keys(),cutoff=0.95)
		if len(new_dish_list)>0:
			new_dish = md_sorted_dict[new_dish_list[0]]
			final.append([dish,new_dish,0])
			continue
		else:
			freq = int(row[1])
			threshold = 10000
			if freq > threshold:
				final.append([dish,dish,1])
				continue
			else:
				new_dish = ""
				new_dish_flag = False
				for md in md_db:
					if set(md.split()).issubset(dish.split()):
						new_dish = md
						new_dish_flag = True
						break
				if new_dish_flag:
					final.append([dish,new_dish,2])
				else:
					ping_result = google_ping(dish,check_word_list,cooking_list).split()
					if len(ping_result) > 0:
						if ping_result[0] == 'and':
							ping_result = ping_result[1:]
						if ping_result[(len(ping_result)-1)] == 'and':
							ping_result = ping_result[:(len(ping_result)-1)]
						final.append([dish,' '.join(ping_result),3])
					else:
						final.append([dish,'',4])
					# final.append([dish,"",3])
	return final

def find_unique(original_filename,original_file_md_index,original_file_cuisine_index):
	unique_md = {}
	unique_md_list = []
	with open(original_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			if row[original_file_cuisine_index] == "alcoholic beverages":
				continue
			udish = row[original_file_md_index]
			if udish in unique_md.keys():
				unique_md[udish] += 1
			else:
				unique_md[udish] = 1
		inputfile.close()
	for k,v in unique_md.iteritems():
		unique_md_list.append([k,v])
	# unique_md_list = unique_md_list[:51]
	return unique_md_list

def remove_empty(final_masterdish):
	for row in final_masterdish:
		if row[1] == "":
			row[1] = row[0]
			row[2] = 4
	return final_masterdish

def subcat_addition(final_masterdish,subcat_add_single_filename,subcat_add_multi_filename):
	subcat_add_single = []
	with open(subcat_add_single_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			subcat_add_single.append([row[0],row[1]])
	subcat_add_multi = []
	with open(subcat_add_multi_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			subcat_add_multi.append([row[0],row[1]])
	for each_dish_row in final_masterdish:
		# if each_dish_row[2] != 3:
		# 	continue
		db_check = ""
		db_check = each_dish_row[1]
		temp_rem_list = []
		temp_rem_flag = True
		for each_entry_multi in subcat_add_multi:
			if each_entry_multi[0] in each_dish_row[1].split() or each_entry_multi[0] in each_dish_row[0].split():
				# print "in multi "
				temp_rem_list.append(each_entry_multi[1])
				if each_entry_multi[0] in each_dish_row[1].split():
					nl = []
					for n,i in enumerate(each_dish_row[1].split()):
						if n != each_dish_row[1].split().index(each_entry_multi[0]):
							nl.append(i)
					each_dish_row[1] = ' '.join(nl)
		single_flag = True
		for each_entry in subcat_add_single:
			if len(each_entry[0].split()) == 1:
				find_str_list1 = each_dish_row[1].split()
				if each_entry[0] in find_str_list1:
					find_str_list1[find_str_list1.index(each_entry[0])] = each_entry[1]
					each_dish_row[1] = ' '.join(find_str_list1)
					temp_rem_flag = False
					single_flag = False
					break
			else:
				ngram_list1 = ngrams(each_dish_row[1].split(),len(each_entry[0]))
				if each_entry[0] in ngram_list1:
					each_dish_row[1] = each_dish_row[1].replace(each_entry[0],each_entry[1])
					temp_rem_flag = False
					single_flag = False
					break
		if single_flag:
			# print "single_flag"
			for each_entry in subcat_add_single:
				if len(each_entry[0].split()) == 1:
					find_str_list2 = each_dish_row[0].split()
					# print "LIST =",find_str_list2
					if each_entry[0] in find_str_list2:
						# print each_entry[0]
							
						each_dish_row[1] = each_dish_row[1]+' '+each_entry[1]
						temp_rem_flag = False
						break
				else:
					ngram_list2 = ngrams(each_dish_row[1].split(),len(each_entry[0].split()))
					if each_entry[0] in ngram_list2:
						each_dish_row[1] = each_dish_row[1]+' '+each_entry[1]
						temp_rem_flag = False
						break
		if temp_rem_flag and len(temp_rem_list) > 0:
			temp_rem_list = list(OrderedDict.fromkeys(temp_rem_list))
			each_dish_row[1] = each_dish_row[1]+' '+' '.join(temp_rem_list)
		each_dish_row[1] = each_dish_row[1].strip()
		each_dish_row[1] = ' '.join(list(OrderedDict.fromkeys(each_dish_row[1].split())))
		each_dish_row[1] = each_dish_row[1].strip()
		if db_check.strip() != each_dish_row[1]:
			each_dish_row[2] = str(each_dish_row[2]) + "_5"
	return final_masterdish

def map_to_original(final_masterdish,original_filename,original_file_md_index):
	full_masterdish = []
	with open(original_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		next(reader)
		for row in reader:
			new_row = row[:]
			new_row_flag = True
			for entry in final_masterdish:
				if row[original_file_md_index] == entry[0]:
					new_row.extend(entry[1:])
					new_row_flag = False
			if new_row_flag:
				new_row.extend(['',''])
			full_masterdish.append(new_row)
	return full_masterdish

def word_cleaning(final_masterdish):
	word_count = {}
	for row in final_masterdish:
		row_list = row[(len(row)-2)].split()
		for word in row_list:
			if word in word_count.keys():
				word_count[word] += 1
			else:
				word_count[word] = 1
	word_list = sorted(word_count.items(),key=lambda x:(-x[1],x[0]))
	change_list = []
	w_count = 0
	for word_entry in word_list:
		w_count += 1
		match = difflib.get_close_matches(list(word_entry)[0],word_list[w_count:],cutoff=0.95)
		if len(match) > 0:
			change_list.append([list(word_entry)[0],match[0]])
	# print change_list
	for i in range(0,3):
		for entry in change_list:
			for row in final_masterdish:
				if row[(len(row)-1)] == 3 or row[(len(row)-1)] == "3" or row[(len(row)-1)] == "3_5" or row[(len(row)-1)] == "":
					dl = row[(len(row)-2)].split()
					new_dl = ""
					if entry[0] in dl:
						dl[dl.index(entry[0])] = entry[1]
						new_dl = ' '.join(dl)
					else:
						new_dl = ' '.join(dl)
					row[(len(row)-2)] = new_dl
	return final_masterdish

def string_cleaning(final_cleaned_masterdish):
	md_freq = {}
	for row in final_cleaned_masterdish:
		if row[(len(row)-2)] in md_freq.keys():
			md_freq[row[(len(row)-2)]] += 1
		else:
			md_freq[row[(len(row)-2)]] = 1
	string_list = sorted(md_freq.items(),key=lambda x:(-x[1],x[0]))
	string_change_list = []
	s_count = 0
	for string_entry in string_list:
		s_count += 1
		for m_string_entry in string_list[s_count:]:
			match = difflib.get_close_matches(list(string_entry)[0],[list(m_string_entry)[0]],cutoff=0.95)
			if len(match) > 0:
				string_change_list.append([list(string_entry)[0],match[0]])
				break
	# print string_change_list
	for entry in string_change_list:
		for row in final_cleaned_masterdish:
			if row[(len(row)-1)] == 3 or row[(len(row)-1)] == "3" or row[(len(row)-1)] == "3_5" or row[(len(row)-1)] == "":
				if entry[0] == row[(len(row)-2)]:
					row[(len(row)-2)] = entry[1]
	return final_cleaned_masterdish

def clean_tense(final_cleaned_masterdish):
	correction_file = csv.reader(open('list_of_words_tense_correction.csv'), delimiter=',', quotechar='"')
	correction_list = []
	correction_count = 0
	for row in correction_file:
		correction_count += 1
		if correction_count > 0:
			correction_list.append(row)
	for row in final_cleaned_masterdish:
		for each_list in correction_list:
			a = row[(len(row)-2)].split()
			for n,i in enumerate(a):
				if i == each_list[0]:
					a[n] = each_list[1]
			row[(len(row)-2)] = " ".join(a)
	return final_cleaned_masterdish

def match_to_db(final_cleaned_masterdish,md_db_wc_freq,original_file_md_index,original_file_cuisine_index):
	for row in final_cleaned_masterdish:
		for md in md_db_wc_freq:
			if row[(len(row)-1)] == 3 or row[(len(row)-1)] == "3" or row[(len(row)-1)] == "3_5":
				match = difflib.get_close_matches(' '.join(sorted(row[(len(row)-2)].split())),[' '.join(sorted(md[0].split()))],cutoff=0.95)
				if len(match) > 0:
					row[(len(row)-2)] = md[0]
					row[(len(row)-1)] = "3_0"
					break
		if row[original_file_cuisine_index] == 'alcoholic beverages':
			row[(len(row)-2)] = row[original_file_md_index]
	return final_cleaned_masterdish

def update_md_db(final_file,new_md_db_freq,add_to_checklist,original_file_subcuisine_index):
	for row in final_file:
		# print row
		if row[(len(row)-1)] == 0 or row[(len(row)-1)] == "0" or row[(len(row)-1)] == 2 or row[(len(row)-1)] == "2" or row[(len(row)-1)] == "3_0":
			if row[(len(row)-2)] in new_md_db_freq.keys():	
				new_md_db_freq[row[(len(row)-2)]] += 1
			else:
				if row[original_file_subcuisine_index] == "wine" or row[original_file_subcuisine_index] == "juice" or row[original_file_subcuisine_index] == "shake" or row[original_file_subcuisine_index] == "smoothie":
					continue
				if row[(len(row)-2)] in add_to_checklist.keys():
					add_to_checklist[row[(len(row)-2)]] += 1
				else:
					add_to_checklist[row[(len(row)-2)]] = 1
		else:
			if row[original_file_subcuisine_index] == "wine" or row[original_file_subcuisine_index] == "juice" or row[original_file_subcuisine_index] == "shake" or row[original_file_subcuisine_index] == "smoothie":
				continue
			if row[(len(row)-2)] in add_to_checklist.keys():
				add_to_checklist[row[(len(row)-2)]] += 1
			else:
				add_to_checklist[row[(len(row)-2)]] = 1
	return [new_md_db_freq,add_to_checklist]

def write_output(final_masterdish,original_filename,output_filename):
	header_list = []
	with open(original_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		for row in reader:
			header_list = row[:]
			break
	header_list.extend(['new_masterdish','masterdish_flag'])
	op = open(output_filename,'wb')
	writer = csv.writer(op)
	writer.writerow(header_list)
	for row in final_masterdish:
		writer.writerow(row)

def write_dict(write_this,original_filename,output_filename):
	header_list = []
	with open(original_filename,'rb') as inputfile:
		reader = csv.reader(inputfile)
		for row in reader:
			header_list = row[:]
			break
	op = open(output_filename,'wb')
	writer = csv.writer(op)
	writer.writerow(header_list)
	for k,v in write_this.iteritems():
		writer.writerow([k,v])

def write_list(write_this,header_list,output_filename):
	op = open(output_filename,'wb')
	writer = csv.writer(op)
	writer.writerow(header_list)
	for row in write_this:
		writer.writerow(row)

def main():
	original_filename = 'PO-output-1.csv'
	output_filename = 'Poland-masterdish-output.csv'
	new_database_filename = 'masterdish_final_db_output.csv'
	check_list_db_filename = 'check_list_db_output.csv'

	database_filename = 'masterdish_final_db_input.csv'
	check_words_filename = 'check_words.csv'
	cooking_words_filename = 'cooking_words.csv'
	subcat_add_single_filename = 'subcategory_addition_single.csv'
	subcat_add_multi_filename = 'subcategory_addition_multi.csv'
	original_file_md_index = 13
	original_file_cuisine_index = 5
	original_file_subcuisine_index = 6
	

	new_md_db_freq = {}
	add_to_checklist = {}
	
	print "Loading data..."
	start = timeit.default_timer()
	md_db_dict = load_db(database_filename)
	new_md_db_freq = md_db_dict
	md_db_wc_freq = get_sorted_list(md_db_dict)
	check_word_list = load_check_words(check_words_filename)
	cooking_list = load_cooking_list(cooking_words_filename)
	unique_masterdish = find_unique(original_filename,original_file_md_index,original_file_cuisine_index)
	write_list(unique_masterdish,['Masterdish_Name','Frequency'],'Unique_masterdish.csv')
	stop = timeit.default_timer()
	time_taken = stop - start
	print "Loading data done in ",time_taken," sec"
	
	print "Finding Masterdish..."
	start = timeit.default_timer()
	final = find_md(md_db_wc_freq,check_word_list,cooking_list,unique_masterdish)
	stop = timeit.default_timer()
	time_taken = stop - start
	print "Masterdish found in ",time_taken," sec"
	
	print "Adding Sub category..."
	start = timeit.default_timer()
	final_masterdish = remove_empty(final)
	final_masterdish = subcat_addition(final_masterdish,subcat_add_single_filename,subcat_add_multi_filename)
	full_masterdish = map_to_original(final_masterdish,original_filename,original_file_md_index)
	stop = timeit.default_timer()
	time_taken = stop - start
	print "Subcategory addition done in ",time_taken," sec"

	print "Cleaning Masterdish..."
	start = timeit.default_timer()
	final_cleaned_masterdish = word_cleaning(full_masterdish)
	final_cleaned_masterdish = string_cleaning(final_cleaned_masterdish)
	final_cleaned_masterdish = clean_tense(final_cleaned_masterdish)
	stop = timeit.default_timer()
	time_taken = stop - start
	print "Word, String, Tense cleaning done in ",time_taken," sec"

	print "Matching google ping results with masterdish database..."
	start = timeit.default_timer()
	final = match_to_db(final_cleaned_masterdish,md_db_wc_freq,original_file_md_index,original_file_cuisine_index)
	stop = timeit.default_timer()
	time_taken = stop - start
	print "Matching with database done in ",time_taken," sec"
	write_output(final,original_filename,output_filename)

	print "Updating database..."
	start = timeit.default_timer()
	db_change = update_md_db(final,new_md_db_freq,add_to_checklist,original_file_subcuisine_index)
	stop = timeit.default_timer()
	time_taken = stop - start
	print "Database updated in ",time_taken," sec"
	
	write_output(final,original_filename,output_filename)
	write_dict(db_change[0],database_filename,new_database_filename)
	write_dict(db_change[1],database_filename,check_list_db_filename)

if __name__ == '__main__':
	main()