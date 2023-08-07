import random
import math

# To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

# pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

# pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
# We initially calculate a bound on the error probability
# An error can only occur when the remainder of the hash values of p and a substring of x is same
# In other words, q divides the difference of the hash values
# The difference can atmost be (26**m)-1
# log denotes logarithm with base 2 below
# Therefore the number of prime factors is less than log((26**m)-1)
# This is further less than log(26**m) which is m log(26)
# The number of possible values of q as a prime number from 1 to N is as per claim 2
# So the error probability is always less than maximum number of prime factors divided by number of possible values of q
# Thus we can say (m log(26) / pi(N)) < eps
# Opening up this inequality we get (N / log N) > k where k is as below
# k = 2 (m/eps) log(26)
# Thus, k must be greater than 2 log(26) which is about 9.4
# It can be checked by graphing that for N = 1.8 k log(k) satisfies the above inequality for all k >= 2 log(26)
# Thus, we obtain the below value of N
def findN(eps,m):
	k = 2 * (m/eps) * math.log(26,2)
	N = math.ceil(1.8*k*math.log(k,2))
	return N

# Return sorted list of starting indices where p matches x
# This function calculates remainders with q of the hash values of p and substrings of x
# Note that we keep taking remainder at each step to avoid exceeding space complexity
def modPatternMatch(q,p,x):

	# initialize the needed variables
	L = []
	funcp = 0
	funcx = 0
	remainder = 1

	# Calculating the remainder of hash values of p and first m-length substring of x
	iter = len(p)-1
	while iter >= 0:
		funcp = (funcp + (remainder*((ord(p[iter])-65) % q)) % q) % q
		funcx = (funcx + (remainder*((ord(x[iter])-65) % q)) % q) % q
		storerem = remainder
		remainder = (remainder * (26 % q)) % q

		iter -= 1

	# Comparing the values of f(p) mod q denoted by funcp and f(x[0.....m-1]) mod q denoted by funcx
	# If equality holds then we append to L
	if(funcp == funcx):
		L.append(0)

	# Iterating to compare funcp with funcx which denotes f(x[iter1.....iter1+m-1]) mod q in the iteration i
	iter1 = 1
	iter2 = len(p)
	numpatterns = len(x)-len(p)+1
	while iter1 < numpatterns:
		funcx = ((26*(funcx - (storerem*((ord(x[iter1-1])-65) % q) % q)) % q) + ((ord(x[iter2])-65) % q)) % q

		# If equality holds then we append to L
		if funcx == funcp:
			L.append(iter1)
		
		iter1 += 1
		iter2 += 1

	return L

# Return sorted list of starting indices where p matches x
# This function is very similar to modPatternMatch
# The difference is that we take into account '?'
# We do this by removing the remainder of hash value of position in x matching with '?'
def modPatternMatchWildcard(q,p,x):

	# Initialize the needed variables
	L = []
	funcp = 0
	funcx = 0
	remainder = 1

	# Iterate to calculate funcp and funcx
	# It also finds the position of '?' in p
	iter = len(p)-1
	while iter >= 0:
		if p[iter] == '?':
			wildcardint = iter
		else:
			funcp = (funcp + (remainder*((ord(p[iter])-65) % q)) % q) % q
		funcx = (funcx + (remainder*((ord(x[iter])-65) % q)) % q) % q	
		storerem = remainder
		remainder = (remainder * (26 % q)) % q

		iter -= 1
	
	# This gives us 26**(m-wildint-1) in mod q form
	power = 1
	for i in range(len(p)-wildcardint-1):
		power = (power * (26 % q)) % q

	# We keep track of original funcx
	# We then remove hash of matching position in mod q form
	# Now, we compare them
	funcxorig = funcx
	funcx -= (power*((ord(x[wildcardint])-65) % q)) % q
	funcx = funcx % q
	if(funcp == funcx):
		L.append(0)
	funcx = funcxorig

	# We repeat the above process (n-m) times to cover the possible substrings in x
	iter1 = 1
	iter2 = len(p)
	numpatterns = len(x)-len(p)+1
	while iter1 < numpatterns:
		funcx = ((26*(funcx - (storerem*((ord(x[iter1-1])-65) % q) % q)) % q) + (ord(x[iter2])-65) % q) % q
		funcxorig = funcx
		funcx -= (power*((ord(x[iter1+wildcardint])-65) % q)) % q
		funcx = funcx % q 
		if funcx == funcp:
			L.append(iter1)
		funcx = funcxorig

		iter1 += 1
		iter2 += 1

	return L