#statisticalAnalysis.py
import operator
from operator import itemgetter
from tabulate import tabulate
import math
import scipy
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



data = list(open('data/nytBookThemes.csv', 'r'))[:-1]

themeCategories = (open('data/book_theme_Categories.csv', 'r'))
allKeys = []
fictionKeys = ()
discardKeys = []

with (open('data/book_theme_Categories.csv', 'r')) as f:
	lines = [line.split(',') for line in f]
	del lines[0]
	for line in lines:
		themeName = line[0]
		if themeName == '':
			continue
		listThemes = []
		del line[0]

		for item in line:
			item = item.strip()
			if item == '':
				continue
			newItem = ''.join([i for i in item if not i.isdigit()])
			newItem = newItem.strip()
			listThemes.append(newItem)
		if themeName == 'Discard':
			discardKeys = listThemes
			continue
		if themeName == 'Fiction Keys':
			fictionKeys = ('Fiction', listThemes)
			continue
		
		allKeys.append((themeName, listThemes))



def binomial_tests(N, p, y):
	test = scipy.stats.binom_test(y, N, p, alternative='two-sided')
	return test

def topXdicts(thisSortedDict, compareDict, countGender, countOtherGender, numTop):
	top10s = []
	percents = []
	i = 0
	numTop = len(thisSortedDict)

	likelihood = float(countGender) / (countGender + countOtherGender)
	for (genre, count) in thisSortedDict:

		if genre not in discardKeys:
			if genre in compareDict:
				compareCount = compareDict[genre]
				if count + compareCount < 10:
					continue
			else:
				compareCount = 0
				if count + compareCount < 10:
					continue
			percentThis = float(count)/countGender * 100
			percentOther = float(compareCount)/countOtherGender * 100
			standardDev = math.sqrt((count + compareCount) * 0.6685 * 0.3315)
			if (float(count) / (count + compareCount)) >= 0.6685:
				skew = "M"
			else:
				skew = "F"

			pValue = binomial_tests((count + compareCount), likelihood, count)

			numberM =  count
			numberF = compareCount


			allOtherMale = countGender - count
			allOtherFemale = countOtherGender - compareCount


			oddsratio, pvalue = stats.fisher_exact([[numberF, allOtherFemale], [numberM, allOtherMale]])


			top10s.append([genre, count, compareCount, standardDev, pValue, oddsratio,  skew])
			percents.append([genre, percentThis, percentOther])
			i = i + 1
		else:
			continue

	top10s = sorted(top10s, key=itemgetter(4), reverse=False)
	percents = sorted(percents, key = itemgetter(2), reverse=True)
	return top10s, percents



def consolidateDict(thisData):

	newData = []

	for (gender, author, themes) in thisData:
		newThemes = []
		for theme in themes:
			found = False
			for (key, listKeys) in allKeys:
				if theme in listKeys:
					newThemes.append(key)
					found = True
			if found == False:
				newThemes.append(theme)
		newThemes = list(set(newThemes))
		newData.append((gender, author, newThemes))

	return newData



def themes(thisData):

	maleThemes = {}
	femaleThemes = {}
	allThemes = {}
	numBooks = 0
	numBooksThemes = 0

	for (gender, author, themes) in thisData:

		themes = themes[0:3]
		if themes != ['']:
			numBooks += 1
			numBooksThemes += 1
		else:
			numBooks += 1


		if gender == 'male':
			for theme in themes:
				if theme == '':
					continue
				if theme in maleThemes:
					maleThemes[theme] += 1
				else:
					maleThemes[theme] = 1
				

		elif gender == 'female':
			for theme in themes:
				if theme == '':
					continue
				if theme in femaleThemes:
					femaleThemes[theme] += 1
				else:
					femaleThemes[theme] = 1

		for theme in themes:
			if theme == '':
				continue
			if theme in allThemes:
				allThemes[theme] += 1
			else:
				allThemes[theme] = 1

	removeKeys = ['Discard']
	for theme in allThemes.keys():
		if allThemes[theme] <= 20:
			removeKeys.append(theme)

	maleThemes = { k:v for k, v in maleThemes.items() if k not in removeKeys}
	femaleThemes = { k:v for k, v in femaleThemes.items() if k not in removeKeys}
	allThemes = { k:v for k, v in allThemes.items() if k not in removeKeys}


	sorted_male = sorted(maleThemes.items(), key=operator.itemgetter(1), reverse=True)

	sorted_female = sorted(femaleThemes.items(), key=operator.itemgetter(1), reverse=True)

	sorted_all = sorted(allThemes.items(), key=operator.itemgetter(1), reverse=True)


	return maleThemes, femaleThemes, allThemes, sorted_male, sorted_female, sorted_all 

