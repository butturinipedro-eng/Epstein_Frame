import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import CheckButtons
import numpy as np

# ==============================
# CONFIGURAÇÃO GLOBAL DO ESTILO
# ==============================
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 14
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['legend.fontsize'] = 12
mpl.rcParams['figure.titlesize'] = 18


# =============================================================
# FUNÇÃO 1: PLOTAR BH INDIVIDUAL (B(t), H(t) e laço de histerese)
# =============================================================
def plotar_BH(arquivo, coluna_B="Sum14", coluna_H="Gain4"):
    try:
        df = pd.read_csv(arquivo)
        df[coluna_B] = df[coluna_B].astype(str).str.replace(",", ".").astype(float)
        df[coluna_H] = df[coluna_H].astype(str).str.replace(",", ".").astype(float)
        B = df[coluna_B].values
        H = df[coluna_H].values
        t = range(len(B))

        base = os.path.basename(arquivo)

        # --- B(t)
        """plt.figure(figsize=(7,4))
        plt.plot(t, B, color='darkred', lw=1.5)
        plt.title(f"B(t) — {base}")
        plt.xlabel("Amostras")
        plt.ylabel("B [T]")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()"""

        # --- H(t)
        """plt.figure(figsize=(7,4))
        plt.plot(t, H, color='navy', lw=1.5)
        plt.title(f"H(t) — {base}")
        plt.xlabel("Amostras")
        plt.ylabel("H [A/m]")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()"""

        # --- Curva BH
        plt.figure(figsize=(6,6))
        plt.plot(H, B, '-', color='black', lw=1.5)
        plt.title(f"Laço de Histerese — {base}")
        plt.xlabel("H [A/m]")
        plt.ylabel("B [T]")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao processar '{arquivo}': {e}")

def comparar_bh_publicacao(pasta, coluna_B="Sum14", coluna_H="Gain4", salvar=False):
    """
    Lê todos os arquivos bh_*.csv de uma pasta e plota as curvas B×H
    com formatação padronizada para artigo científico:
    - Legenda: "B = X T | Hdc = Y A/m"
    - Ordem crescente de Hdc
    - Sem checkboxes interativos
    - Fonte Times New Roman (já configurada globalmente)
    
    Parâmetros:
      pasta (str): diretório onde estão os arquivos bh_*.csv
      coluna_B, coluna_H (str): nomes das colunas no CSV
      salvar (bool): se True, salva a figura como PNG na pasta
    """
    arquivos = [f for f in os.listdir(pasta) if f.lower().startswith("bh_") and f.lower().endswith(".csv")]
    if not arquivos:
        print(f"⚠️ Nenhum arquivo 'bh_*.csv' encontrado em: {pasta}")
        return

    # --- Define densidade de fluxo base como 0,7 T ---
    densidade_base = "0,7"

    # --- Função auxiliar para extrair Hdc numérico ---
    def extrair_hdc(nome):
        nome = nome.lower()
        match = re.search(r"(\d+)(?=_?a?_?m?)", nome)
        return int(match.group(1)) if match else 0

    # Ordena os arquivos pelo valor de Hdc crescente
    arquivos.sort(key=extrair_hdc)

    # --- Figura e eixos ---
    fig, ax = plt.subplots(figsize=(7.5, 6))

    # --- Loop pelos arquivos ---
    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        try:
            df = pd.read_csv(caminho)
            df[coluna_B] = df[coluna_B].astype(str).str.replace(",", ".").astype(float)
            df[coluna_H] = df[coluna_H].astype(str).str.replace(",", ".").astype(float)
            B = df[coluna_B].values
            H = df[coluna_H].values

            hdc = extrair_hdc(arquivo)
            legenda = f"B = {densidade_base} T | Hdc = {hdc} A/m"
            ax.plot(H, B, lw=1.6, label=legenda)
        except Exception as e:
            print(f"❌ Erro ao ler '{arquivo}': {e}")

    # --- Configuração visual ---
    ax.set_title(f"Comparação de Laços B×H para {densidade_base} T e diferentes Hdc")
    ax.set_xlabel("H [A/m]")
    ax.set_ylabel("B [T]")
    ax.legend(loc="best", frameon=False)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_yticks([i * 0.1 for i in range(-7, 8)])  # Define passos de 0.1 no eixo Y
    ax.set_ylim(-0.75, 0.75)  # Limita o eixo Y de -0.75 a 0.75
    plt.tight_layout()

    # --- Salvar opcionalmente ---
    if salvar:
        nome_figura = os.path.join(pasta, f"Comparacao_BH_{os.path.basename(pasta)}.png")
        plt.savefig(nome_figura, dpi=600, bbox_inches="tight")
        print(f"✅ Figura salva em: {nome_figura}")

    plt.show()


