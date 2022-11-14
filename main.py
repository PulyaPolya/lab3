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
    x = formatting(n, m)
    y = (x*(x+b)) %n
    c1 = (x+int(b/2))%n
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
    s2 =pow(y, int((q+1)/4), q)
    _, u,v = gcdExtended(p,q)
    x1 = ktl(s1,s2, p,q)
    x2 = ktl(p-s1,s2, p,q)
    x3 =ktl(s1,q-s2, p,q)
    x4 = ktl(p-s1,q-s2, p,q)
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
    r = square_mod((y+ int((b**2)/4)), p,q)
    for ri in r:
        xi = (ri - int(b/2)) %n
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


p = 23
q = 19
n = p*q
b = 4
m = 9
y,c1,c2 = encrypt(m,n,b)
print(decrypt(y,c1,c2,b,n, p,q))
print(formatting(n,m)%n)
#r = generate_number([2**63, 2**64-1])          aaaaa

# m = 0xaa
# modulus = 0x18D7B2F50DCA40E0561937466D9FB993D
# B = 0xAA9E0A5D813E5F09FF281CFF4B35F05F
# y, c1, c2 = encrypt(m,modulus,B)
# print(hex(y))
# print(c1,c2)
# print(hex(formatting(modulus, m)))
# n = 0x2e120fbdb44536538345cc655555e218cebd45f652a7954ffacf0ffb3e75acd6e2ba1c35deadf133350115efe74a4ecc2843d1ecd07792e1ccc63085e6b622e99
# b = 0x3b72e9b87ff3b733a1c3489d6538f31203d8cb16f9a7d3dd3bd4da8874e30020f
# p = 0x1e57939d2858ed470359bec519c35528120986693856517e9e2c1749affe0f96b
# q = 0x184b3f2cecc551b18f97a788e7975c73a769dc6f9afd9f6f252d329065dc1250b
# # p,q,b = generate_keys(2**256, 2**258)
# # print(f'n_hex: {hex(n)[2:]}, m_hex: {hex(m)[2:]}, b_hex :{hex(b)[2:]},'
# #       f' p_hex:{hex(p)[2:]}, q_hex:{hex(q)[2:]}')
# cipher =0xD801C655D55A61DEC96DB0577E80284948E94E5C4DF213565BC289ED6F68B2778526095BCF7AE02B745F0F601C130F422CC13918D575BEBCECF7DB4682807CAC
# print(decrypt(cipher,0,0,b,n, p,q))
# print(format(n,m))