def fictionNonFiction(maleDict, femaleDict):
	maleTotalNon = maleDict['Nonfiction']
	femaleTotalNon = femaleDict['Nonfiction']

	femaleTotalFic = femaleDict['Fiction']
	maleTotalFic = maleDict['Fiction']

	print 'count total books labelled F/NF' +  str(maleTotalNon + femaleTotalNon + femaleTotalFic + maleTotalFic)

	return (femaleTotalNon, maleTotalNon), (femaleTotalFic, maleTotalFic)

def genderPercentages(thisData):


	maleCount = 0
	femaleCount = 0
	for (gender, author, themes) in thisData:
		if gender == 'male':
			maleCount += 1
		elif gender == 'female':
			femaleCount += 1

	return maleCount, femaleCount

def genderPercentagesDates(thisData):

	new_L = {}
	for item in thisData:
	    if item[3] in new_L:
	        new_L[item[3]].append(item)
	    else:
	        new_L[item[3]] = []
	        new_L[item[3]].append(item)


	keys = sorted(new_L.keys())


	longitudinalLabels = keys
	longitudinalMale = []
	longidtudinalFemale = []
	allLongitudinal = []


	for key in keys:
		maleCount = 0
		femaleCount = 0
		allCount = 0
		dateData = new_L[key]
		totalCount = len(dateData)
		for (gender, author, themes, date) in dateData:
			if gender == 'male':
				maleCount += 1
				allCount += 1
			elif gender == 'female':
				femaleCount += 1
				allCount += 1

		percentMale = round(float(maleCount)/len(dateData) * 100, 1)
		percentFemale = round(float(femaleCount)/len(dateData) * 100, 1)

		longitudinalMale.append(percentMale)
		longidtudinalFemale.append(percentFemale)
		allLongitudinal.append(allCount)

	return allLongitudinal, longitudinalMale, longidtudinalFemale

def repeats(thisData):
	maleDict = {}
	femaleDict = {}

	for (gender, author, themes) in thisData:
		if gender == 'male':
			if author in maleDict:
				maleDict[author] += 1
			else:
				maleDict[author] = 1
		if gender == 'female':
			if author in femaleDict:
				femaleDict[author] += 1
			else:
				femaleDict[author] = 1

	#print femaleDict
	#print maleDict

	fmKeys = femaleDict.keys()
	mKeys = maleDict.keys()

	femaleMoreThanOne = 0
	femaleMoreThanThree = 0
	femaleMoreThanFive = 0
	femaleMoreThanten = 0

	for key in fmKeys:
		if femaleDict[key] >= 10:
			femaleMoreThanOne += 1
			femaleMoreThanThree += 1
			femaleMoreThanFive += 1
			femaleMoreThanten += 1
		elif femaleDict[key] > 5:
			femaleMoreThanOne += 1
			femaleMoreThanThree += 1
			femaleMoreThanFive += 1
		elif femaleDict[key] > 3:
			femaleMoreThanOne += 1
			femaleMoreThanThree += 1
		elif femaleDict[key] > 1:
			femaleMoreThanOne += 1

	maleMoreThanOne = 0
	maleMoreThanThree = 0
	maleMoreThanFive = 0
	maleMoreThanten = 0

	for key in mKeys:
		if maleDict[key] >= 10:
			maleMoreThanOne += 1
			maleMoreThanThree += 1
			maleMoreThanFive += 1
			maleMoreThanten += 1
		elif maleDict[key] > 5:
			maleMoreThanOne += 1
			maleMoreThanThree += 1
			maleMoreThanFive += 1
		elif maleDict[key] > 3:
			maleMoreThanOne += 1
			maleMoreThanThree += 1
		elif maleDict[key] > 1:
			maleMoreThanOne += 1

	return (femaleMoreThanOne, femaleMoreThanThree, femaleMoreThanFive, femaleMoreThanten), \
			(maleMoreThanOne, maleMoreThanThree, maleMoreThanFive, maleMoreThanten)


