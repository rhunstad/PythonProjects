#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 00:56:51 2020

@author: RyHunstad
"""


"""
MATHEMATICS: 
    
For prime p, with set N [n_1, n_2, ..., n_phi(p)] being the set of integers with 
cardinality phi(p) in the set [0, 1, ..., p-1] -- where phi(n) is the Euler Totient 
Function that gives the amount k of numbers 1 <= k <= n that are coprime to n, 
which for prime n, phi(n) = n-1 -- that are coprime to p (with such a set forming 
a multiplicative group of positive integers mod p {an Abelian group} under multiplication 
modulo p -- and via Euler's Totient Function for prime p, the multiplicative group 
is the same as the set [1, p-1]), 

g is said to be a primitive root modulo p if for every number n in the set N, 
there exists an integer k such that g^k mod p = n for every n. Further, for g that is a 
primitive root mod p and prime p, the operation g^k mod p is cyclical with period p-1. Another 
implication is g forms a generator set of the group N (i.e., for the set g where g is a subset 
of N and |g| = 1, the operation g^k mod n can be made to recreate all elements in group N). 
If there exists such a generator g in N, then there are a total of phi(phi(n)) generators total in N. 



DIFFIE HELLMAN KEY EXCHANGE: 

For a prime p and g such that g is a primite root mod p, Alice and Bob agree to use 
modulus p and base g where g is a primitive root (a generator) of p. 

Alice chooses a private integer a and sends Bob the result A, where A = g^a (mod p)
Bob does the same with private integer b and sends Alice the result B where B = g^b (mod p)
Alice then computes B^a mod p, and Bob computes A^b mod p, where B^a mod p = Z^b mod p (an implication
of the definition of the multiplicative group of integers mod p, an Abelian group under the 
operation multiplication mod p)

Thus, Alice and Bob both share a shared secret key where Alice does not know what b was 
and Bob does not know what a was. Further, this can be accomplished in (I believe) only 
at most 4 transmissions: (1) message from Alice to Bob initiating the exchange wherein she sends 
Bob a suggested p and g as well as her calculated key A, (2) Bob receives A, p and g, and 
if he agrees to use them he computes the full key, and sends his side of the shared secret B {see above} 
to Alice in the second transmission, after which both Alice and Bob have the full shared 
secret key but neither of them know a or b. 

"""


from cryptography.fernet import Fernet
from random import randint
import math
import hashlib
import base64



# Perform the main key determination and exchange
def main():
    scale = int(input("Enter byte-length to use for numbers p, a, b (warning: anything >10 takes a long time): "))
    p = find_prime(2**(scale+1)-1)
    
    # group = multiplicative_group(p)  # Commented out because it took too long and was redundant
    group = list(range(1, p))
    g = find_g(group, p)                        # Find a small generator/primitive root g
    a = randint(2**scale, 2**(scale+1)-1)       # Randomly generate a and b with user's specified length
    b = randint(2**scale, 2**(scale+1)-1)
    key = confirm(g, p, a, b)                   # Checks to see if the 2 asymmetric keys match
    if key:                                     # If key is not False, it is a list containing the numeric key
        key = str(key).encode("utf-8")
        print("Diffie-Hellman shared secret number: ", key)
        
        key = base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', key, key, 100000))
        print("DH shared secret (hashed in sha256): ", key)
        
        f = Fernet(key)             # Generate key
        
        usr = input("Enter message to be encrypted: ")
        enc = f.encrypt(usr.encode("utf-8"))
        print("Encrypted message: ", enc)
        dec = f.decrypt(enc)
        print("Decrypted Message: ", dec)
    else:
        print("Nope :/")


# Confirms that the equation balances and the exchange was performed properly:
def confirm(g, p, a, b):
    if ((((g**a) % p)**b) % p) == ((((g**b) % p)**a) % p):
        key = ((((g**b) % p)**a) % p)
        return key
    else:
        return False
    
    
# Tests if a number is prime, returns True if such
def is_prime(p):
    if p < 2:
        return False
    elif p == 2:
        return True
    for num in range(2, math.floor(p/2)+1):
        if p % num == 0:
            return False
    return True


# Tests to see if two numbers are coprime -- that is, they share no common factors other than 1
def are_coprime(p, q):
    q_fac = factorize(p)
    p_fac = factorize(q)
    len1 = len(p_fac) + len(q_fac)
    len2 = len(list(dict.fromkeys(p_fac + q_fac)))      
    # By converting to dict and back to list I eliminate duplicates, and if the 2 lists have more than 1
    # duplicate, the number of elements in the new list will be less than the old list minus 1    
    if len2 + 1 < len1:
        return False
    else:
        return True
    

# returns True if g is a generator (see definition above) of p, False if not
def is_generator(g, p):
    if not is_prime(p): 
        return False
    
    mult_group = list(range(1, p))
    coprimes = []
    for k in mult_group:
        val = (g**k) % p
        if val in mult_group:
            coprimes.append(val)
            
    if sorted(coprimes) == mult_group:
        return True
    else:
        return False
        
    
    
# Finds and returns the multiplicative group (see definition above) of prime p:
def multiplicative_group(p):
    group = []
    for n in range(p):
        if are_coprime(n, p):
            group.append(n)
    return group


# Finds the first prime less than or equal to p: 
def find_prime(p):
    for i in range(p, 1, -1):
        if is_prime(i):
            return i


# Finds a generator in the multiplicative group of integers mod p
def find_g(group, p):
    for num in group:
        if is_generator(num, p):
            return num


# Finds the factors of n and returns them as a list: 
def factorize(n):
    factors = []
    for i in range(1, n+1):
        if n % i == 0:
            factors.append(i)
    return factors
            

main()

# ---------------------------------------------------------------------------#

#***************    -      Deprecated Methods:  -        ********************#

    
# # convert user-defined string (i.e. takes string to be a number in base-128) and converts to 
# # base-10 for use as the private integer in the Diffie-Hellman Key Exchange
# def string_to_int(string):
#     count = len(string)-1
#     base10 = 0
#     for char in list(string):
#         charval = ord(char)*(128**count)
#         base10 += charval
#         count += -1
#     return base10


# # Convert from Python base-10 int back into base-128 (ASCII) string
# def int_to_string(base10):
#     base64map = {1:"A", }
#     string = ""
#     place = 0
#     while 128**place < base10:
#         place += 1
#     place += -1
#     for i in range(place, -1, -1):
#         num = 128**i
#         string += (chr(math.floor(base10/num)))
#         base10 = base10 % num
#     return string
    