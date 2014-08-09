__author__ = 'ericdennison'

# The purpose of this exercise is to build facility and skill with lists and conditionals

# Accept an arbitrary string of text from the user, strip out all spaces, and figure out how many of each character
# are present in the text. For example: "Python is the coolest computer language ever!"

#eeeeee
#oooo
#tttt
#aa
#cc
#gg
#hh
#ll
#nn
#pp
#rr
#ss
#uu
#i
#m
#v
#y

import string

originaltext = input("Please enter a string of text (the bigger the better): ")
text = originaltext.lower()
counts = [text.count(c) for c in string.ascii_lowercase]  # build a list with character counts for a, b, c, etc..
pairs = list(zip(counts,string.ascii_lowercase))  # zip the counts together with the characters
pairs.sort(key = lambda pair: (-pair[0],pair[1]) ) # for each (count, letter) item, sort as if (-count, letter)
pairs = filter(lambda x: x[0] != 0, pairs) # remove empties
stringbars = [x*y for x,y in pairs] # build "bars" of characters
print ("The distribution of characters in \"{0}\" is:".format(originaltext))
for s in stringbars:
    print (s)