# =============================================================
# FUNÇÃO 2: PLOTAR TENSÃO E CORRENTE
# =============================================================
def plotar_VI(arquivo_tensao, arquivo_corrente):
    try:
        df_v = pd.read_csv(arquivo_tensao)
        df_i = pd.read_csv(arquivo_corrente)

        col_v = df_v.columns[-1]
        col_i = df_i.columns[-1]

        v = df_v[col_v].astype(str).str.replace(",", ".").astype(float).values
        i = df_i[col_i].astype(str).str.replace(",", ".").astype(float).values

        n = min(len(v), len(i))
        v = v[:n]; i = i[:n]
        t = range(n)

        nome_v = os.path.basename(arquivo_tensao)
        nome_i = os.path.basename(arquivo_corrente)

        plt.figure(figsize=(7,4))
        plt.plot(t, v, color="purple", lw=1.5)
        plt.title(f"Tensão — {nome_v}")
        plt.xlabel("Amostras")
        plt.ylabel("Tensão [V]")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(7,4))
        plt.plot(t, i, color="brown", lw=1.5)
        plt.title(f"Corrente — {nome_i}")
        plt.xlabel("Amostras")
        plt.ylabel("Corrente [A]")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao processar '{arquivo_tensao}' ou '{arquivo_corrente}': {e}")


# =============================================================
# FUNÇÃO 3: PLOTAR PERDAS E CALCULAR MÉDIA
# =============================================================
def plotar_perdas(arquivo_perdas):
    try:
        df = pd.read_csv(arquivo_perdas)
        col = df.columns[-1]
        perdas = df[col].astype(str).str.replace(",", ".").astype(float).values
        media = perdas.mean()
        x = range(len(perdas))

        plt.figure(figsize=(7,4))
        plt.plot(x, perdas, color='darkgreen', lw=1.3, label='Perdas medidas')
        plt.axhline(media, color='red', linestyle='--', label=f"Média = {media:.6f} W/kg")
        plt.title(f"Perdas — {os.path.basename(arquivo_perdas)}")
        plt.xlabel("Amostras")
        plt.ylabel("Perdas [W/kg]")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

        print(f"✅ Média das perdas: {media:.6f} W/kg")

    except Exception as e:
        print(f"❌ Erro ao processar '{arquivo_perdas}': {e}")


# =============================================================
# FUNÇÃO 4: COMPARAR MÚLTIPLOS BH COM CHECKBOX
# =============================================================
def comparar_bh_em_diretorio(pasta, coluna_B="Sum14", coluna_H="Gain4"):
    arquivos = [f for f in os.listdir(pasta) if f.lower().startswith("bh_") and f.lower().endswith(".csv")]
    if not arquivos:
        print(f"⚠️ Nenhum arquivo 'bh_*.csv' encontrado em: {pasta}")
        return

    # Detecta densidade base
    match = re.search(r"(\d+[_.,]?\d*)t", pasta.lower())
    densidade_base = match.group(1).replace("_", ".") if match else "?"

    # Ordena por valor de Hdc
    def extrair_hdc(nome):
        nome = nome.lower()
        match = re.search(r"(\d+)(?=_?a?_?m?)", nome)
        return int(match.group(1)) if match else 0

    arquivos.sort(key=extrair_hdc)

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(left=0.3)
    linhas, labels = [], []

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        try:
            df = pd.read_csv(caminho)
            df[coluna_B] = df[coluna_B].astype(str).str.replace(",", ".").astype(float)
            df[coluna_H] = df[coluna_H].astype(str).str.replace(",", ".").astype(float)
            B, H = df[coluna_B].values, df[coluna_H].values
            hdc = extrair_hdc(arquivo)
            label = f"B = {densidade_base} T | Hdc = {hdc} A/m"
            linha, = ax.plot(H, B, lw=1.4, label=label)
            linhas.append(linha)
            labels.append(label)
        except Exception as e:
            print(f"❌ Erro ao ler '{arquivo}': {e}")

    ax.set_title(f"Comparação de Laços B×H — {os.path.basename(pasta)}")
    ax.set_xlabel("H [A/m]")
    ax.set_ylabel("B [T]")
    ax.grid(True, linestyle="--", alpha=0.7)

    rax = plt.axes([0.02, 0.25, 0.25, 0.5])
    visibility = [True] * len(linhas)
    check = CheckButtons(rax, labels, visibility)

    def toggle(label):
        idx = labels.index(label)
        linhas[idx].set_visible(not linhas[idx].get_visible())
        plt.draw()

    check.on_clicked(toggle)
    plt.show()


