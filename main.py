import random
import math
from bitarray.util import int2ba
import struct
from bitarray.util import ba2int
import tonelli as tll
import sys


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

def formatting1(n, m):
    bit = len("{0:b}".format(n))
    l = math.ceil(len("{0:b}".format(n))/8)
    #r = generate_number([2**63, 2**64-1])
    r = 17633251709656066200
    pw = 8*(l-8)
    x = 255*(2**pw)+ m*(2**64) +r
    x = x%n
    correct = x > math.sqrt(n)
    print(correct)
    return int(x)


def formatting(n, m):
    bit = len("{0:b}".format(n))
    l = math.ceil(len("{0:b}".format(n))/8)
    l_m = math.ceil(len("{0:b}".format(m))/8)
    r = generate_number([2**63, 2**64-1])
    # print(l)
    # print(l_m)
    #r = 17633251709656066200
    zeros = (l - l_m -10) *2
    formatted = '0xff'
    for i in range(zeros):
        formatted += '0'
    formatted += str(hex(m))[2:]
    formatted += str(hex(r))[2:]
    x = int(formatted, 16)
    return x


def divide_2(p):
    a = int2ba(p)
    a.pop(-1)
    i = ba2int(a)
    return i

def jacobi(a, n):
    a = a%n
    assert (n > a > 0 and n % 2 == 1)
    t = 1
    while a != 0:
        while a % 2 == 0:
            #a /= 2
            a = divide_2(a)
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
    #(f'x formatted {x}')
    y = (x*(x+b)) %n
    c1 = (x+b_div_2)%n
    c1 = c1%2
    c2 =1 if jacobi((x+b_div_2) %n,n) ==1 else 0
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
    s1 = tll.tonelli(y%p, p)
    s2 = tll.tonelli(y%q, q)
    _, u,v = gcdExtended(p,q)
    x1 = (v*q*s1 + u*p*s2) %n
    x2 = (v*q*s1 - u*p*s2) %n
    x3 = (-v*q*s1 - u*p*s2) % n
    x4 = (-v*q*s1 + u*p*s2) % n
    return(x1,x2,x3,x4)

def check_c1_c2(x, c1, c2, n,b):
    c1x = (x + int(b / 2)) % n
    c1x = c1x % 2
    c2x = 1 if jacobi(x + int(b / 2), n) == 1 else 0
    if c1 == c1x and c2 == c2x:
        return (':)', c1x, c2x)
    else:
        return (':(',c1x, c2x)

def decrypt(y,c1,c2,b,n, p,q):
    two_minus = pow(2, -1, n) # b /2
    b_div_2 = (two_minus *b ) %n
    square = y+ pow(b_div_2, 2, n)
    r = square_mod(square, p,q)
    result = 0
    arr_x= {}
    for ri in r:
        xi = (ri - b_div_2) %n
        res, c1x, c2x  =  check_c1_c2(xi, c1, c2, n,b)
        arr_x[xi] = (c1x, c2x)
        if res == ':)':
            #return xi
            result = xi
    #print(f'arr_x is {arr_x}')
    return result


def sign(m,  p,q):
    while True:
        x =formatting(p * q, m)
        if jacobi(x,p) ==1 and jacobi(x,q) ==1:
            r = square_mod(x, p,q)
            return (m,random.choice(r))
    # else:
    #     return 'choose another x'

def get_original_message(x, n):
    s = str(hex(x))[4:]
    s = s[:-16]
    while s[0] == '0':
        s = s[1:]
    return int(s, 16)



def verify(m,s,n):
    #x = formatting(n, m)
    x1 = pow(s,2,n)
    message = get_original_message(x1, n)
    #message = int(message, 16)
    if message == m:
        return ':)'
    else:
        return ':('



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

def send_square_root(y, n, p,q):
    x1, x2, x3, x4 = square_mod(y,p,q)
    arr_x = [x1,x2,x3,x4]
    i = 0
    while True:
        res_p = jacobi(arr_x[i],p)
        res_q = jacobi(arr_x[i], q)
        if res_p == 1 and res_q == 1:
            return arr_x[i]
        i += 1


def attack(n):
    while True:
        t = generate_number([1,n])
        y = pow(t,2,n)
        print(f'y is {hex(y)}')
        print('please input z')
        z = input()
        z = int(z, 16)
        if t != z and t != n - z:
            p, _, _ = gcdExtended(t+z, n)
            if p != 1 and p != 0:
                print(n %p)
                return p

