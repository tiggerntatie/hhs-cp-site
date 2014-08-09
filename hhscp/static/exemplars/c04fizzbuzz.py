__author__ = 'ericdennison'

maxn = int(input("How many numbers shall we print? "))
fizzn = int(input("For multiples of what number shall we print 'Fizz'? "))
buzzn = int(input("For multiples of what number shall we print 'Buzz'? "))

for n in range(1,maxn+1):
    fizzmultiple = not n % fizzn # % calculates remainder of division - zero if n is multiple of fizzn
    buzzmultiple = not n % buzzn # ditto..
    if fizzmultiple and buzzmultiple:   # check for both, first
        print("FizzBuzz")
    elif fizzmultiple:  # then individuals
        print("Fizz")
    elif buzzmultiple:
        print("Buzz")
    else:
        print(n)

