# Importações

import pandas as pd

from PorAdicao import totaisAdicaoToDataFrame
from ValoresTotais import valoresTotaisToDataFrame
from Itens import itensToDataFrame


# Criar um objeto ExcelWriter
with pd.ExcelWriter("DI.xlsx", engine="xlsxwriter") as writer:
    valoresTotaisToDataFrame().to_excel(writer, sheet_name="Totais", index=False)
    totaisAdicaoToDataFrame().to_excel(writer, sheet_name="PorAdição")
    itensToDataFrame().to_excel(writer, sheet_name="Itens")
