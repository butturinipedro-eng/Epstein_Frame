# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 19:14:43 2025

@author: pedro
"""


# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate

# ---------------- CONFIGURAÇÃO (edite só estes caminhos) ----------------
arquivo_tensao   = r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 1\25C_2\1T 60Hz\Tensao_1T_60Hz_25C_C1_1.csv"
arquivo_corrente = r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 1\25C_2\1T 60Hz\Corrente_1T_60Hz_25C_C1_1.csv"
pasta_saida = r"C:\Users\pedro\Desktop\50C\1T 30Hz"  # onde salvar .png
os.makedirs(pasta_saida, exist_ok=True)

# Parâmetros do núcleo e ensaio (ajuste se necessário)
Np = 152               # número de espiras primário
Ns = 740              # número de espiras secundário
L_mag = 0.94          # comprimento magnético (m)
fm = 60               # frequência (Hz) - usada caso não exista coluna de tempo
A_Lam = 7.98e-06  # área da seção magnética (m^2)
Dens_Aco = 7650       # densidade do aço (kg/m^3)
# -------------------------------------------------------------------------

def read_csv_tolerant(path):
    """Lê CSV e retorna DataFrame; levanta erro claro se falhar."""
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise IOError(f"Erro ao ler '{path}': {e}")
    return df

def find_column_by_keyword(columns, keywords):
    """Retorna primeira coluna cujo nome contém qualquer keyword (case-insensitive)."""
    cols = list(columns)
    lowcols = [c.lower().strip() for c in cols]
    for kw in keywords:
        for i, lc in enumerate(lowcols):
            if kw.lower() in lc:
                return cols[i]
    return None

# --- Leitura ---
df_v = read_csv_tolerant(arquivo_tensao)
df_i = read_csv_tolerant(arquivo_corrente)

# --- detectar colunas (tolerante com espaços/case) ---
# procura coluna tempo em qualquer um dos arquivos (prefer df_v)
time_col_v = find_column_by_keyword(df_v.columns, ["time", "tempo", "t "])
time_col_i = find_column_by_keyword(df_i.columns, ["time", "tempo", "t "])
time_col = time_col_v or time_col_i  # prefere tensão, senão corrente

# detectar colunas de tensão e corrente pelos nomes 'volt' / 'voltage' e 'curr' / 'current' ou 'multiport'
voltage_col = find_column_by_keyword(df_v.columns, ["voltage", "volt", "tensao", "multiport"])
current_col = find_column_by_keyword(df_i.columns, ["current", "corr", "i ", "multiport"])

# se não encontrou com heurística, tenta fallback por posição (segunda coluna comum)
if voltage_col is None:
    # se df_v tiver mais de 1 coluna, pega a segunda coluna; senão a primeira
    voltage_col = df_v.columns[1] if df_v.shape[1] > 1 else df_v.columns[0]
if current_col is None:
    current_col = df_i.columns[1] if df_i.shape[1] > 1 else df_i.columns[0]

# --- Avisos com as colunas detectadas ---
print("Colunas detectadas:")
print(f" Tensão file: '{os.path.basename(arquivo_tensao)}' -> voltage_col = '{voltage_col}'")
print(f" Corrente file: '{os.path.basename(arquivo_corrente)}' -> current_col = '{current_col}'")
if time_col:
    print(f" Tempo detectado em coluna: '{time_col}'")
else:
    print(" Tempo não detectado nos CSVs -> será gerado a partir de fm (período).")

# --- extrair vetores ---
v_raw = df_v[voltage_col].values.astype(float)
i_raw = df_i[current_col].values.astype(float)

# sincronizar tamanho
num_dados = min(len(v_raw), len(i_raw))
v = v_raw[:num_dados]
i = i_raw[:num_dados]


# --- montar tempo: preferir coluna de tempo se existir ---
if time_col is not None:
    # escolhe a coluna de tempo do arquivo que a contém
    if time_col in df_v.columns:
        t = df_v[time_col].values.astype(float)[:num_dados]
    else:
        t = df_i[time_col].values.astype(float)[:num_dados]
    # garantir monotonicidade e reamostrar se necessário não é feito aqui; assume dados já temporais
else:
    # gerar um vetor de um período com num_dados pontos
    t = np.linspace(0.0, 1.0/fm, num_dados)

# --- cálculos numéricos robustos com compatibilidade SciPy --- 
# cumulative trapezoid (fallback para cumtrapz)
if hasattr(integrate, "cumulative_trapezoid"):
    cumtrap = integrate.cumulative_trapezoid
else:
    # antigo nome
    cumtrap = integrate.cumtrapz

# trapezoid (fallback)
if hasattr(integrate, "trapezoid"):
    trap = integrate.trapezoid
else:
    trap = integrate.trapz

# Campo magnético H(t)
H = (Np / L_mag) * i

# Fluxo magnético (integra tensão)
phi = cumtrap(v, t, initial=0)  # phi(t) = integral v dt
# remover DC offset do fluxo / integral
phi = phi - np.mean(phi)

# B(t)
B = phi / (Ns * A_Lam)

# área de histerese (J/m^3 por ciclo) e perdas (W/kg)
area_histerese = abs(trap(B, H))
perdas_histerese = fm * area_histerese / Dens_Aco

print("\nResultados:")
print(f" Área do ciclo de histerese = {area_histerese:.6e} J/m^3 por ciclo")
print(f" Perdas por histerese = {perdas_histerese:.6e} W/kg")

# --- nome base para salvar, baseado no nome do arquivo de tensão (pode usar ambos) ---
def clean_name(name):
    base = os.path.splitext(os.path.basename(name))[0]
    # substituir espaços e caracteres problemáticos
    base = base.replace(" ", "_").replace("-", "_")
    return base

tag_v = clean_name(arquivo_tensao)
tag_i = clean_name(arquivo_corrente)
tag = f"{tag_v}__{tag_i}"  # tag combinada para identificar o teste

# função que mostra e salva (um por vez)
def show_and_save(fig, filename):
    outpath = os.path.join(pasta_saida, filename)
    fig.savefig(outpath, dpi=300, bbox_inches="tight")
    print(f"✅ Salvo: {outpath}")
    plt.show()   # exibe e bloqueia até janela fechada

# --- Gráficos individuais (A: um por vez) ---
# 1) B(t)
fig = plt.figure(figsize=(8,4))
plt.plot(t, B)
plt.title("Densidade de Fluxo Magnético B(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("B [T]")
plt.grid(True)
fname = f"B_t_{tag}.png"
show_and_save(fig, fname)
plt.close(fig)

# 2) H(t)
fig = plt.figure(figsize=(8,4))
plt.plot(t, H)
plt.title("Intensidade de Campo Magnético H(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("H [A/m]")
plt.grid(True)
fname = f"H_t_{tag}.png"
show_and_save(fig, fname)
plt.close(fig)

# 3) v(t)
fig = plt.figure(figsize=(8,4))
plt.plot(t, v)
plt.title("Tensão v(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("Tensão [V]")
plt.grid(True)
fname = f"Tensao_t_{tag}.png"
show_and_save(fig, fname)
plt.close(fig)

# 4) i(t)
fig = plt.figure(figsize=(8,4))
plt.plot(t, i)
plt.title("Corrente i(t)")
plt.xlabel("Tempo [s]")
plt.ylabel("Corrente [A]")
plt.grid(True)
fname = f"Corrente_t_{tag}.png"
show_and_save(fig, fname)
plt.close(fig)

# 5) Curva BH
fig = plt.figure(figsize=(6,6))
plt.plot(H, B, "-")
plt.title("Curva de Histerese B x H")
plt.xlabel("H [A/m]")
plt.ylabel("B [T]")
plt.grid(True)
fname = f"BH_{tag}.png"
show_and_save(fig, fname)
plt.close(fig)

print("\nTodos os gráficos mostrados e salvos.")
