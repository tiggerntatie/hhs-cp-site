'''
Created on Jan 18, 2013
@author: Jack
Prints a multiplication table.
'''

# Prompt the user to enter the table's width and height.
width = input("Width of multiplication table: ")
height = input("Height of multiplication table: ")

print ""

# Print the table.
for i in range(1, height + 1):
	for j in range(1, width + 1):
		print "{0:>3}".format(i*j),
	print ""