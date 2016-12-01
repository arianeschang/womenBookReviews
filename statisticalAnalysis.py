#statisticalAnalysis.py
import operator
from operator import itemgetter
from tabulate import tabulate

data = list(open('nytBookThemes.csv', 'r'))[:-1]

fictionKeys = ('Fiction', ['Womens Fiction', 'Science Fiction', 'Fiction', 'Historical Fiction', 'Realistic Fiction', \
					'Literary Fiction', 'Science Fiction Fantasy', 'Christian Fiction', 'Speculative Fiction', 'Adult Fiction'])
historyKeys = ('History', ['History', 'Historical Fiction', 'Historical', 'North American Hi...', 'Military History', \
						'Russian History', 'History and Politics', 'European History'])

#QUESTIONABLE
Sociology = ('Humanities', ['Social Science', 'Sociology', 'Cultural', 'Culture', 'Anthropology', 'Museology', 'Social', 'Humanities'])
socialIssues = ('Social Issues', ['Social Movements'])

feminismKeys = ('Feminism', ['Feminism', 'Womens', 'Womens Fiction', 'Female Authors'])
familyKeys = ('Family', ['Marriage', 'Parenting'])
blgtKeys = ('BLGT', ['Glbt', 'Gay Romance', 'Queer'])
romanceKeys = ('Romance', ['Gay Romance', 'Romance', 'Love', 'Romantic', 'Relationships', 'Category Romance'])
genderKeys = ('Gender and Sexuality', ['Gender', 'Sexuality', 'Erotica'])

businessKeys = ('Business', ['Business', 'Management', 'Buisness', 'Leadership'])

sportsKeys = ('Sports', ['Mountaineering', 'Football', 'Soccer', 'Sports and Games'])
scienceKeys = ('Science', ['Science Nature', 'Space', 'Biology', 'Neuroscience'])
technologyKeys = ('Technology', ['Artificial Intelligence', 'Computers'])

fantasyKeys = ('Fantasy|Science Fiction', ['Science Fiction', 'Fantasy', 'Science Fiction Fantasy', 'Shapeshifters', 'Superheroes', 'Fairies'])

biographyKeys = ('Biography', ['Biography Memoir', 'Biography'])
autobiographyKeys= ('Autobiography', ['Autobiography', 'Diary'])

warKeys = ('War', ['War', 'Military', 'World War II', 'Crime', 'Military History'])
adventureKeys = ('Adventure', ['Adventure', 'Thriller', 'Mystery', 'Action', 'Suspense', 'Paranormal', 'Spy Thriller'])
artKeys = ('Art', ['Sequential Art', 'Art', 'Design', 'Music', 'Art and Photography'])
governmentKeys = ('Politics|Economics|Law', ['Politics', 'Economics', 'Law', 'History and Politics'])

environmentalKeys = ('Environment', ['Wildlife', 'Animals', 'Environment', 'Science Nature', 'Nature'])

darkKeys = ('death|dark', ['Death', 'Dark'])

#QUESTIONABLE
healthKeys = ('Health', ['Health', 'Fat', 'Medical'])
mentalHealthKeys = ('Mental Health', ['Alcohol', 'Mental Health'])

domestic = ('Domestic/American', ['American', 'New York', 'North American Hi...', 'Western', 'United States', 'American History'])
international = ('Foreign/Non-American', ['European Literature', 'Asian Literature', 'Russian History', 'Russia', 'European History'])

christianity = ('Christianity', ['Christian', 'Christianity', 'Christian Fiction', 'Church'])

discardKeys = ['Fiction', 'Nonfiction', 'Contemporary', 'Literature', 'Novels', 'Short Stories', 'Writing', 'Book Club', '']
#discardKeys = []

allKeys = [fictionKeys, historyKeys, Sociology, socialIssues, feminismKeys,familyKeys, blgtKeys, romanceKeys, genderKeys, sportsKeys,
				scienceKeys, fantasyKeys, biographyKeys, domestic, international, christianity, businessKeys, darkKeys, \
				autobiographyKeys, warKeys, adventureKeys, artKeys, governmentKeys, environmentalKeys, healthKeys, mentalHealthKeys]

def topXdicts(thisSortedDict, compareDict, countGender, countOtherGender, numTop):
	top10s = []
	i = 0
	numTop = 30
	for (genre, count) in thisSortedDict:
		if i == numTop:
			top10s = sorted(top10s, key=itemgetter(3), reverse=True)
			return top10s
		if genre not in discardKeys:
			compareCount = compareDict[genre]
			percentThis = float(count)/countGender * 100
			percentOther = float(compareCount)/countOtherGender * 100
			delta = (percentThis - percentOther)/((percentThis + percentOther)/2) * 100
			top10s.append([genre, percentThis, percentOther, delta])
			i = i + 1
		else:
			continue

	top10s = sorted(top10s, key=itemgetter(3), reverse=True)
	return top10s



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

	for (gender, author, themes) in thisData:
		if gender == 'male':
			for theme in themes:
				if theme in maleThemes:
					maleThemes[theme] += 1
				else:
					maleThemes[theme] = 1
		elif gender == 'female':
			for theme in themes:
				if theme in femaleThemes:
					femaleThemes[theme] += 1
				else:
					femaleThemes[theme] = 1

	sorted_male = sorted(maleThemes.items(), key=operator.itemgetter(1), reverse=True)

	sorted_female = sorted(femaleThemes.items(), key=operator.itemgetter(1), reverse=True)

	return maleThemes, femaleThemes, sorted_male, sorted_female