# =============================================================
# FUNÇÃO 5: CURVA BH DO MATERIAL (Bmax × Hmax)
# =============================================================
def curva_BH_material(*arquivos, coluna_B="Sum14", coluna_H="Gain4", salvar_csv=True):
    """
    Recebe múltiplos arquivos bh_*.csv, extrai Bmax e Hmax de cada um
    e plota a curva Bmax × Hmax do material.
    """
    dados = []

    for arquivo in arquivos:
        try:
            df = pd.read_csv(arquivo)
            df[coluna_B] = df[coluna_B].astype(str).str.replace(",", ".").astype(float)
            df[coluna_H] = df[coluna_H].astype(str).str.replace(",", ".").astype(float)
            Bmax = df[coluna_B].abs().max()
            Hmax = df[coluna_H].abs().max()
            nome = os.path.basename(arquivo)
            dados.append((nome, Hmax, Bmax))
        except Exception as e:
            print(f"❌ Erro ao ler '{arquivo}': {e}")

    if not dados:
        print("⚠️ Nenhum dado válido encontrado.")
        return

    df_out = pd.DataFrame(dados, columns=["Arquivo", "Hmax [A/m]", "Bmax [T]"])
    df_out.sort_values("Hmax [A/m]", inplace=True)

    plt.figure(figsize=(7,5))
    plt.plot(df_out["Hmax [A/m]"], df_out["Bmax [T]"], 'o-', color='black', lw=1.5)
    #plt.title("Curva BH do Material (Bmax × Hmax)")
    plt.xlabel("H")
    plt.ylabel("B")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    if salvar_csv:
        df_out.to_csv("curva_BH_material.csv", index=False)
        print("✅ Dados salvos em 'curva_BH_material.csv'")


#FUNÇÃO PLOTAR PERDAS PARA DIFERENTES B
def _ler_media_perdas(arquivo):
    """Lê o último arquivo CSV e retorna a média das perdas (float)."""
    try:
        df = pd.read_csv(arquivo)
        col_p = df.columns[-1]
        perdas = df[col_p].astype(str).str.replace(",", ".").astype(float)
        return perdas.mean()
    except Exception as e:
        print(f"⚠️ Erro ao ler '{arquivo}': {e}")
        return np.nan
    
def plotar_perdas_vs_B(pasta_base):
    """
    Lê arquivos 'perdas_*.csv' de subpastas como:
      0_3T, 0_4T, 0_5T, ..., 1_0T
    e plota o gráfico de Perdas Médias x Densidade de Fluxo (B).

    Parâmetro:
      pasta_base (str): diretório contendo as pastas 0_3T, 0_4T, etc.
    """
    dados = []

    # procura subpastas do tipo *_T
    for pasta in sorted(os.listdir(pasta_base)):
        if re.match(r"^\d+[_.,]?\d*t$", pasta.lower()):
            caminho_pasta = os.path.join(pasta_base, pasta)
            arquivo_perdas = os.path.join(caminho_pasta, f"perdas_{pasta}.csv")

            if os.path.exists(arquivo_perdas):
                media = _ler_media_perdas(arquivo_perdas)
                B = float(pasta.lower().replace("_", ".").replace("t", ""))
                dados.append((B, media))

    if not dados:
        print(f"⚠️ Nenhum arquivo de perdas encontrado em {pasta_base}")
        return

    dados = sorted(dados, key=lambda x: x[0])
    B_vals, perdas_vals = zip(*dados)

    plt.figure(figsize=(7, 5))
    plt.plot(B_vals, perdas_vals, "o-", lw=1.8, color="navy")
    #plt.title("Perdas Magnéticas em Função da Densidade de Fluxo (sem Hdc)")
    plt.xlabel("B [T]")
    plt.ylabel("Average magnetic losses [W/kg]")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


#PERDAS COM HDC

