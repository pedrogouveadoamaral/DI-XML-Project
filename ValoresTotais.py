# Importações

import pandas as pd
from source import ReadXML
from PorAdicao import getBcPisCofinsTotal, getNrAdicao, afrmm_global, getVrSiscomexAdicao, getBcIIAdicao, \
    getVrIIAdicao, getBcPisCofinsAdicao, getVrPisAdicao, getVrCofinsAdicao, getVrIpiAdicao, getVrFreteAdicao, \
    getSeguroAdicao, getVrAcrescimoAdicao, bcicms_global, getVrIcmsAdicao, getVrProdutosXmlAdicao, getVrProdutosNotaAdicao

# Variável com o XML parseado
nfe = ReadXML.nfe

# Dados gerais da nota
def getTotalAdicoes():
    get = nfe.getElementsByTagName('totalAdicoes')
    totalAdicoes = int(get[0].firstChild.data)
    return totalAdicoes

# Valores únicos

def getinformacaoComplementar():
    get = nfe.getElementsByTagName('informacaoComplementar')
    informacaoComplementar = get[0].firstChild.data
    return informacaoComplementar

def getValorTotalFrete():
    get = nfe.getElementsByTagName('freteTotalReais')
    valorFrete = float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:])
    return valorFrete

def getMoedaNegociadaFrete():
    getMoedaNegociada = nfe.getElementsByTagName('freteMoedaNegociadaNome')
    moedaNegociada = getMoedaNegociada[0].firstChild.data
    return moedaNegociada

def getVrFreteMoedan():
    get = nfe.getElementsByTagName('freteTotalMoeda')
    value = get[0].firstChild.data
    if len(value) == 4:
        valorFrete = float(get[0].firstChild.data[:2] + "." + get[0].firstChild.data[-2:])
    if len(value) == 5:
        valorFrete = float(get[0].firstChild.data[:3] + "." + get[0].firstChild.data[-2:])
    if len(value) == 6:
        valorFrete = float(get[0].firstChild.data[:4] + "." + get[0].firstChild.data[-2:])
    if len(value) == 7:
        valorFrete = float(get[0].firstChild.data[:5] + "." + get[0].firstChild.data[-2:])
    if len(value) == 8:
        valorFrete = float(get[0].firstChild.data[:6] + "." + get[0].firstChild.data[-2:])
    if len(value) == 9:
        valorFrete = float(get[0].firstChild.data[:7] + "." + get[0].firstChild.data[-2:])
    return valorFrete

def getValorCambioMoedaFrete():
    vrfretemoeda = getVrFreteMoedan()
    vrfretereais = getValorTotalFrete()
    vrcambiofrete = round((vrfretereais / vrfretemoeda), 4)
    return vrcambiofrete

def getMoedaNegociadaProd():
    getMoedaNegociada = nfe.getElementsByTagName('condicaoVendaMoedaNome')
    moedaNegociada = getMoedaNegociada[0].firstChild.data
    return moedaNegociada

def getCambioMoedaProd():#Dividindo o valor da tag condicaoVendaValorReais pelo da tag condicaoVendaValorMoeda
    getVrMoedaNegociada = nfe.getElementsByTagName('condicaoVendaValorMoeda')
    vrMoedaNegociada = float(getVrMoedaNegociada[0].firstChild.data[:13] + "." + getVrMoedaNegociada[0].firstChild.data[-2:])
    getVrReais = nfe.getElementsByTagName('condicaoVendaValorReais')
    vrReais = float(getVrReais[0].firstChild.data[:13] + "." + getVrReais[0].firstChild.data[-2:])
    vrMoedaNegociada = round((vrReais / vrMoedaNegociada), 4)
    return vrMoedaNegociada

def getPesoBrutoTotal():
    get = nfe.getElementsByTagName('cargaPesoBruto')
    pesoBTotal = float(get[0].firstChild.data[:10] + "." + get[0].firstChild.data[-5:])
    return pesoBTotal

def getPesoLiquidoTotal():
    get = nfe.getElementsByTagName('cargaPesoLiquido')
    pesoLTotal = float(get[0].firstChild.data[:10] + "." + get[0].firstChild.data[-5:])
    return pesoLTotal

def getVMLE():
    get = nfe.getElementsByTagName('localEmbarqueTotalReais')
    valorVMLE = float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:])
    return valorVMLE

def getVMLD():
    get = nfe.getElementsByTagName('localDescargaTotalReais')
    valorVMLD = round(float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:]), 2)
    return valorVMLD

def getLocalDesambarque():
    get = nfe.getElementsByTagName('cargaUrfEntradaNome')
    localdesembarque = get[0].firstChild.data
    return localdesembarque

