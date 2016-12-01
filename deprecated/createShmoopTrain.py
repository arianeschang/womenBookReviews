from goodreads import client
from time import strftime, gmtime
from bs4 import BeautifulSoup
import urllib2




lines = list(open('shmoopTrainThemes.csv', 'r'))

print 'authenticating goodreads'
gc = client.GoodreadsClient("ENQJ9KubRltIC7lSKZSYA", "trYzd1HBcV4kNCtarG071uFZS1nbKLvo5Rg8CTb0ao")


def getGoodreads(link):

	page = urllib2.urlopen(link)
	soup = BeautifulSoup(page, "lxml")

	main = soup.find("div", "leftContainer")
	content = main.find("div", "last col stacked")
	right = content.find("div", id="metacol")
	description = str(right.find("div", 'readable stacked'))

	description = BeautifulSoup(description.split('</span>')[1], 'lxml').text

	print description
	return description.encode('utf-8')

finalLines = []

i = 0
for line in lines:
	split = line.split(',')
	title = split[0] 
	author = split[1]

	print title
	print author

	print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
	print 'looking for book'
	book = gc.search_books(title)[0]
	print book
	print strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())



	title = book.title
	description = book.description.encode('utf-8')
	link = book.link
	print link

	print description

	if description == None:
		description = getGoodreads(link)

	line += ('#$' + description)
	finalLines.append(line)
	i = i + 1
	if i == -1:
		break


print finalLines
outputFile = open('shmoopSummaries.csv', 'w')
for book in finalLines:
	outputFile.write(book + '\n')