def processData(thisData):
	listOfThemes = []
	listOfThemesDates = []

	for item in thisData:
		line = item.split(',')

		filename = line[1]
		reviewer = line[2]
		reviewer_gender = line[3]
		author = line[4]
		authorGender = line[5]
		numAuthors = line[6]
		date = line[7]
		url = line[8]
		title = line[9]


		goodReadsInfo = line[10]
		info = goodReadsInfo.split(";';")

		isbn = info[1][:-1][:-1]

		themes = info[0].split(';')
		themes[0] = themes[0][1:]
		themes = [theme.strip() for theme in themes]

		listOfThemes.append((authorGender, author, themes))
		listOfThemesDates.append((authorGender, author, themes, date))

	return listOfThemes, listOfThemesDates

def listifyWholeThemes(bothDicts):
	total = 0

	returnList = []
	keys = bothDicts.keys()

	for key in keys:
		returnList.append((key, bothDicts[key]))
		total += bothDicts[key]

	returnList = sorted(returnList, key=itemgetter(1), reverse=True)

	return returnList, total

def plots(malePercents, allLong, longMale, longFemale, malePercent, femalePercent, womenNonFicPercent, womenFicPercent, menNonFicPercent, menFicPercent):

	#PIE CHART
	
	labels = 'Men', 'Women'
	fracs = [malePercent, femalePercent]
	colors = ["#e6b3ff", "#b3d1ff"]

	sns.set(style="darkgrid")
	fig1, ax1 = plt.subplots()
	fig1.patch.set_facecolor('white')
	ax1.pie(fracs,labels=labels, autopct='%1.1f%%', colors=colors, wedgeprops = { 'linewidth' : 1 , 'edgecolor' : 'white'})
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.rcParams['patch.edgecolor'] = 'white' 
	plt.title('Breakdown of Books Reviewed By Gender', y=1.05, fontsize=20)
	plt.show()
	plt.savefig('pie.png')
	


	#LONGITUDINAL ALL BOOK COUNTS
	sns.set(style="darkgrid")
	data = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
	fig = plt.bar(data, allLong, color='#98d6ba')
	plt.title('Number of Books in Dataset by Year', y=1.05, fontsize=20)
	plt.xlabel('Year', fontsize=16)
	plt.ylabel('Count of Books', fontsize=16)
	plt.show()

	sns.set(style="whitegrid")
	fig, ax = plt.subplots(figsize=(10,5))
	x = ['Non-Fiction', 'Fiction']
	pos = [0.5,1.25]
	width = 0.25
	dataWomen = [31.9, 58.88]
	dataMen = [42.43, 43.75]

	plt.bar(pos, dataWomen, width, alpha=0.5, color='#b3d1ff', label='Women')
	plt.bar([p + width for p in pos], dataMen, width, alpha=0.5, color='#e6b3ff', label='Men')
	ax.set_ylabel('% of all books', fontsize=16)

	# Set the chart's title
	ax.set_title('Percentage of All Books, Fiction vs. Non-Fiction by Gender', fontsize=20)
	ax.set_xticks([p + 1 * width for p in pos])
	ax.set_xticklabels(x, fontsize=16)
	plt.legend(['Women', 'Men'], loc='upper left', fontsize=16)
	plt.ylim([0, 100] )





	# Adding the legend and showing the plot
	plt.grid()
	plt.show()

