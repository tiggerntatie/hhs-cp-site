__author__ = 'ericdennison'

choice = None
while choice != "none":
    area = None
    choice = input("Find area of a square, rectangle, triangle, parallelogram, trapezoid or kite (or none)? ")
    if choice == "square":
        base = float(input("What is the side length? "))
        area = base**2
    elif choice in ["rectangle", "parallelogram"]:
        base = float(input("What is the base length? "))
        height = float(input("What is the height? "))
        area = base*height
    elif choice == "triangle":
        base = float(input("What is the base length? "))
        height = float(input("What is the height? "))
        area = 0.5*base*height
    elif choice == "trapezoid":
        base1 = float(input("What is one base length? "))
        base2 = float(input("What is another base length? "))
        height = float(input("What is the height? "))
        area = height*(base1+base2)/2.0
    elif choice == "kite":
        diag1 = float(input("What is one diagonal length? "))
        diag2 = float(input("What is another diagonal length? "))
        area = diag1*diag2/2.0
    elif choice != "none":
        print ("I'm sorry: I don't know how to find the area of a {0}!".format(choice))
    if area != None:
        print ("The area is {0:.6}".format(area))