def fictionNonFiction(maleDict, femaleDict):
	maleTotalNon = maleDict['Nonfiction']
	femaleTotalNon = femaleDict['Nonfiction']

	femaleTotalFic = femaleDict['Fiction']
	maleTotalFic = maleDict['Fiction']

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
	'''
	print femaleMoreThanOne
	print maleMoreThanOne
	print

	print femaleMoreThanThree
	print maleMoreThanThree
	print

	print femaleMoreThanFive
	print maleMoreThanFive
	print

	print femaleMoreThanten
	print maleMoreThanten
	print
	'''

	return (femaleMoreThanOne, femaleMoreThanThree, femaleMoreThanFive, femaleMoreThanten), \
			(maleMoreThanOne, maleMoreThanThree, maleMoreThanFive, maleMoreThanten)


def processData(thisData):
	listOfThemes = []

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

	return listOfThemes

def listifyWholeThemes(bothDicts):
	total = 0

	returnList = []
	del bothDicts[""]
	keys = bothDicts.keys()

	for key in keys:
		returnList.append((key, bothDicts[key]))
		total += bothDicts[key]

	returnList = sorted(returnList, key=itemgetter(1), reverse=True)

	return returnList, total


def main():
	dataList = processData(data)

	#total review count
	totalReviews = len(dataList)
	print 
	print 'Analyzing: ' + str(totalReviews) + ' book reviews.'

	#percentage man vs. woman
	maleCount, femaleCount = genderPercentages(dataList)

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
	maleThemes, femaleThemes, sorted_male, sorted_female = themes(dataList)
	(femaleTotalNon, maleTotalNon),(femaleTotalFic, maleTotalFic) = fictionNonFiction(maleThemes, femaleThemes)
	bothDicts = { k: maleThemes.get(k, 0) + femaleThemes.get(k, 0) for k in set(maleThemes) & set(femaleThemes) }
	lengthKeys = len(bothDicts.keys())

	womenNonFicPercent = float(femaleTotalNon)/femaleCount * 100
	menNonFicPercent = float(maleTotalNon)/maleCount * 100

	womenFicPercent = float(femaleTotalFic)/femaleCount * 100
	menFicPercent = float(maleTotalFic)/maleCount * 100

	top20Male = topXdicts(sorted_male, femaleThemes, maleCount, femaleCount, 20)
	top20Female = topXdicts(sorted_female, maleThemes, femaleCount, maleCount, 20)

	allDictList, total = listifyWholeThemes(bothDicts)

	print 
	print "-----------UNCONSOLIDATED THEMES------------"
	print
	print 'Number of unique themes found: ' + str(lengthKeys)
	print 'Number of total themes found: ' + str(total)
	print tabulate(allDictList, headers=["Theme", "TotalCount"]) 

	print 
	print 'Percentage of Books by Women that are Nonfiction: ' + str(round(womenNonFicPercent, 2)) + '%' 
	print 'Percentage of Books by Women that are Fiction: ' + str(round(womenFicPercent, 2)) + '%' 

	print 
	print 'Percentage of Books by Men that are Nonfiction: ' + str(round(menNonFicPercent, 2)) + '%' 
	print 'Percentage of Books by Men that are Fiction: ' + str(round(menFicPercent, 2)) + '%' 

	print 
	print "Men: Top 20 Themes and Corresponding Women's Percentage"
	print
	print tabulate(top20Male, headers=["Theme","Men(%)", "Women(%)", 'Delta'])

	print 
	print "Women: Top 20 Themes and Corresponding Men's Percentage"
	print
	print tabulate(top20Female, headers=["Theme","Women(%)", "Men(%)", "Delta"])
	print 


	#consolidated dict datas
	newData = consolidateDict(dataList)
	maleThemesCons, femaleThemesCons, sorted_maleCons, sorted_femaleCons = themes(newData)
	(femaleTotalNonCons, maleTotalNonCons),(femaleTotalFicCons, maleTotalFicCons) = fictionNonFiction(maleThemesCons, femaleThemesCons)

	womenNonFicPercentCons = float(femaleTotalNonCons)/femaleCount * 100
	menNonFicPercentCons = float(maleTotalNonCons)/maleCount * 100

	womenFicPercentCons = float(femaleTotalFicCons)/femaleCount * 100
	menFicPercentCons = float(maleTotalFicCons)/maleCount * 100

	top20MaleCons = topXdicts(sorted_maleCons, femaleThemesCons, maleCount, femaleCount, 20)
	top20FemaleCons = topXdicts(sorted_femaleCons, maleThemesCons, femaleCount, maleCount, 20)

	bothDictsCons = { k: maleThemesCons.get(k, 0) + femaleThemesCons.get(k, 0) for k in set(maleThemesCons) | set(femaleThemesCons) }
	lengthKeysCons = len(bothDictsCons.keys())


	print "-----------CONSOLIDATED THEMES------------"
	print 
	print 'Number of total themes found: ' + str(lengthKeysCons)
	print  

	
	
	print 'Percentage of Books by Women that are Nonfiction: ' + str(round(womenNonFicPercentCons, 2)) + '%' 
	print 'Percentage of Books by Women that are Fiction: ' + str(round(womenFicPercentCons, 2)) + '%' 

	print 
	print 'Percentage of Books by Men that are Nonfiction: ' + str(round(menNonFicPercentCons, 2)) + '%' 
	print 'Percentage of Books by Men that are Fiction: ' + str(round(menFicPercentCons, 2)) + '%' 
	

	print 
	print "Men: Top 20 Themes and Corresponding Women's Percentage"
	print 
	print tabulate(top20MaleCons, headers=["Theme","Men(%)", "Women(%)", 'Delta'])

	print 
	print "Women: Top 20 Themes and Corresponding Men's Percentage"
	print
	print tabulate(top20FemaleCons, headers=["Theme","Women(%)", "Men(%)", "Delta"])
	print 








if __name__ == '__main__':
   main()
