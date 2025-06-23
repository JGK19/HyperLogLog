import random
import string
import math

from HyperLogLog import HLL

def main():
    N = 1000 # Numero de elementos distintos no conjunto
    b = 7
    numero_registradores = 2**b

    dados = gerar_strings_distintas(N, 7)
    dados_duplicados = dados+dados
    N_previsto = HLL(dados_duplicados, b)

    print(f"estimativa do Hyperloglog: {N_previsto}")
    print("ERRO:", abs(1 - (N_previsto/N)))
    print(f"Erro previsto do algoritimo: {1.04/math.sqrt(numero_registradores)}")

def gerar_strings_distintas(N, K):
    alfabeto = string.ascii_letters
    strings = set()

    while len(strings) < N:
        s = ''.join(random.choices(alfabeto, k=K))
        strings.add(s)

    return list(strings)

main()