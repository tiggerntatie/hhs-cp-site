__author__ = 'ericdennison'

n = int(raw_input("I will estimate pi. How many terms should I use? "))
sigfigs = int(raw_input("How many sig figs should I use in the result? "))
pi = 4*sum([((-1)**k)/(2.0*k+1) for k in range(0,n)])
print("The approximate value of pi is {0:.{precision}}".format(pi,precision=sigfigs))