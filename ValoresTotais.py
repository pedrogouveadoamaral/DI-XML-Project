# Importações

import pandas as pd
from source import ReadXML
from PorAdicao import afrmm_global, getVrSiscomexAdicao, getBcIIAdicao, \
    getVrIIAdicao, getBcPisCofinsAdicao, getVrPisAdicao, getVrCofinsAdicao, \
    getVrIpiAdicao, getVrFreteAdicao, getSeguroAdicao, getVrAcrescimoAdicao, \
    bcicms_global, getVrIcmsAdicao, getVrProdutosXmlAdicao, getVrProdutosNotaAdicao

# Variável com o XML parseado
nfe = ReadXML.nfe

# Dados gerais da nota
def getTotalAdicoes():
    # Função que coleta e retorna o valor total de adições da DI
    get = nfe.getElementsByTagName('totalAdicoes')
    total_adicoes = int(get[0].firstChild.data)
    return total_adicoes

# Valores únicos

def getinformacaoComplementar():
    # Função que coleta e retorna os valores dentro da tag de informações complementares
    get = nfe.getElementsByTagName('informacaoComplementar')
    informacao_complementar = get[0].firstChild.data
    return informacao_complementar

def getValorTotalFrete():
    # Função que coleta e retorna o valor total de frete
    get = nfe.getElementsByTagName('freteTotalReais')
    valor_frete = float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:])
    return valor_frete

def getMoedaNegociadaFrete():
    # Função que coleta e retorna o nome da moeda estrangeira utilizada na negociação do frete - Ex: DOLAR US
    get_moeda_negociada = nfe.getElementsByTagName('freteMoedaNegociadaNome')
    moeda_negociada = get_moeda_negociada[0].firstChild.data
    return moeda_negociada

def getVrFreteMoedan():
    # Função que coleta e retorna o valor total do frete na moeda estrangeira utilizada na negociação do frete
    get = nfe.getElementsByTagName('freteTotalMoeda')
    value = get[0].firstChild.data
    if len(value) == 4:
        valor_frete = float(get[0].firstChild.data[:2] + "." + get[0].firstChild.data[-2:])
    if len(value) == 5:
        valor_frete = float(get[0].firstChild.data[:3] + "." + get[0].firstChild.data[-2:])
    if len(value) == 6:
        valor_frete = float(get[0].firstChild.data[:4] + "." + get[0].firstChild.data[-2:])
    if len(value) == 7:
        valor_frete = float(get[0].firstChild.data[:5] + "." + get[0].firstChild.data[-2:])
    if len(value) == 8:
        valor_frete = float(get[0].firstChild.data[:6] + "." + get[0].firstChild.data[-2:])
    if len(value) == 9:
        valor_frete = float(get[0].firstChild.data[:7] + "." + get[0].firstChild.data[-2:])
    return valor_frete

def getValorCambioMoedaFrete():
    # Função que coleta e retorna o valor de cotação da moeda estrangeira utilizada na negociação do frete
    # Dividindo o valor total do frete em reais pelo valor total do frete na moeda negociada
    vr_frete_moeda = getVrFreteMoedan()
    vr_frete_reais = getValorTotalFrete()
    vr_cambio_frete = round((vr_frete_reais / vr_frete_moeda), 4)
    return vr_cambio_frete

def getMoedaNegociadaProd():
    # Função que coleta e retorna o nome da moeda estrangeira utilizada na negociação dos produtos - Ex: DOLAR US
    get_moeda_negociada = nfe.getElementsByTagName('condicaoVendaMoedaNome')
    moeda_negociada = get_moeda_negociada[0].firstChild.data
    return moeda_negociada

def getCambioMoedaProd():
    # Função que coleta e retorna o valor de cotação da moeda estrangeira utilizada na negociação do frete
    # Dividindo o valor da tag condicaoVendaValorReais pelo da tag condicaoVendaValorMoeda
    get_vr_moeda_negociada = nfe.getElementsByTagName('condicaoVendaValorMoeda')
    vr_moeda_negociada = float(get_vr_moeda_negociada[0].firstChild.data[:13] + "." + get_vr_moeda_negociada[0].firstChild.data[-2:])
    get_vr_reais = nfe.getElementsByTagName('condicaoVendaValorReais')
    vr_reais = float(get_vr_reais[0].firstChild.data[:13] + "." + get_vr_reais[0].firstChild.data[-2:])
    vr_moeda_negociada = round((vr_reais / vr_moeda_negociada), 4)
    return vr_moeda_negociada

def getPesoBrutoTotal():
    # Função que retorna o valor do peso bruto total
    get = nfe.getElementsByTagName('cargaPesoBruto')
    peso_b_total = float(get[0].firstChild.data[:10] + "." + get[0].firstChild.data[-5:])
    return peso_b_total

def getPesoLiquidoTotal():
    # Função que retorna o valor do peso líquido total
    get = nfe.getElementsByTagName('cargaPesoLiquido')
    peso_l_total = float(get[0].firstChild.data[:10] + "." + get[0].firstChild.data[-5:])
    return peso_l_total

def getVMLE():
    # Função que retorna o valor total do VMLE
    get = nfe.getElementsByTagName('localEmbarqueTotalReais')
    valor_vmle = float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:])
    return valor_vmle

def getVMLD():
    # Função que retorna o valor do VMLD
    get = nfe.getElementsByTagName('localDescargaTotalReais')
    valor_vmld = round(float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:]), 2)
    return valor_vmld

def getLocalDesambarque():
    # Função que retorna o local de desembarque da mercadoria no Brasil
    get = nfe.getElementsByTagName('cargaUrfEntradaNome')
    local_desembarque = get[0].firstChild.data
    return local_desembarque

def valoresTotaisToDataFrame():
    # Função para criar os dfs de cada coluna e no final gera o df concatenando todas as colunas
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
