__author__ = 'ericdennison'

rawtext = input("Please enter a string of text (the bigger the better): ")

allreversed = rawtext[::-1]
allwords = rawtext.split()
allwordsinreverse = allwords[::-1]
allwordsreversed = [word[::-1] for word in allwords]

print ('You entered "{0}". Now jumble it: '.format(rawtext))
print(allreversed)
print(' '.join(allwordsinreverse))
print(' '.join(allwordsreversed))
