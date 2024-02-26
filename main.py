# Importações

import pandas as pd

from PorAdicao import totaisAdicaoToDataFrame
from ValoresTotais import valoresTotaisToDataFrame
from Itens import itensToDataFrame


def toExcel():
    # Criar um objeto ExcelWriter
    with pd.ExcelWriter("ValoresDi.xlsx", engine="xlsxwriter") as writer:
        # Escrever o DataFrame em uma planilha chamada "ValoresDi"
        valoresTotaisToDataFrame().to_excel(writer, sheet_name="Totais", index=False)
        totaisAdicaoToDataFrame().to_excel(writer, sheet_name="PorAdição")
        itensToDataFrame().to_excel(writer, sheet_name="Itens")
try:
    toExcel()
    print('Arquivo criado com sucesso!')
except:
    print('Não foi possível criar o arquivo, verifique!')
