# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def analisar_configuracao(files, titulo, save_dir):
    """Lê 5 arquivos CSV, combina os dados, calcula médias e plota boxplot."""
    series = []
    medias_individuais = []

    # --- Leitura dos arquivos ---
    for file in files:
        df = pd.read_csv(file)
        p = df["Peak Detector17:4"]
        series.append(p)
        medias_individuais.append(p.mean())

    # --- Combina todas as séries ---
    todos_valores = np.hstack(series)  # junta todos os valores dos 5 arquivos
    media_total = np.mean(medias_individuais)  # média das 5 medições

    # --- Impressão ---
    print(f"\nConfiguração: {titulo}")
    print(f"Média total (5 arquivos): {media_total:.6f}")

    # --- Gráfico ---
    plt.figure(figsize=(6,4))
    plt.boxplot([todos_valores], positions=[1], labels=['Medições'], showfliers=True)
    plt.scatter(2, media_total, color='red', s=80, zorder=3, label='Média dos dados')

    plt.xlim(0.5, 2.5)
    plt.xticks([1,2], ['Medições', 'Média'])
    plt.ylabel('Perdas (W/kg)', fontsize=14)
    plt.title(titulo, fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.tick_params(axis='both', which='major', labelsize=13)

    # --- Salvar figura ---
    filename = titulo.replace(" ", "_").replace("/", "_") + ".png"
    filepath = os.path.join(save_dir, filename)
    plt.savefig(filepath, dpi=300)
    print(f"✅ Gráfico salvo em: {filepath}")

    plt.show()


def main():
    # --- Pasta onde os gráficos serão salvos ---
    save_dir = r"C:\Users\User\Desktop\IC\Imagens\Conjunto 2"
    os.makedirs(save_dir, exist_ok=True)

    # --- Caminhos dos arquivos ---
    files_1T = [
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1T_30Hz_100C_1.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1T_30Hz_100C_2.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1T_30Hz_100C_3.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1T_30Hz_100C_4.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1T_30Hz_100C_5.csv"
    ]

    files_15T = [
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_5T_30Hz_100C_1.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_5T_30Hz_100C_2.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_5T_30Hz_100C_3.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_5T_30Hz_100C_4.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_5T_30Hz_100C_5.csv"
    ]

    files_17T = [
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_7T_30Hz_100C_1.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_7T_30Hz_100C_2.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_7T_30Hz_100C_3.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_7T_30Hz_100C_4.csv",
        r"C:\Users\User\Desktop\IC\Testes Temperatura\Conjunto 2\100C\Perdas_1_7T_30Hz_100C_5.csv"
    ]

    # --- Execução ---
    analisar_configuracao(files_1T,  "100C - Conjunto 2 - 1,0T - 30Hz", save_dir)
    analisar_configuracao(files_15T, "100C - Conjunto 2 - 1,5T - 30Hz", save_dir)
    analisar_configuracao(files_17T, "100C - Conjunto 2 - 1,7T - 30Hz", save_dir)


if __name__ == "__main__":
    main()
