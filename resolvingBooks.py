import wikipedia
from bs4 import BeautifulSoup
import urllib2
from goodreads import client
import csv
import os

urlTitles = list(open('metaAdditionsTitles.csv', 'r'))


finalFile = open('nytBookThemes.csv', 'w').close()
finalFile = open('nytBookThemes.csv', 'a')


def getWikiGenre(title):
	genre = ''

	try:
		book = wikipedia.page(title)
	except wikipedia.DisambiguationError, e:

		allResults = e.options

		found = False
		for result in allResults:
			if '(novel)' in result:
				book = wikipedia.page(result)
				found = True

		if found == False:
			return 'Wiki not found'



	url = book.url

	print url

	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, "lxml")

	vcard = soup.find_all("table", class_="infobox vcard")[0]
	rows = vcard.find_all("tr")

	for row in rows:
		try:
			th = row.find_all("th")[0]
			td = row.find_all("td")[0]
			if th.text.lower() == 'genre':
				genre = td.text
				genre = genre.encode(('utf8'))
				genre = genre.rstrip().split('\n')
				genre = "; ".join(genre)
				return genre
		
		except:
			continue

	return 'No Genre found'

def getGoodReadsGenres(link):
	page = urllib2.urlopen(link)
	soup = BeautifulSoup(page, "lxml")

	main = soup.find_all("div", class_="mainContent")[0]
	content = main.find_all("div", class_="mainContentFloat")[0]
	right = content.find_all("div", class_="rightContainer")[0]
	left = right.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['stacked'])[0]
	bigBox = left.find_all("div", class_="bigBox")[0]
	genreBox = bigBox.find_all("div", class_="bigBoxBody")[0]
	genres = genreBox.find_all("div", class_="elementList")

	listGenres = []
	for genre in genres:
		thisGenreContainer = genre.find_all("div", class_="left")[0]
		thisGenre = thisGenreContainer.find_all("a", "actionLinkLite bookPageGenreLink")[0].text
		listGenres.append(thisGenre)


	return list(set(listGenres))

def getAllGenres(title, author, gc):
	print 'finding Goodreads URL'
	try:
		book = gc.search_books(search + ' ' + author)[0]
	except:
		try:
			book = gc.search_books(title)[0]
		except:
			try:
				newTitle = title.split(' ')[0:4]
				book = gc.search_books(newTitle)[0]
			except:
				print title
				print author
				print 'DIDN"T WORK'

	isbn =  book.isbn
	link = book.link
	print link
	wikiGenre = ""
	GRgenre = []


	#try:
	#	wikiGenre = getWikiGenre(title)
	#except Exception, e:
	#	print "Unable to get wiki"
	#	print e

	try:
		GRgenre = getGoodReadsGenres(link)
	except Exception, e:
		print "Unable to get goodreads"
		print e

	print title
	#print "Wikipedia finds: " + wikiGenre
	print "Goodreads finds: " + "; ".join(GRgenre)

	return title, wikiGenre, "; ".join(GRgenre), isbn


def main():
	print 'authenticating goodreads'
	gc = client.GoodreadsClient("ENQJ9KubRltIC7lSKZSYA", "trYzd1HBcV4kNCtarG071uFZS1nbKLvo5Rg8CTb0ao")


	#lines = list(open('bookTitles.txt', 'r'))[0]
	#listBooks = lines.split(', ')

	for row in urlTitles:
		line = row.split(',')
		if line[6] == 'y':
			continue
		filename = line[1]
		reviewer = line[2]
		reviewer_gender = line[3]
		author = line[4]
		authorGender = line[5]
		numAuthors = line[6]
		date = line[7]
		url = line[8]
		title = line[9]

		title = title[:-1]

		try:
			title, wikiGenre, grGenre, isbn  = getAllGenres(title, author, gc)
			row = row[:-1]
			writtenstring = row + title + ',(' + grGenre + ";';" + str(isbn) + ')' + '\n'
			finalFile.write(writtenstring)

		
		except:
			continue
		


		

if __name__ == '__main__':
   main()


