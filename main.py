import random
import math
from bitarray.util import int2ba
import struct
from bitarray.util import ba2int


def generate_number(range):
    r = random.randint(range[0], range[1])
    return r

def factor(p):
    a = int2ba(p)
    s = 0
    while a[-1] ==0:
        s+=1
        a.pop(-1)
    i = ba2int(a)
    return(s,i)
def miller_rabin(p):
    k = 50
    s,d = factor(p-1)
    #arr_x = [2,3,5,7]
    for i in range(k):

        x = generate_number([1,p-1])
        gcd = math.gcd(p,x)
        if gcd >1 :
            return 'not prime'
        pseudo_prime = False
        x_d = pow(x,d,p)
        if x_d == 1 or x_d == p-1:
            pseudo_prime = True
        else:
            for i in range(s):
                x_d =pow(x_d,2,p)
                if x_d == p-1:
                    pseudo_prime = True
                    break
                elif x_d == 1:
                    return 'not prime'
        if pseudo_prime == False:
                return 'not prime'
    return 'prime'

def generate_prime(n0, n1, k=100):
    for i in range(k):
        x = generate_number([n0, n1])
        m0 = x if x % 2 == 1 else x + 1
        interval = int((n1 - m0)/2)
        for j in range(interval):
            p = m0+ 2*j
            if miller_rabin(p) == 'prime':
                return p



def generate_p(n0, n1):
    answer = False
    while not answer:
        p  = generate_prime(n0, n1)
        if p%4 ==3:
            answer = True
            return p

def generate_keys(n0,n1):
    p = generate_p(n0,n1)
    q = generate_p(n0, n1)
    b = generate_p(n0, n1)
    return (p,q,b)

def format(n, m):
    l = len("{0:b}".format(n))/8
    r = generate_number([2**64, 2**65-1])
    x = 255*2**(8*(l-8))+ m*(2**64) +r
    return x

def jacobi(a, n):
    assert (n > a > 0 and n % 2 == 1)
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return t
    else:
        return 0

def encrypt(x,n,b):
    y = x*(x+b) %n
    c1 = (x+b/2)%n
    c1 = c1%2
    c2 =1 if jacobi(x+int(b/2),n) ==1 else 0
    return (y,c1,c2)


def gcdExtended(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y

def ktl(s1, s2, p, q):
    M = p*q
    M1 = int(M /p)
    M2 = int(M / q)
    _, f1, g1 = gcdExtended(p, M1)
    _, f2, g2 = gcdExtended(q, M2)
    x = s1*g1*M1+ s2*g2*M2
    x = x%M
    return x






def square_mod(y,p,q):
    n = p*q
    s1 = pow(y, int((p+1)/4), p)
    t1 = pow(s1, 2, p)
    s2 =pow(y, int((q+1)/4), q)
    t2 = pow(s2, 2, q)
    _, u,v = gcdExtended(p,q)
    x1 = ktl(s1,s2, p,q)
    x2 = ktl(p-s1,s2, p,q)
    x3 =ktl(s1,q-s2, p,q)
    x4 = ktl(p-s1,q-s2, p,q)
    # x1 = (u*p*s1 + v*q*s2) %n
    # x2 = (u*p*s1 - v*q*s2) %n
    # x3 = (-u*p*s1 + v*q*s2) %n
    # x4 = (-u*p*s1 - v*q*s2) %n
    return(x1,x2,x3,x4)
def decrypt(y,c1,c2,b,n):
    pass


print(square_mod(4,19,11))
