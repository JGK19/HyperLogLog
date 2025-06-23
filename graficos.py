import matplotlib.pyplot as plt
import random
import string
import math

# === Funções HyperLogLog ===

def alpha(m):
    if m == 16:
        return 0.673
    elif m == 32:
        return 0.697
    elif m == 64:
        return 0.709
    elif m >= 128:
        return 0.7213 / (1 + 1.079 / m)
    else:
        raise ValueError("Valor de m não suportado")

def position_1r(n):
    if n == 0:
        return 33
    return (n & -n).bit_length()

def divide_bits(n, b):
    mascara = (1 << b) - 1
    bits_direita = n & mascara
    resto = n >> b
    return bits_direita, resto

def HLL(U, b):
    m = 2**b
    M_registers = [0 for _ in range(m)]

    for v in U:
        x = hash(v)
        j, w = divide_bits(x, b)
        M_registers[j] = max(M_registers[j], position_1r(w))

    Z = sum(2 ** -Mj for Mj in M_registers)
    E = alpha(m) * (m ** 2) / Z

    if E <= (5 / 2) * m:
        V = M_registers.count(0)
        if V != 0:
            E_star = m * math.log(m / V)
        else:
            E_star = E
    elif E <= (1 / 30) * 2 ** 32:
        E_star = E
    else:
        E_star = -(2 ** 32) * math.log(1 - (E / 2 ** 32))

    return E_star

# === Funções auxiliares ===

def gerar_strings_distintas(N, K):
    alfabeto = string.ascii_letters
    strings = set()
    while len(strings) < N:
        s = ''.join(random.choices(alfabeto, k=K))
        strings.add(s)
    return list(strings)

# === Parâmetros ===

conjuntos = {
    'pequeno (N=500)': 500,
    'médio (N=10_000)': 10_000,
    'grande (N=1_000_000)': 1_000_000
}
bs = list(range(4, 13))  # b de 4 a 12
resultados = {nome: [] for nome in conjuntos}
erros = {nome: [] for nome in conjuntos}

# === Execução ===

for nome, N in conjuntos.items():
    dados = gerar_strings_distintas(N, 7)
    dados_duplicados = dados + dados  # simula multiconjunto
    for b in bs:
        estimativa = HLL(dados_duplicados, b)
        erro_relativo = abs(1 - (estimativa / N))
        resultados[nome].append(estimativa)
        erros[nome].append(erro_relativo)

# === Gráficos ===

fig, axs = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico de estimativa
for nome, N in conjuntos.items():
    axs[0].plot(bs, resultados[nome], label=nome)
    axs[0].hlines(N, xmin=bs[0], xmax=bs[-1], linestyles='dotted', colors='gray')

axs[0].set_title("Estimativa de cardinalidade vs b")
axs[0].set_xlabel("b (bits para registradores)")
axs[0].set_ylabel("Estimativa")
axs[0].legend()
axs[0].grid(True)

# Gráfico de erro relativo
for nome in conjuntos:
    axs[1].plot(bs, erros[nome], label=nome)

# Linha do erro teórico: 1.04 / sqrt(m)
erro_teorico = [1.04 / math.sqrt(2**b) for b in bs]
axs[1].plot(bs, erro_teorico, label="Erro teórico $\\frac{1.04}{\\sqrt{m}}$", linestyle='dotted', color='black')

axs[1].set_title("Erro relativo vs b")
axs[1].set_xlabel("b (bits para registradores)")
axs[1].set_ylabel("Erro relativo")
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
