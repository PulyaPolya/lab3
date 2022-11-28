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

def formatting(n, m):
    bit = len("{0:b}".format(n))
    l = math.ceil(len("{0:b}".format(n))/8)
    #r = generate_number([2**63, 2**64-1])
    r = 17633251709656066200
    pw = 8*(l-8)
    x = 255*(2**pw)+ m*(2**64) +r
    x = x%n
    correct = x > math.sqrt(n)
    return int(x)

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

def encrypt(m,n,b):
    two_minus = pow(2, -1, n)  # b /2
    b_div_2 = (two_minus * b) % n
    x = formatting(n, m)
    y = (x*(x+b)) %n
    c1 = (x+b_div_2)%n
    c1 = c1%2
    c2 =1 if jacobi(x+b_div_2,n) ==1 else 0
    print(f'c1: {c1}, c2: {c2}')
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
    print(f'p: {p}, q: {q}')
    s1 = pow(y, int((p+1)/4), p)
    print(f'y, {y}')
    print(f'q%4 {q%4}')
    print(f'int((q + 1) / 4): {int((q + 1) / 4)}')
    s2 = pow(y, int((q + 1) / 4), q)
    print(f's2 is {s2}')
    print(f's1**2 mod p: {pow(s1,2,p)}')
    print(f'y mod p: { y % p}')
    print(f's2**2 mod q: {pow(s2, 2, q)}')
    print(f'y mod q: {y % q}')

    _, u,v = gcdExtended(p,q)
    x1 = (v*q*s1 + u*p*s2) %n
    x2 = (v*q*s1 - u*p*s2) %n
    x3 = (-v*q*s1 - u*p*s2) % n
    x4 = (-v*q*s1 + u*p*s2) % n
    print(f'y is {y}')
    print(f'x1**2 is {pow (x1,2,n)}')
    print(f'x2**2 is {pow(x2, 2, n)}')
    # x1 = ktl(s1,s2, p,q)
    # x2 = ktl(p-s1,s2, p,q)
    # x3 =ktl(s1,q-s2, p,q)
    # x4 = ktl(p-s1,q-s2, p,q)
    print(f'x1: {x1}, x2: {x2},x3: {x3}, x4: {x4}')
    return(x1,x2,x3,x4)

def check_c1_c2(x, c1, c2, n,b):
    c1x = (x + int(b / 2)) % n
    c1x = c1x % 2
    c2x = 1 if jacobi(x + int(b / 2), n) == 1 else 0
    if c1 == c1x and c2 == c2x:
        return ':)'
    else:
        return ':('

def decrypt(y,c1,c2,b,n, p,q):
    two_minus = pow(2, -1, n) # b /2
    b_div_2 = (two_minus *b ) %n
    square = y+ pow(b_div_2, 2, n)

    print(f'square {square}')
    r = square_mod(square % n, p,q)
    for ri in r:
        print(f'ri**2: {pow(ri, 2,n)}')
        xi = (ri - b_div_2) %n
        res =  check_c1_c2(xi, c1, c2, n,b)
        if res == ':)':
            return xi


def sign(m,  p,q):
    x =formatting(p * q, m)
    if jacobi(x,p) ==1 and jacobi(x,q) ==1:
        r = square_mod(x, p,q)
        return (m,random.choice(r))
    else:
        return 'choose another x'

def verify(m,s,n):
    x = formatting(n, m)
    x1 = pow(s,2,n)
    if x1 == x:
        return 'true'
    else:
        return 'false'


# p = 23

def bit_to_byte(sequence):
    n = len(sequence)
    resulting_len = math.floor(n/8)
    bait_arr = []
    rest = n %8
    for i in range(0,n - rest, 8):
        bin = sequence[i: i+8]
        res = int("".join(str(x) for x in bin), 2)
        bait_arr.append(res)
    if rest > 0:
        residue = sequence[-rest:]
        arr = [0]*(8-rest)
        arr += residue
        res = int("".join(str(x) for x in arr), 2)
        bait_arr.append(res)
    return bait_arr

def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]


#p,q,b = generate_keys(2**40, 2**56)
p = 0x946b4e797dce9f
q = 0xc40b9c0ac0cb5b #incorrect
# p = 0x2e02acbdaa8f  #correct
# q = 0x1640db0a96e3
# p =31
# q = 19
n = p*q
b = 4
m = 0xa
print(f'n_hex: {hex(n)[2:]}, m_hex: {hex(m)[2:]}, b_hex :{hex(b)[2:]},'
      f' p_hex:{hex(p)[2:]}, q_hex:{hex(q)[2:]}')

y,c1,c2 = encrypt(m,n,b)
print(decrypt(y,c1,c2,b,n, p,q))
print(formatting(n,m)%n)