def plotar_perdas_vs_Hdc(*arquivos, coluna_perdas="Peak Detector17:4", salvar_csv=True):
    """
    Recebe múltiplos arquivos de perdas, calcula a média de cada um
    e plota a curva de perdas médias × Hdc.
    """
    dados = []

    for i, arquivo in enumerate(arquivos):
        try:
            df = pd.read_csv(arquivo)
            df[coluna_perdas] = df[coluna_perdas].astype(str).str.replace(",", ".").astype(float)
            media_perdas = df[coluna_perdas].mean()

            # Assign Hdc values manually based on the order of files
            hdc = i * 5  # 0 A/m, 5 A/m, 10 A/m, etc.

            nome = os.path.basename(arquivo)
            dados.append((nome, hdc, media_perdas))
        except Exception as e:
            print(f"❌ Erro ao ler '{arquivo}': {e}")

    if not dados:
        print("⚠️ Nenhum dado válido encontrado.")
        return

    df_out = pd.DataFrame(dados, columns=["Arquivo", "Hdc [A/m]", "Perdas Médias [W/kg]"])
    df_out.sort_values("Hdc [A/m]", inplace=True)

    plt.figure(figsize=(7,5))
    plt.plot(df_out["Hdc [A/m]"], df_out["Perdas Médias [W/kg]"], 'o-', color='blue')
    plt.title("Perdas Médias × Hdc para 0,7T")
    plt.xlabel("Hdc [A/m]")
    plt.ylabel("Perdas Médias [W/kg]")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def plotar_boxplot_perdas_vs_Hdc(*arquivos, coluna_perdas="Peak Detector17:4", salvar_csv=True):
    """
    Similar to plotar_perdas_vs_Hdc but creates a boxplot for each Hdc value.
    """
    dados = []

    for i, arquivo in enumerate(arquivos):
        try:
            df = pd.read_csv(arquivo)
            df[coluna_perdas] = df[coluna_perdas].astype(str).str.replace(",", ".").astype(float)

            # Assign Hdc values manually based on the order of files
            hdc = i * 5  # 0 A/m, 5 A/m, 10 A/m, etc.

            for perda in df[coluna_perdas]:
                dados.append((hdc, perda))
        except Exception as e:
            print(f"❌ Erro ao ler '{arquivo}': {e}")

    if not dados:
        print("⚠️ Nenhum dado válido encontrado.")
        return

    df_out = pd.DataFrame(dados, columns=["Hdc [A/m]", "Perdas [W/kg]"])

    plt.figure(figsize=(7,5))
    df_out.boxplot(column="Perdas [W/kg]", by="Hdc [A/m]", grid=False, showmeans=True)
    plt.title("Boxplot de Perdas × Hdc para 0,7T")
    plt.suptitle("")  # Remove the automatic title
    plt.xlabel("Hdc [A/m]")
    plt.ylabel("Perdas [W/kg]")
    plt.tight_layout()
    plt.show()

    if salvar_csv:
        df_out.to_csv("boxplot_perdas_vs_Hdc.csv", index=False)
        print("✅ Dados salvos em 'boxplot_perdas_vs_Hdc.csv'")


def plotar_BH_artigo(arquivos, colunas_B_H=("Sum14", "Gain4")):
    """
    Plota os laços de histerese para três arquivos em uma única figura com três subplots.

    Parâmetros:
        arquivos (list): Lista com três caminhos de arquivos CSV (0.3T, 0.6T, 1T).
        colunas_B_H (tuple): Tupla com os nomes das colunas para B e H, respectivamente.
    """
    if len(arquivos) != 3:
        print("❌ É necessário fornecer exatamente três arquivos (0.3T, 0.6T, 1T).")
        return

    coluna_B, coluna_H = colunas_B_H
    titulos = ["0.3 T 60 Hz", "0.6 T 60 Hz", "1.0 T 60 Hz"]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

    for i, arquivo in enumerate(arquivos):
        try:
            df = pd.read_csv(arquivo)
            df[coluna_B] = df[coluna_B].astype(str).str.replace(",", ".").astype(float)
            df[coluna_H] = df[coluna_H].astype(str).str.replace(",", ".").astype(float)
            B = df[coluna_B].values
            H = df[coluna_H].values

            axes[i].plot(H, B, '-', color='black', lw=1.5)
            axes[i].set_title(titulos[i])
            axes[i].set_xlabel("H [A/m]")
            if i == 0:
                axes[i].set_ylabel("B [T]")
            axes[i].grid(True, linestyle='--', alpha=0.6)

        except Exception as e:
            print(f"❌ Erro ao processar '{arquivo}': {e}")

    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()


def combinar_imagens_artigo(arquivos, titulos):
    """
    Combina três imagens lado a lado em uma única figura.

    Parâmetros:
        arquivos (list): Lista com três caminhos de arquivos PNG.
        titulos (list): Lista com os títulos das imagens na ordem dos arquivos.
    """
    if len(arquivos) != 3 or len(titulos) != 3:
        print("❌ É necessário fornecer exatamente três arquivos e três títulos.")
        return

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, (arquivo, titulo) in enumerate(zip(arquivos, titulos)):
        try:
            img = plt.imread(arquivo)
            axes[i].imshow(img)
            axes[i].set_title(titulo)
            axes[i].axis('off')  # Remove os eixos
        except Exception as e:
            print(f"❌ Erro ao carregar '{arquivo}': {e}")

    plt.tight_layout()
    plt.show()
