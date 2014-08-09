'''
Created on Jan 18, 2013
@author: Jack
Prints a multiplication table.
'''

# Prompt the user to enter the table's width and height.
width = int(input("Width of multiplication table: "))
height = int(input("Height of multiplication table: "))

print ("")

# Print the table.
for i in range(1, height + 1):
	for j in range(1, width + 1):
		print ("{0:>4}".format(i*j), end="")
	print ("")