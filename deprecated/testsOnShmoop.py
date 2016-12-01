from collections import Counter

myshmoopfile = open("shmoopTrainThemes.csv", "r")
lines = myshmoopfile.readlines()

allthemes = []
for line in lines:
	line = line.split('\n')[0]
	linelist = line.split(';!')
	beginning = linelist[0]
	firstTheme = beginning.split(',')[-1]
	linelist[0] = firstTheme
	#allthemes.append(linelist[:4])
	allthemes.append(linelist)


themes = [item.lower() for sublist in allthemes for item in sublist]

newList = []

for theme in themes:
	if theme == 'sex and lust':
		newList.append('sex')
	elif 'war' in theme:
		newList.append('warfare')
	elif theme in ['technology', 'modernization and technology', 'technology & modernization']:
		newList.append('technology and modernization')
	elif theme in ['family/marriage', 'home and family']:
		newList.append('family')
	elif 'foreignness' in theme:
		newList.append('foreignness')
	elif 'philosoph' in theme:
		newList.append('philosophy')
	elif 'femin' in theme:
		newList.append('women and femininity')
	elif 'masculin' in theme:
		newList.append('men and masculinity')
	elif 'race' in theme:
		newList.append('race')
	elif theme == 'lust':
		newList.append('sex')
	elif 'sexual identity' in theme or theme=='sexuality':
		newList.append('sexual identity')
	elif 'alcohol' in theme:
		newList.append('drugs and alcohol')
	elif 'loyalty' in theme:
		newList.append('loyalty')
	elif 'lies' in theme or 'manipulation' in theme:
		newList.append('lies and deceit')
	elif theme=='faith':
		newList.append('religion')
	elif theme == 'good vs. evil' or theme == 'good versus evil':
		newList.append('morality and ethics')
	elif 'contrasting regions' in theme:
		newList.append('contrasting regions')
	elif 'justice' in theme:
		newList.append('justice')
	elif 'fate' in theme:
		newList.append('fate and free will')
	elif 'supernatural' in theme:
		newList.append('the supernatural')
	elif 'natural' in theme:
		newList.append('the natural world')
	elif 'language' in theme:
		newList.append('language and communication')
	elif 'memory' in theme:
		newList.append('memory and the past')
	elif 'death' in theme:
		newList.append('mortality')
	elif 'youth' in theme:
		newList.append('youth')
	elif theme == 'change':
		newList.append('transformation')
	elif theme == 'admiration':
		newList.append('awe and amazement')
	else:
		newList.append(theme)

themes = newList
print Counter(themes)

counts = Counter(themes)
newCounts =  Counter({k: counts for k, counts in counts.items() if counts >= 10})

print newCounts
print len(counts)
print len(newCounts)

for count in newCounts:
	print count