def valoresTotaisToDataFrame():
    df0 = pd.DataFrame({"Adições": [getTotalAdicoes()]})
    df1 = pd.DataFrame({"Moeda - Produtos": [getMoedaNegociadaProd()]})
    df2 = pd.DataFrame({"Cotação R$ - Produtos": [getCambioMoedaProd()]})
    df3 = pd.DataFrame({"Moeda - Frete": [getMoedaNegociadaFrete()]})
    df4 = pd.DataFrame({"Cotação R$ - Frete": [getValorCambioMoedaFrete()]})
    df5 = pd.DataFrame({"VMLE": [getVMLE()]})
    df6 = pd.DataFrame({"VMLD": [getVMLD()]})
    df7 = pd.DataFrame({"Frete R$": [round(float(sum(getVrFreteAdicao().values())), 2)]})
    df8 = pd.DataFrame({"Seguro R$": [round(float(sum(getSeguroAdicao().values())), 2)]})
    df9 = pd.DataFrame({"ProdutosXML": [round(float(sum(getVrProdutosXmlAdicao().values())), 2)]})
    df10 = pd.DataFrame({"ProdutosNota": [round(float(sum(getVrProdutosNotaAdicao().values())), 2)]})
    df11 = pd.DataFrame({"BcII": [round(float(sum(getBcIIAdicao().values())), 2)]})
    df12 = pd.DataFrame({"VrII": [round(float(sum(getVrIIAdicao().values())), 2)]})
    df13 = pd.DataFrame({"BcPisCofins": [round(float(sum(getBcPisCofinsAdicao().values())), 2)]})
    df14 = pd.DataFrame({"VrPIS": [round(float(sum(getVrPisAdicao().values())), 2)]})
    df15 = pd.DataFrame({"VrCofins": [round(float(sum(getVrCofinsAdicao().values())), 2)]})
    df16 = pd.DataFrame({"VrIpi": [round(float(sum(getVrIpiAdicao().values())), 2)]})
    df17 = pd.DataFrame({"Siscomex": [round(float(sum(getVrSiscomexAdicao().values())), 2)]})
    df18 = pd.DataFrame({"AFRMM": [round(float(sum(afrmm_global.values())), 2)]})
    df19 = pd.DataFrame({"Acréscimo": [round(float(sum(getVrAcrescimoAdicao().values())), 2)]})
    df20 = pd.DataFrame({"BcICMS": [round(float(sum(bcicms_global.values())), 2)]})
    df21 = pd.DataFrame({"VrICMS": [round(float(sum(getVrIcmsAdicao().values())), 2)]})
    df = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17,
                    df18, df19, df20, df21],
                   axis=1, sort=True).set_index('Adições')
    return df

def valoresTotaisToDataFrame2():
    data = {
        "Adições": [getTotalAdicoes()],
        "Moeda - Produtos": [getMoedaNegociadaProd()],
        "Cotação R$ - Produtos": [getCambioMoedaProd()],
        "Moeda - Frete": [getMoedaNegociadaFrete()],
        "Cotação R$ - Frete": [getValorCambioMoedaFrete()],
        "VMLE": [getVMLE()],
        "VMLD": [getVMLD()],
        "Frete R$": [round(float(sum(getVrFreteAdicao().values())), 2)],
        "Seguro R$": [round(float(sum(getSeguroAdicao().values())), 2)],
        "ProdutosXML": [round(float(sum(getVrProdutosXmlAdicao().values())), 2)],
        "ProdutosNota": [round(float(sum(getVrProdutosNotaAdicao().values())), 2)],
        "BcII": [round(float(sum(getBcIIAdicao().values())), 2)],
        "VrII": [round(float(sum(getVrIIAdicao().values())), 2)],
        "BcPisCofins": [round(float(sum(getBcPisCofinsAdicao().values())), 2)],
        "VrPIS": [round(float(sum(getVrPisAdicao().values())), 2)],
        "VrCofins": [round(float(sum(getVrCofinsAdicao().values())), 2)],
        "VrIpi": [round(float(sum(getVrIpiAdicao().values())), 2)],
        "Siscomex": [round(float(sum(getVrSiscomexAdicao().values())), 2)],
        "AFRMM": [round(float(sum(afrmm_global.values())), 2)],
        "Acréscimo": [round(float(sum(getVrAcrescimoAdicao().values())), 2)],
        "BcICMS": [round(float(sum(bcicms_global.values())), 2)],
        "VrICMS": [round(float(sum(getVrIcms().values())), 2)]
    }

    df = pd.DataFrame(data).set_index('Adições')
    return df

# valoresTotaisToDataFrame2().to_excel("ValoresTotais.xlsx", sheet_name='Totais')


# valoresTotaisToDataFrame().to_excel("ValoresTotais.xlsx", sheet_name='Totais')
# 