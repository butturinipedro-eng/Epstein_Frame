import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import funcoes_histerese as fh



#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_3T/bh_0_3T.csv")
#plotar_VI(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_3T/tensao_0_3T.csv", r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_3T/corrente_0_3T.csv")
#plotar_perdas(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_3T/perdas_0_3T.csv")
#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_4T/bh_0_4T.csv")
#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_5T/bh_0_5T.csv")
#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_6T/bh_0_6T.csv")
#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_8T/bh_0_8T.csv")
#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/0_9T/bh_0_9T.csv")
#plotar_BH(r"C:/Users/User/Desktop/IC/Resultados Giovanni/1_0T/bh_1_0T.csv")

#fh.comparar_bh_em_diretorio(r"C:\Users\User\Desktop\IC\0_7 HDC")
#fh.comparar_bh_publicacao(r"C:\Users\User\Desktop\IC\0_7 HDC")
#fh.curva_BH_material(r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_3T\bh_0_3T.csv",r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_4T\bh_0_4T.csv", r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_5T\bh_0_5T.csv", r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_6T\bh_0_6T.csv",r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_7T\bh_0_7T.csv",r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_8T\bh_0_8T.csv", r"C:\Users\User\Desktop\IC\Resultados Giovanni\0_9T\bh_0_9T.csv", r"C:\Users\User\Desktop\IC\Resultados Giovanni\1_0T\bh_1_0T.csv")
#fh.plotar_perdas_vs_B(r"C:\Users\User\Desktop\IC\Resultados Giovanni")
#fh.plotar_perdas_vs_Hdc(r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_0_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_5_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_10_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_15_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_20_Hdc.csv")
#fh.plotar_boxplot_perdas_vs_Hdc(r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_0_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_5_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_10_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_15_Hdc.csv",r"C:\Users\User\Desktop\IC\0_7 HDC\perdas_0_7T_20_Hdc.csv")
#fh.plotar_BH(r"C:\Users\User\Desktop\IC\Resultados Giovanni\1_0T\bh_1_0T.csv")
fh.plotar_BH_artigo([
    r"C:\Users\User\Desktop\IC\0_3T\bh_0_3T.csv",
    r"C:\Users\User\Desktop\IC\0_6T\bh_0_6T.csv",
    r"C:\Users\User\Desktop\IC\1_0T\bh_1_0T.csv"
])
fh.combinar_imagens_artigo([r"C:\Users\User\Desktop\IC\0_3T\0_3T0.png",r"C:\Users\User\Desktop\IC\0_6T\0_6T0.png",r"C:\Users\User\Desktop\IC\1_0T\1_0T0.png"], ["0.3 T 60 Hz", "0.6 T 60 Hz", "1.0 T 60 Hz"])