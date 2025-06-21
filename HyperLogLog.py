import math

def HLL(U, b):
    m = 2**b
    M_registers = [0 for _ in range(m)]

    for v in U:
        x = hash(v)
        j, w = divide_bits(x, b)
        M_registers[j] = max(M_registers[j], position_1r(w))
    
    Z = sum(2 ** -Mj for Mj in M_registers)
    E = alpha(m) * (m**2) * 1/Z

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

    return E_star


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


def position_1r(n):
    if n == 0:
        return 33  # Nenhum bit 1 presente
    return (n & -n).bit_length()

def divide_bits(n, b):
    mascara = (1 << b) - 1          
    bits_direita = n & mascara      
    resto = n >> b                  
    return bits_direita, resto