# sys.setrecursionlimit(2000)
# M = 0xE1D3B2060EF04CB49F96E512E34F5EDAEE4C61837DF8E2855296E8AC723FFBC006F9CD3375A65E9ED5FE863C2DD69004F4328D00FFC39FE77B6D88A15516A1CEBBB76C825CBBAA9BB2E2AAEE80E607EAE30E22BD8EEE6F45A5B02EB7666D8811292F90E6AA2CC7D3018193323EB8C9B77D56885D0F79631566B858A0B3495A41846D3BBC93CA1F83D8452CC6B8F8F2D41A2348C48C9863D4267308D257374DED6EBADA5D02037F9AA935BEAF11D6791C8E03BF33B7B9E7433D80D0B992CA291B66581AFC29A33FB6A64DC8748D02D27D8C168CBD6DDA25FFD78F3A877254F496394E5150281DE6799C4B60DD1AECCDF4193361FC3C78D23C22C52BE312331C35
# p = attack(M)
# print(p)
# t = 0x1daeb5a05741ad3769a56cc0cbf71deba19c62fe6c52c97dffad0c3b39fcf3771d2af614639775be93b51c3dea7498b3158b02614109860321b02bf4f1fa10cb9425501fa3a9f18a2dc3aafd2b8076ed9926943c8571e875da75c00ddecaa32214af9f673755e27beb43dc4b8324f30f20e37bd1cbb65d133305ba5fcf4904d7440721be9be73e889cb25c0a780fcc19ce8b35eafeb8f27f69e4c16760252e8299b2ea28dc7a66ab9df50116cdcec1485fea78b33d7edfffc987336700c56fa0a1126c3fb13a86730cc87af2985fd783277e1750043a002f444cac1182617987c06601802b2b550d9f99e08507038fb26ec4b13944f04c380c536ab7b0337fdf
# z = 0x3870E7144B2E2A7E84EF2F3ACB28C3CAE7AB1E9B3BF65A7D6D1123CA067E2998D93EB381838356608E6D15AE5237D3B970D9AD846F9393C01E2E9752563DE75D731084ADC031B209AB0C8D67F5E7CBE003F8CCD02774C9912A4144EC0DFCE21C05BC7F5E18692A4E521894C3FAB9FEED6EB64636331A5F30275AC7B8F9E79B07160245C87D73F1CEB3EFA3062F7B017AA12A29B784A9C71D78CEA1BD708F6FA04DF1FD59FEE01EFD8F8362966ADFD435D613ABCDE04402F5A445A4DD8039C61150D6DAF4F5E06F70CB308AA33502867AA1B59D9B219BD47996251C5FCC88F22F07D9E97D15489EA997F5457C3DEE1727F16ACE2635E94D5838D5791CB8D6C0B0
#


# p,q,b = generate_keys(2**256, 2**257)

#

n = 0x318a0c3335dfbf788646f504965f0791d1ec3dbfd5f26b78e9a5288067a64654aac07571f262f8d6b3e97be0c1f7124d7f57488a8a13c2dc96a40959b4ed4591d
p= 0x1ce2d8c6813bc5fbcd0a0f2fa6226486b8bb8aeac4cbefcb8f2e3f802edfd48f3
q = 0x1b7093982101cc2452dd7480f2486877142904ce1f91087772b1ba546732159af
m = 0x12
m1 = 0xABCDEF12345
n = p*q
b = 4
Modulus = 0x99FC85F0D888EDCD984A6FA2E129DE9D605778FC523C7E76F4E09BC4B16F31E5
B = 0x525C2034F5D7A33D6658D5FAE17A0D8F595A87676F7A96F6A35675ADFFB3E509
m_f = formatting(Modulus, m)

y,c1,c2 = encrypt(m1, Modulus,B)
print(f'y: {hex(y)}, c1: {c1}, c2: {c2}')
# print(f'formatted_message{hex(formatting(Modulus, m))}')
# print(f'n_hex: {hex(n)[2:]}, m_hex: {hex(m)[2:]}, b_hex :{hex(b)[2:]},'
#       f' p_hex:{hex(p)[2:]}, q_hex:{hex(q)[2:]}')
#
# m, signature = sign(m,  p,q)
# print(hex(m), hex(signature))
# s = 0x37FFFFDF6A745E0B0A2C7A50A3F8C3EAF18BDBF0138076C66A13085F23C6BFA8
# print(verify(m, s, Modulus))
# c = 0x02FE0A21B0F27CABE52EF52726A501031CFEC3D856A4ECD8E2BEDCC8046E6348F47CB6F7C2C67DA44D36AB7F53520FDF1ABC0F2921E54974224212DDFF484B70F8
# c1 = 1
# c2 = 1
# form_message =decrypt(c,c1,c2,b,n,p,q)
# message = get_original_message(form_message, n)
# print(hex(message))
# mod = 0xBE131D0D88854553237DD4D5F04FAEB4A15A5CE42B4F5435249D6614EF62C7DE063047AC1A8E9C2AFA47285C46EAD7B6574C8A728B9428C5DA3A92A4EF8378B4832138028949B75EC0211DBBB9E2334D8A5DF29DA33DA281A96C3D2758316F0A0221BBBA5FF5B44F574B705691D0BEF06A43BB5B7DAB732BDE225F2559AC52B6BC942AF06344742D25499A47094EFB9C1EABF24FD1365B5EECF7CA93548D33F16BD586E623C6D2615B85D3B669A7A7947D8FFE95EAB8F9F8A12840CD739555C15FC2F180DF73547805D751CBA6FC987E13C8ECB3DFA12E1878E5CFBC28A58FA58EDCEFE3E893E0809004930606B9CE222065F892489BC9A61E7AD762A4BC96D9
# print(hex(attack(mod)))