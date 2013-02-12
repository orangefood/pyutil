import math

def prime(max):
	primes=[2]
	n=3
	while n<=max:
		prime=True
		for p in primes:
			if n%p==0:
				prime=False
				break
		if prime:
			primes.append(n)
		n=n+2
	return primes
			

def prime_factor(n,primes=None):
	if n==1: return []
	fac=[]
	if primes==None: primes=prime(math.sqrt(n))
	for p in primes:
		if n%p==0:
			fac=prime_factor(n/p)
			fac.append(p)
			break;
	if len(fac)==0:
		fac.append(n)
	return sorted(fac)

def factors(n):
	import itertools
	primes=prime_factor(n)
	factors=[(p,) for p in primes]
	for i in range(2,len(primes)+1):
		factors=factors+[c for c in itertools.combinations(primes,i)]
	factors=list(set(factors))
	f =[1]*len(factors)
	for i in range(len(factors)):
		for m in factors[i]:
			f[i]=f[i]*m
	return [1]+sorted(f)


def cummul(m):
	a=[m[0]]*len(m)
	for i in range(1,len(m)): 
		a[i]=a[i-1]*m[i]
	return a

def rect(n):
	f=factors(n)
	a=f[len(f)/2]
	return sorted([a,n/a])




