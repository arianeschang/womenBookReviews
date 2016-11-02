import requests


import json


baseurl = "https://api.nytimes.com/svc/books/v3/reviews.json?api-key=ee16f894db8b43258d8d15ef622f82a4";

'''
session = requests.Session()

url = url + '&author=Ben%20Lerner'

r = requests.get(url)
print r
json_data = json.loads(r.text)
print json_data
'''
def getresponse1(author):
	authorString = '&author=' + author.replace(' ', '%20')
	thisUrl = baseurl + authorString
	print thisUrl

	r = requests.get(thisUrl)
	json_data = json.loads(r.text)
	print json_data
	return json_data

def getresponse():
	return {u'status': u'OK', u'num_results': 11, u'results': [{u'book_title': u'Zone One', u'byline': u'GLEN DUNCAN', u'isbn13': [u'9780307455178', u'9780385528078', u'9780385535014', u'9781410446213'], u'url': u'http://www.nytimes.com/2011/10/30/books/review/zone-one-by-colson-whitehead-book-review.html', u'publication_dt': u'2011-10-30', u'summary': u'In Colson Whitehead\u2019s novel, humans spared the effects of a plague battle zombies in Lower Manhattan.', u'book_author': u'Colson Whitehead'}, {u'book_title': u'Sag Harbor', u'byline': u'TOUR\xc9', u'isbn13': [u'9780307455161'], u'url': u'http://www.nytimes.com/2009/05/03/books/review/Toure-t.html', u'publication_dt': u'2009-05-03', u'summary': u'The well-off 15-year-old black hero of Colson Whitehead\u2019s memoiristic fourth novel lives in a world where life doesn\u2019t assault him but rather affords him the time to figure out who he wants to be.', u'book_author': u'Colson Whitehead'}, {u'book_title': u'Sag Harbor', u'byline': u'JANET MASLIN', u'isbn13': [u'9780307455161'], u'url': u'http://www.nytimes.com/2009/04/27/books/27masl.html', u'publication_dt': u'2009-04-27', u'summary': u'Colson Whitehead\u2019s sea-breeze buoyant novel captures the fireflies of teenage summertime in a jar without pretending to have some larger purpose.', u'book_author': u'Colson Whitehead'}, {u'book_title': u'THE NOBLE HUSTLE: Poker, Beef Jerky and Death', u'byline': u'DAVID KIRBY', u'isbn13': [u'9780385537056'], u'url': u'http://www.nytimes.com/2014/06/01/books/review/the-noble-hustle-and-fading-hearts-on-the-river.html', u'publication_dt': u'2014-06-01', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'The Intuitionist', u'byline': u'GARY KRIST', u'isbn13': [u'9780385492997'], u'url': u'http://www.nytimes.com/1999/02/07/books/the-ascent-of-man.html', u'publication_dt': u'1999-02-07', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'John Henry Days', u'byline': u'DANIEL ZALEWSKI', u'isbn13': [u'9780385498197'], u'url': u'http://www.nytimes.com/2001/05/13/books/interview-tunnel-vision.html', u'publication_dt': u'2001-05-13', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'John Henry Days', u'byline': u'JONATHAN FRANZEN', u'isbn13': [u'9780385498197'], u'url': u'http://www.nytimes.com/2001/05/13/books/freeloading-man.html', u'publication_dt': u'2001-05-13', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'John Henry Days', u'byline': u'', u'isbn13': [u'9780385498197'], u'url': u'http://www.nytimes.com/2001/12/02/books/editors-choice.html', u'publication_dt': u'2001-12-02', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'The Colossus of New York: A City in 13 Parts', u'byline': u'LUC SANTE', u'isbn13': [u'9780385507943'], u'url': u'http://www.nytimes.com/2003/10/19/books/eight-million-reasons.html', u'publication_dt': u'2003-10-19', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'Apex Hides the Hurt: A Novel', u'byline': u'DAVID GATES', u'isbn13': [u'9780385507950'], u'url': u'http://www.nytimes.com/2006/04/02/books/review/02gates.html', u'publication_dt': u'2006-04-02', u'summary': u'', u'book_author': u'Colson Whitehead'}, {u'book_title': u'The Underground Railroad', u'byline': u'JUAN GABRIEL V\xc1SQUEZ', u'isbn13': [u'9780385542364'], u'url': u'http://www.nytimes.com/2016/08/14/books/review/colson-whitehead-underground-railroad.html', u'publication_dt': u'2016-08-14', u'summary': u'In \u201cThe Underground Railroad,\u201d his new novel about American slavery, Colson Whitehead courageously opens his eyes where the rest of us would rather look away.', u'book_author': u'Colson Whitehead'}], u'copyright': u'Copyright (c) 2016 The New York Times Company.  All Rights Reserved.'}




def dealwithresponse(resultdict, filename, reviewer):

	filename = filename.split('.txt')[0]

	nums = []
	for letter in filename:
		print letter
		try:
			int(letter)
			nums.append(letter)
		except:
			break

	nums = ''.join(nums)
	noprelimnums = filename.replace(nums, '')
	print noprelimnums

	print reviewer

	targetBook = ''

	if resultdict['num_results'] == 1:
		targetBook = resultdict['results'][0]
		return targetBook

	elif resultdict['num_results'] == 0:
		return 
	else:
		resultArray = resultdict['results']
		realResults = []
		for result in resultArray:
			if noprelimnums in result['url']:
				realResults.append(result)

		if len(realResults) == 1:
			return realResults[0]


def main():
	lines = list(open('initialMeta.csv', 'r'))
	WCLines = list(open('initialMetaWC.csv', 'r'))

	del lines[0]

	try:
		metaLines = list(open('metaAdditions.csv', 'r'))
		outputFile = open('metaAdditions.csv', 'a')
	except:
		outputFile = open('metaAdditions.csv', 'a')
		outputFile.write('file_name,file_name_complete,reviewer,reviewer_gender,author,author_gender,multiple,date,review_url,book_isbn,book_title' + '\n')


	for row in lines:

		line = row.split(',')
		if line[6] == 'y':
			continue
		filename = line[1]
		if filename != '02gates.html.txt':
			continue
		reviewer = line[2]
		reviewer_gender = line[3]
		author = line[4]
		authorGender = line[5]
		numAuthors = line[6]
		date = line[7]

		print filename

		response = getresponse()
		print response
		result = dealwithresponse(response, filename, reviewer)

		url = result['url'].encode('utf8')
		isbn13 = result['isbn13'][0]
		title = result['book_title'].encode('utf8')
		print isbn13

		print type(url), type(isbn13), type(title)

		print url

		row = row + ',' + url + ',' + isbn13 + ',' + title
		outputFile.write(row + '\n')

		print result
		

	







if __name__ == '__main__':
   main()
