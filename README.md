# FoodPanda-Global-Master-Dish
Built information retrieval and recommendation system for global master dish database across 42 countries with User Interface. Implemented data mining techniques to classify the unstructured data &amp; formulate association rules


Stages:
-	Step 0: Add Count to Input file
-	Step 1: Translation
-	Step 2: Cleaning of alcoholic and Non-alcoholic Beverages
-	Step 3: Cleaning of all products except alcoholic Beverages
-	Step 4: Add Classifiers to masterdish
-	Step 5: Finding of Correct masterdish
-	Step 6: Finding of Suncuisine and Subcategory
-	Step 7: Country cuisine mapping based on restaurants(R language)
-	Step 8: Compression code 
-	Step 9: generate final file
-	Step 10: Find Ingredients
-	Step 11: Add masterdish to Db
-	Step 12: Final File Fixes
-	Step 13: Confidence addition
-	Step 14: Find Stats for DB match


Step 0(Description):
-	Add count in the original file to track all the rows based on the count

Step 1(Description):
1. Language analysis:
	-	Take random entries(10% of total data) find the language in which the product is written.
	-	Make a list of majority of languages
	-	Based on the output, decide what languages will be used for translation and one language  by default.
2. Find Unique of product & menu and perform the translation and map it back to the main file.
	Logic:
	-	make default lang based on above result except few other languages.
	-	Translate the input(i1) to english(o1)
	-	Now reverse translate the output(o1) of above step back to original word(i2).
	-	Find % match of i1 and i2 which is equal to x.
	-	IF i1 is already lowercase then o1 is the answer else lowercase i1 and repeat above steps of only step2. Now let y be the % db match.
	-	if x > y,o1 is the answer else other.

Step 2(Description):
-	Find Alcoholic and Nonalcoholic beverages based on the wordlist.
-	Find masterdish of alcoholic beverages
-	Classify cuisine,subcuisine and subcategory of Alco & Non-alco beverages

Step 3(Description):
-	Find Clean Masterdish by removing punctuations,variants and prepositions.
-	Also other processing takes place to get better masterdish output.

Step 4(Description):
-	Add Classifier to masterdish where classifier are missed out from the masterdish

Step 5(Description):
-	Check the masterdish in db(direct match and 95% match).
-	Force fitting using DB
-	if not present in db than send the MD for google pinging.
-	Clean the result of google ping and again check it if present in DB

Step 6(Description):
-	Find Cuisine, Subcuisine and Subcategory of Masterdishes with the help of wordlist.

Step 7(Description):
-	Find cuisine for respective country based on restaurant mapping(Using R code).

Step 8(Description):
-	Run compression Code to find what different cuisine subcuisine and subcategory a MD have. 

Step 9(Description):
-	Based on compression Output generate final files

Step 10(Description):
-	Find ingredients by pinging recipepuppy by MD.

Step 11(Description):
-	Add masterdish to DB based on high frequency and some other logic.

Step 12(Description):
-	Run final fixes code to fix md,cuisine,subcuisine and subcategory.

Step 13(Description):
-	Find confidence ratio for masterdish having various cuisine,subcuisine and subcategory.

Step 14(Description):
-	Find Stats related to MD matching the dishes in DB.
