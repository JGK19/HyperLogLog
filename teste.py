import random
import string
import math
import hashlib

import mmh3

def position_1r(n):
    if n == 0:
        return 33  # Nenhum bit 1 presente
    return (n & -n).bit_length()


def alpha(m):
    match m:
        case 16:
            return 0.673
        case 32:
            return 0.697
        case 64:
            return 0.709
        case _ if m >= 128:
            return 0.7213 / (1 + (1.079 / m))
        case _:
            raise ValueError(f"Valor de m não suportado: {m}")

def gerar_strings_distintas(N, K):
    alfabeto = string.ascii_letters  # letras maiúsculas + minúsculas
    strings = set()

    while len(strings) < N:
        s = ''.join(random.choices(alfabeto, k=K))
        strings.add(s)

    return list(strings)

def gerar_lista_letras_mistas(N):
    return random.choices(string.ascii_letters, k=N)

def gerar_lista_letras(N):
    return random.choices(string.ascii_uppercase, k=N)

def divide_bits(n, b):
    mascara = (1 << b) - 1          
    bits_direita = n & mascara      
    resto = n >> b                  
    return bits_direita, resto

def hash32(s):
    h = hashlib.sha1(s.encode()).hexdigest()
    return int(h[:8], 16)

N = 1000
"""U = gerar_strings_distintas(N, 7)
U = U + U"""
U = gerar_lista_letras(N)
print(len(U))

b = 4
m = 2**b
M_registers = [0 for _ in range(m)]
print(N, m*math.log2(m))

for v in U:
    x = hash(v)
    j, w = divide_bits(x, b)
    M_registers[j] = max(M_registers[j], position_1r(w))

print(M_registers)
Z = sum(2 ** -Mj for Mj in M_registers)

E = alpha(m) * (m**2) * 1/Z

print("estimativa pura: ", E)

if E <= (5/2) * m:
    V = M_registers.count(0)
    if V != 0:
        E_star = m*math.log(m/V)
    else:
        E_star = E

elif E <= (1/30) * 2**32:
    E_star = E
else:
    E_star = -(2**32) * math.log(1 - (E/(2**32)))

print("estimativa final:", E_star)
print("ERRO:", abs(1 - (E_star/N)))
print(1.04/math.sqrt(m))