def plotThemes(data, male, female):

	data = sorted(data, key=itemgetter(2), reverse=True)
	themes = [x[0] for x in data]
	menNum = [float(x[1])/male * 100 for x in data]
	womenNum = [float(x[2])/female * 100 for x in data]


	sns.set(style="whitegrid")
	fig, ax = plt.subplots(figsize=(10,5))
	x = themes
	pos = [i+.3 for i in range(len(themes))]
	width = 0.3
	dataWomen = womenNum
	dataMen = menNum

	plt.bar(pos, dataWomen, width, alpha=0.5, color='#b3d1ff', label='Women')
	plt.bar([p + width for p in pos], dataMen, width, alpha=0.5, color='#e6b3ff', label='Men')
	ax.set_ylabel("% of Each Gender's Books", fontsize=16)

	# Set the chart's title
	ax.set_title("Percentage of Each Gender's Total Books by Genre", fontsize=20)
	ax.set_xticks([p + .5 * width for p in pos])
	ax.set_xticklabels(x, fontsize=11, rotation=90)
	plt.legend(['Women', 'Men'], loc='upper left', fontsize=16)
	plt.ylim([0, 25] )

	plt.tight_layout()
	plt.grid()
	plt.show()

def main():
	dataList, dataListDates = processData(data)
	dataListDates

	#total review count
	totalReviews = len(dataList)
	print 
	print 'Analyzing: ' + str(totalReviews) + ' book reviews.'

	#percentage man vs. woman
	maleCount, femaleCount = genderPercentages(dataList)
	allLong, longMale, longFemale = genderPercentagesDates(dataListDates)

	malePercent = float(maleCount)/totalReviews * 100
	femalePercent = float(femaleCount)/totalReviews * 100

	print 
	print 'Of the ' + str(totalReviews) + ' reviews: ' + str(maleCount) + \
				' (' + str(round(malePercent, 2)) + '%) are written by men'
	print 'Of the ' + str(totalReviews) + ' reviews: ' + str(femaleCount) + \
				' (' + str(round(femalePercent, 2)) + '%) are written by women'



	#how often do male vs. female authors get re-reviewed
	femaleRepeats, maleRepeats = repeats(dataList)
	(femaleMoreThanOne, femaleMoreThanThree, femaleMoreThanFive, femaleMoreThanten) = femaleRepeats
	(maleMoreThanOne, maleMoreThanThree, maleMoreThanFive, maleMoreThanten) = maleRepeats

	womenRepeatPercent = float(femaleMoreThanOne)/femaleCount * 100
	menRepeatPercent = float(maleMoreThanOne)/maleCount * 100

	womenRepeatPercent3 = float(femaleMoreThanThree)/femaleCount * 100
	menRepeatPercent3 = float(maleMoreThanThree)/maleCount * 100

	womenRepeatPercent5 = float(femaleMoreThanFive)/femaleCount * 100
	menRepeatPercent5 = float(maleMoreThanFive)/maleCount * 100

	print 
	print str(round(menRepeatPercent, 2)) + '% of male authors are reviewed more than once.'
	print str(round(womenRepeatPercent, 2)) + '% of female authors are reviewed more than once.'

	print 
	print str(round(menRepeatPercent3, 2)) + '% of male authors are reviewed more than three times.'
	print str(round(womenRepeatPercent3, 2)) + '% of female authors are reviewed more than three times.'
	print

	print str(round(menRepeatPercent5, 2)) + '% of male authors are reviewed more than five times.'
	print str(round(womenRepeatPercent5, 2)) + '% of female authors are reviewed more than five times.'
	print  

	#unconsolidated dicts datas
	maleThemes, femaleThemes, allThemes, sorted_male, sorted_female, sorted_all = themes(dataList)
	(femaleTotalNon, maleTotalNon),(femaleTotalFic, maleTotalFic) = fictionNonFiction(maleThemes, femaleThemes)
	
	bothDicts = { k: maleThemes.get(k, 0) + femaleThemes.get(k, 0) for k in set(maleThemes) & set(femaleThemes) }
	
	lengthKeys = len(allThemes.keys())

	womenNonFicPercent = float(femaleTotalNon)/femaleCount * 100
	menNonFicPercent = float(maleTotalNon)/maleCount * 100

	womenFicPercent = float(femaleTotalFic)/femaleCount * 100
	menFicPercent = float(maleTotalFic)/maleCount * 100

	print 'male'
	top20Male, malePercents = topXdicts(sorted_male, femaleThemes, maleCount, femaleCount, 20)
	print 'female'
	top20Female, femalePercents = topXdicts(sorted_female, maleThemes, femaleCount, maleCount, 20)

	allDictList, total = listifyWholeThemes(allThemes)

	print 
	print "-----------UNCONSOLIDATED THEMES------------"
	print
	print 'Number of unique themes found: ' + str(lengthKeys)
	print 'Number of total themes found: ' + str(total)
	print tabulate(allDictList, headers=["Theme", "TotalCount"]) 

	print 
	print 'Percentage of Books by Women that are Nonfiction: ' + str(round(womenNonFicPercent, 2)) + '%, ' + str(femaleTotalNon) 
	print 'Percentage of Books by Women that are Fiction: ' + str(round(womenFicPercent, 2)) + '%, ' + str(femaleTotalFic) 

	print 
	print 'Percentage of Books by Men that are Nonfiction: ' + str(round(menNonFicPercent, 2)) + '%, ' + str(maleTotalNon)
	print 'Percentage of Books by Men that are Fiction: ' + str(round(menFicPercent, 2)) + '%, ' + str(maleTotalFic) 

	print 'Male Count' + str(maleCount)
	print 'Female Count' + str(femaleCount)
	print 
	print "Men: Top Themes and Corresponding Women's Percentage"
	print
	print tabulate(top20Male, headers=["Theme", "Men(#)", "Women(#)",'Standard Dev', 'P Value'])

	print 
	print "Women: Top Themes and Corresponding Men's Percentage"
	print
	print tabulate(top20Female, headers=["Theme", "Women(#)", "Men(#)",'Standard Dev', 'P Value'])
	print 


	#consolidated dict datas
	newData = consolidateDict(dataList)
	maleThemesCons, femaleThemesCons, allThemes, sorted_maleCons, sorted_femaleCons, sorted_all = themes(newData)
	

	(femaleTotalNonCons, maleTotalNonCons),(femaleTotalFicCons, maleTotalFicCons) = fictionNonFiction(maleThemesCons, femaleThemesCons)

	print allThemes
	womenNonFicPercentCons = float(femaleTotalNonCons)/femaleCount * 100
	menNonFicPercentCons = float(maleTotalNonCons)/maleCount * 100

	womenFicPercentCons = float(femaleTotalFicCons)/femaleCount * 100
	menFicPercentCons = float(maleTotalFicCons)/maleCount * 100

	print sorted_maleCons
	print 'male'
	top20MaleCons, malePercents = topXdicts(sorted_maleCons, femaleThemesCons, maleCount, femaleCount, len(sorted_maleCons))
	print 'female'
	top20FemaleCons, femalePercents = topXdicts(sorted_femaleCons, maleThemesCons, femaleCount, maleCount, len(sorted_femaleCons))

	bothDictsCons = { k: maleThemesCons.get(k, 0) + femaleThemesCons.get(k, 0) for k in set(maleThemesCons) | set(femaleThemesCons) }
	lengthKeysCons = len(allThemes.keys())


	print "-----------CONSOLIDATED THEMES------------"
	print 
	print 'Number of total themes found: ' + str(lengthKeysCons)
	print  

	
	
	print 'Percentage of Books by Women that are Nonfiction: ' + str(round(womenNonFicPercentCons, 2)) + '%, ' + str(femaleTotalNonCons) 
	print 'Percentage of Books by Women that are Fiction: ' + str(round(womenFicPercentCons, 2)) + '%, ' + str(femaleTotalFicCons)

	print 
	print 'Percentage of Books by Men that are Nonfiction: ' + str(round(menNonFicPercentCons, 2)) + '%, ' + str(maleTotalNonCons)
	print 'Percentage of Books by Men that are Fiction: ' + str(round(menFicPercentCons, 2)) + '%, ' + str(maleTotalFicCons)
	

	print 
	print "Consolidated Themes"
	print 
	print tabulate(top20MaleCons, headers=["Theme", "Men(#)", "Women(#)",'Standard Dev', 'P Value', 'Odds Ratio', 'skew'])
	print "percents"
	print tabulate(malePercents, headers=["Theme", "Men(%)", "Women(%)"])

	#plots(malePercents, allLong, longMale, longFemale, malePercent, femalePercent, womenNonFicPercent, womenFicPercent, menNonFicPercent, menFicPercent)
	plotThemes(top20MaleCons, maleCount, femaleCount)




if __name__ == '__main__':
   main()
