import pickle

metaLines = list(open('data/001.txt', 'r'))
lines = list(open('data/initialMeta.csv', 'r'))
WCLines = list(open('data/initialMetaWC.csv', 'r'))

i = 0

del lines[0]
finalData = []
tooMany = []

j = 0
for row in lines:
	line = row.split(',')

	if line[6] == 'y':
		continue
	filename = line[1]
	fileURL = filename.split('.txt')[0]
	reviewer = line[2]
	reviewer_gender = line[3]
	author = line[4]
	authorGender = line[5]
	numAuthors = line[6]
	date = line[7]

	#print filename

	possibleURLS = []
	for url in metaLines:
		fileURL = fileURL.split('.html')[0]
		if fileURL.strip() in url.strip() and date.strip() in url.strip():
			possibleURLS.append(url)


	if len(possibleURLS) == 0:
		finalData.append((row, 'none found', None))
		print fileURL
		print row
		#continue
	elif len(possibleURLS) == 1:
		finalData.append((row, possibleURLS[0], None))
		continue
	elif len(possibleURLS) > 1:
		urlsWithHTML = []
		for thisURL in possibleURLS:
			if thisURL.endswith('html\n'):
				urlsWithHTML.append(thisURL)


		if len(urlsWithHTML) == 0:
			finalData.append((row, 'no html files found', None))
			print possibleURLS
			print row

		else:
			urlsRightDate = []

			for thisURL in urlsWithHTML:
				if date.strip() in thisURL.strip():
					urlsRightDate.append(thisURL)

			if len(urlsRightDate) == 1:
				finalData.append((row, urlsRightDate[0], None))
			else:
				finalData.append((row, 'too many files found', urlsRightDate))
				tooMany.append((row, urlsRightDate))
				print urlsRightDate
				print urlsWithHTML
				print row

		

print len(finalData)
with open('listTooManyNYTarticles','w') as f:
    pickle.dump(tooMany,f)

tooManyFiles = 0
noFiles = 0
noHTMLFiles = 0
goodFiles = 0


try:
	metaLines = list(open('metaAdditions2.csv', 'r'))
	outputFile = open('metaAdditions2.csv', 'w')
except:
	outputFile = open('metaAdditions2.csv', 'w')
	outputFile.write('file_name,file_name_complete,reviewer,reviewer_gender,author,author_gender,multiple,date,review_url,book_isbn,book_title' + '\n')

for (row, url, possibleList) in finalData:

	if url == 'too many files found':
		tooManyFiles += 1
	elif url == 'no html files found': 
		noHTMLFiles += 1
	elif url == 'none found':
		noFiles += 1
	else:
		url = url[:-1]
		row = row[:-2]
		string = row + ',' + url + '\n'
		outputFile.write(string)
		goodFiles += 1

print tooManyFiles
print noFiles
print noHTMLFiles
print goodFiles
print tooManyFiles + noFiles + noHTMLFiles + goodFiles




