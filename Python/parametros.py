# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt

# === CONFIGURAÇÕES ===
arquivo_dados = r"C:\Users\User\Desktop\IC\Testes\5Hz_1_0T.CSV"
coluna_tempo = "TIME"
coluna_v1 = "CH1"       # tensão primária
coluna_i1 = "CH2"       # corrente primária
coluna_v2 = "CH3"       # tensão secundária
f = 5  # Hz (ajuste conforme o ensaio)

# Relação de espiras (N1/N2)
n = 152/740

# Parâmetros do modelo
Ls = 0.00000001439005919   # H

# === LEITURA DO ARQUIVO ===
df = pd.read_csv(arquivo_dados)

tempo = df[coluna_tempo].values
v1 = df[coluna_v1].values
i1 = df[coluna_i1].values
v2 = df[coluna_v2].values

# --- Cálculo do passo de tempo e número de amostras por ciclo ---
dt = tempo[1] - tempo[0]           # passo de amostragem
T = 1 / f                         # período de uma senoide
n_amostras_ciclo = int(round(T / dt))  # amostras por ciclo

# --- Seleciona apenas o último ciclo ---
tempo = tempo[-n_amostras_ciclo:]
v1 = v1[-n_amostras_ciclo:]
i1 = i1[-n_amostras_ciclo:]
v2 = v2[-n_amostras_ciclo:]

# --- Ajusta o vetor de tempo para começar em zero ---
tempo = tempo - tempo[0]
tempo_total = tempo[-1] - tempo[0]

# --- Converte v2 para o referencial do primário ---
v2_ref = v2 * n

# --- Potências instantâneas ---
p_total_inst = v1 * i1
p_ferro_inst = v2_ref * i1

# --- Integração (apenas no último ciclo) ---
energia_total = trapezoid(p_total_inst, x=tempo)
energia_ferro = trapezoid(p_ferro_inst, x=tempo)

P_total_media = energia_total / tempo_total
P_ferro_media = energia_ferro / tempo_total

# --- RMS considerando apenas o último ciclo ---
i1_rms = np.sqrt(trapezoid(i1**2, x=tempo) / tempo_total)
v1_rms = np.sqrt(trapezoid(v1**2, x=tempo) / tempo_total)
v2_rms = np.sqrt(trapezoid(v2_ref**2, x=tempo) / tempo_total)

# --- Resistência série e ramo magnetização ---
Rs = (P_total_media - P_ferro_media) / (i1_rms**2)
Rm = v2_rms**2 / P_ferro_media

# --- Cálculo de Lm pelo método da potência reativa ---
omega = 2 * np.pi * f
V1_rms = v1_rms
I1_rms = i1_rms
P_total = P_total_media

S = V1_rms * I1_rms
Q_total = np.sqrt(max(0.0, S**2 - P_total**2))

Xls = omega * Ls
Q_ls = (I1_rms**2) * Xls
Q_m = Q_total - Q_ls

# === RESULTADOS ===
print(f"Passo de amostragem dt = {dt:.6e} s")
print(f"Amostras por ciclo = {n_amostras_ciclo}")
print(f"Tempo total usado (1 ciclo) = {tempo_total:.6e} s")
print(f"Potência média total = {P_total_media:.8f} W")
print(f"Potência média ferro = {P_ferro_media:.8f} W")
print(f"Corrente RMS = {i1_rms:.8f} A")
print(f"Tensão V1 RMS = {v1_rms:.8f} V")
print(f"Tensão V2 referida ao primário RMS = {v2_rms:.8f} V")
print(f"Resistência equivalente Rs = {Rs:.8f} ohms")
print(f"Resistência equivalente Rm = {Rm:.8f} ohms")
print(f"Q_total = {Q_total:.6e} var")
print(f"Q_ls = {Q_ls:.6e} var")
print(f"Q_m = {Q_m:.6e} var")

if Q_m > 0:
    X_m = V1_rms**2 / Q_m
    L_m = X_m / omega
    print(f"X_m = {X_m:.6e} ohm")
    print(f"L_m = {L_m:.8e} H")
else:
    print("Atenção: Q_m <= 0, não foi possível calcular Lm real positivo.")

# --- Gráficos ---
plt.figure(figsize=(8,4))
plt.plot(tempo, v1, label="V1 (Primário)")
plt.plot(tempo, i1, label="I1 (Primário)")
plt.plot(tempo, v2_ref, label="V2 (referida ao primário)")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.title("Último Ciclo - Tensões e Corrente")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,4))
plt.plot(tempo, p_total_inst, label="Potência Instantânea Total (V1*I1)")
plt.plot(tempo, p_ferro_inst, label="Potência Instantânea Ferro (V2_ref*I1)", alpha=0.7)
plt.axhline(P_total_media, color='red', linestyle='--', label=f"Ptotal média = {P_total_media:.4f} W")
plt.axhline(P_ferro_media, color='green', linestyle='--', label=f"Pferro média = {P_ferro_media:.4f} W")
plt.xlabel("Tempo (s)")
plt.ylabel("Potência (W)")
plt.title("Potência Instantânea (Último Ciclo)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()






