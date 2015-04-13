__author__ = 'ericdennison'
import datetime

name = input("Please tell me your name: ")
age = int(input("Please tell me your age: "))
pythonage = datetime.date.today().year-1989
print("Hello, {0}. Python is {1}  years older than you are!".format(name, pythonage-age))
