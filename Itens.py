# Importações

from source import ReadXML
import pandas as pd
from PorAdicao import getSeguroAdicao, getVrFreteAdicao, afrmm_global, getVrSiscomexAdicao, getVrIIAdicao, \
    getBcIIAdicao, getVrProdutosXmlAdicao, getVrAcrescimoAdicao, aliqicms_global, bcicms_global, getVrIcmsAdicao, \
    getVrIpiAdicao, getVrPisAdicao, getVrCofinsAdicao, getCIFAdicao, getBcPisCofinsAdicao

# Variável com o XML parseado
nfe = ReadXML.nfe

# Era do script ValoresTotais
def getCambioMoedaProd():#Dividindo o valor da tag condicaoVendaValorReais pelo valor da tag condicaoVendaValorMoeda
    getvrmoedanegociada = nfe.getElementsByTagName('condicaoVendaValorMoeda')
    vrmoedanegociada = float(getvrmoedanegociada[0].firstChild.data[:13] + "." + getvrmoedanegociada[0].firstChild.data[-2:])
    getvrreais = nfe.getElementsByTagName('condicaoVendaValorReais')
    vrreais = float(getvrreais[0].firstChild.data[:13] + "." + getvrreais[0].firstChild.data[-2:])
    vrmoedanegociada = round((vrreais / vrmoedanegociada), 4)
    return vrmoedanegociada

def getVMLE():
    get = nfe.getElementsByTagName('localEmbarqueTotalReais')
    vmle = float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:])
    return vmle
# Itens

def getNrAdicaoItens():
    get = nfe.getElementsByTagName("adicao")
    nradicao_dict = dict()
    adicao = 1
    c = 1
    for adicao_tag in get:
        nrseqitem = adicao_tag.getElementsByTagName("mercadoria")
        for itens in nrseqitem:
            nradicao_dict.update({c: adicao})
            c += 1
        adicao += 1
    return nradicao_dict

def getNrSeqItem():
    get = nfe.getElementsByTagName('numeroSequencialItem')
    nritem_dict = dict()
    c = 0
    for i in get:
        item = get[c].firstChild.data
        nritem_dict.update({c + 1: item})
        c += 1
    return nritem_dict

def getItemDescricao():
    get = nfe.getElementsByTagName('descricaoMercadoria')
    c = 0
    descricao_dict = dict()
    for i in get:
        item = get[c].firstChild.data
        descricao_dict.update({c + 1: item})
        c = c + 1
    return descricao_dict

def getUnMedidaProduto():
    get = nfe.getElementsByTagName('unidadeMedida')
    unmedida_dict = dict()
    c = 0
    for i in get:
        unmedida = i.firstChild.data.replace(' ', '')
        if unmedida == 'QUILOGRAMA LIQUIDO':
            unmedida_dict.update({c + 1: 'KG'})
        elif unmedida == 'UNIDADE':
            unmedida_dict.update({c + 1: 'UN'})
        elif unmedida == 'PECA':
            unmedida_dict.update({c + 1: 'PC'})
        else:
            unmedida_dict.update({c + 1: unmedida})
        c += 1
    return unmedida_dict

def getItemValorMoedaOriginal():
    get = nfe.getElementsByTagName('valorUnitario')
    valor_dict = dict()
    c = 0
    for i in get:
        item = float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-7:])
        valor_dict.update({c + 1: item})
        c = c + 1
    return valor_dict

def getItemValorReal():
    get = nfe.getElementsByTagName('valorUnitario')
    valor_dict = dict()
    c = 0
    for i in get:
        item = round(float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-7:])
                     * getCambioMoedaProd(), 6)
        valor_dict.update({c + 1: item})
        c = c + 1
    return valor_dict

def getItemQuantidade():
    get = nfe.getElementsByTagName('quantidade')
    quantidade_dict = dict()
    c = 0
    for i in get:
        item = int(get[c].firstChild.data[:9])
        quantidade_dict.update({c + 1: item})
        c = c + 1
    return quantidade_dict

def calcVrTotalProdutoReal():
    valortotal_dict = dict()
    c = 1
    for i in getItemQuantidade():
        valortotal = round(getItemValorReal().get(c) * getItemQuantidade().get(c), 4)
        valortotal_dict.update({c: valortotal})
        c += 1
    return valortotal_dict
valortotalreal = calcVrTotalProdutoReal()

def calcVrSeguroProduto():
    valorseguro_dict = dict()
    c = 1
    for i in getItemQuantidade():
        valorseguro = round(valortotalreal[c] / getVMLE() * float(sum(getSeguroAdicao().values())), 2)
        valorseguro_dict.update({c: valorseguro})
        c = c + 1
    return valorseguro_dict

def calcVrFreteProduto():
    vrfrete_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vrfreadicao, vmldAdicao in zip(getVrIIAdicao().keys(), getVrFreteAdicao().values(),
                                                   getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / vmldAdicao) * vrfreadicao, 2)
                vrfrete_dict.update({c: valor})
                c += 1
    return vrfrete_dict

def calcVrCIFProduto():
    vrcif_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vrcifadicao, vmldAdicao in zip(getVrIIAdicao().keys(), getCIFAdicao().values(),
                                                   getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / vmldAdicao) * vrcifadicao, 2)
                vrcif_dict.update({c: valor})
                c += 1
    return vrcif_dict

def calcVrAFRMMProduto():
    valorafrmm_dict = dict()
    c = 1
    for i in getItemQuantidade():
        valorafrmm = round(valortotalreal[c] / getVMLE() * float(sum(afrmm_global.values())), 2)
        valorafrmm_dict.update({c: valorafrmm})
        c = c + 1
    return valorafrmm_dict

def calcVrSiscomexProduto():
    valorsiscomex_dict = dict()
    c = 1
    for i in getItemQuantidade():
        valorSiscomex = round(valortotalreal[c] / getVMLE() *
                              float(sum(getVrSiscomexAdicao().values())), 2)
        valorsiscomex_dict.update({c: valorSiscomex})
        c = c + 1
    return valorsiscomex_dict

def calcVrIpiProduto():
    valoripi_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vripiadicao, vmldAdicao in zip(getVrIIAdicao().keys(), getVrIpiAdicao().values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / vmldAdicao) * vripiadicao, 2)
                valoripi_dict.update({c: valor})
                c += 1
    return valoripi_dict

def calcBcIIProduto():
    bcii_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vriiadicao, VmldAdicao in zip(getVrIIAdicao().keys(), getBcIIAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / VmldAdicao) * vriiadicao, 2)
                bcii_dict.update({c: valor})
                c += 1
    return bcii_dict

def calcVrIIProduto():
    valorii_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vriiadicao, VmldAdicao in zip(getVrIIAdicao().keys(), getVrIIAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / VmldAdicao) * vriiadicao, 2)
                valorii_dict.update({c: valor})
                c += 1
    return valorii_dict

def calcBcPisCofinsProduto():
    bcpiscofins_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vriiadicao, VmldAdicao in zip(getVrIIAdicao().keys(), getBcPisCofinsAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / VmldAdicao) * vriiadicao, 2)
                bcpiscofins_dict.update({c: valor})
                c += 1
    return bcpiscofins_dict

def caclVrPisProduto():
    valorpis_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vriiadicao, VmldAdicao in zip(getVrIIAdicao().keys(), getVrPisAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / VmldAdicao) * vriiadicao, 2)
                valorpis_dict.update({c: valor})
                c += 1
    return valorpis_dict

def caclcVrCofinsProduto():
    valorcofins_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vrcofinsadicao, VmldAdicao in zip(getVrIIAdicao().keys(), getVrCofinsAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / VmldAdicao) * vrcofinsadicao, 2)
                valorcofins_dict.update({c: valor})
                c += 1
    return valorcofins_dict

def caclcVrAcrescimoProduto():
    valoracrescimo_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vracrescimoadicao, vmldAdicao in zip(getVrIIAdicao().keys(), getVrAcrescimoAdicao().values(),
                                                         getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / vmldAdicao) * vracrescimoadicao, 2)
                valoracrescimo_dict.update({c: valor})
                c += 1
    return valoracrescimo_dict

def getAliqIcmsProduto():
    aliqicms_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vrbcicmsadicao, vmldAdicao in zip(getVrIIAdicao().keys(), aliqicms_global.values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = vrbcicmsadicao
                aliqicms_dict.update({c: valor})
                c += 1
    return aliqicms_dict

def calcBcIcmsProduto():
    valorbcicms_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vrbcicmsadicao, vmldAdicao in zip(getVrIIAdicao().keys(), bcicms_global.values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / vmldAdicao) * vrbcicmsadicao, 2)
                valorbcicms_dict.update({c: valor})
                c += 1
    return valorbcicms_dict

def calcVrIcmsProduto():
    valoricms_dict = dict()
    c = 1
    for adicaoitem in getNrAdicaoItens().values():
        for adicao, vrbcicmsadicao, vmldAdicao in zip(getVrIIAdicao().keys(), getVrIcmsAdicao().values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicaoitem == adicao:
                valor = round((valortotalreal[c] / vmldAdicao) * vrbcicmsadicao, 2)
                valoricms_dict.update({c: valor})
                c += 1
    return valoricms_dict

def calcVrFinalProdutoNota():
    valorfinal_dict = dict()
    vrseguro = calcVrSeguroProduto().values()
    vrfrete = calcVrFreteProduto().values()
    vracrescimo = caclcVrAcrescimoProduto().values()
    vrii = calcVrIIProduto().values()
    c = 1
    for produto, seguro, frete, acrescimo, ii in zip(valortotalreal.values(), vrseguro, vrfrete, vracrescimo, vrii):
        valorfinal = round(produto + seguro + frete + acrescimo + ii, 4)
        valorfinal_dict.update({c: valorfinal})
        c += 1
    return valorfinal_dict

def itensToDataFrame():
    df0 = pd.DataFrame(getNrAdicaoItens().items()).rename(columns={0: "Item", 1: "Adição"}).set_index('Item')
    df1 = pd.DataFrame(getNrSeqItem().items()).rename(columns={0: "Item", 1: "NrSeqItem"}).set_index('Item')
    df2 = pd.DataFrame(getItemDescricao().items()).rename(columns={0: "Item", 1: "Descricao"}).set_index('Item')
    df3 = pd.DataFrame(getUnMedidaProduto().items()).rename(columns={0: "Item", 1: "UnMedida"}).set_index('Item')
    df5 = pd.DataFrame(getItemValorMoedaOriginal().items()).rename(columns={0: "Item", 1: "Vr un Moeda Original"})\
        .set_index('Item')
    df6 = pd.DataFrame(getItemValorReal().items()).rename(columns={0: "Item", 1: "Vr un R$ - XML"})\
        .set_index('Item')
    df7 = pd.DataFrame(getItemQuantidade().items()).rename(columns={0: "Item", 1: "Quantidade"}).set_index('Item')
    df8 = pd.DataFrame(valortotalreal.items()).rename(columns={0: "Item", 1: "VrProd R$ XML"}).set_index('Item')
    df9 = pd.DataFrame(calcVrFinalProdutoNota().items()).rename(columns={0: "Item", 1: "VrProd R$ Nota"}).set_index('Item')
    df10 = pd.DataFrame(calcVrSeguroProduto().items()).rename(columns={0: "Item", 1: "VrSeguro"}).set_index('Item')
    df11 = pd.DataFrame(calcVrFreteProduto().items()).rename(columns={0: "Item", 1: "VrFrete"}).set_index('Item')
    df12 = pd.DataFrame(calcVrCIFProduto().items()).rename(columns={0: "Item", 1: "VrCIF"}).set_index('Item')
    df13 = pd.DataFrame(calcVrAFRMMProduto().items()).rename(columns={0: "Item", 1: "VrAFRMM"}).set_index('Item')
    df14 = pd.DataFrame(calcVrSiscomexProduto().items()).rename(columns={0: "Item", 1: "VrSiscomex"}).set_index('Item')
    df15 = pd.DataFrame(calcBcIIProduto().items()).rename(columns={0: "Item", 1: "BcII"}).set_index('Item')
    df16 = pd.DataFrame(calcVrIIProduto().items()).rename(columns={0: "Item", 1: "VrII"}).set_index('Item')
    df17 = pd.DataFrame(calcBcPisCofinsProduto().items()).rename(columns={0: "Item", 1: "BcPisCofins"}).set_index('Item')
    df18 = pd.DataFrame(caclVrPisProduto().items()).rename(columns={0: "Item", 1: "VrPis"}).set_index('Item')
    df19 = pd.DataFrame(caclcVrCofinsProduto().items()).rename(columns={0: "Item", 1: "VrCofins"}).set_index('Item')
    df20 = pd.DataFrame(calcVrIpiProduto().items()).rename(columns={0: "Item", 1: "VrIpi"}).set_index('Item')
    df21 = pd.DataFrame(caclcVrAcrescimoProduto().items()).rename(columns={0: "Item", 1: "VrAcrescimo"}).set_index('Item')
    df22 = pd.DataFrame(getAliqIcmsProduto().items()).rename(columns={0: "Item", 1: "AliqIcms"}).set_index('Item')
    df23 = pd.DataFrame(calcBcIcmsProduto().items()).rename(columns={0: "Item", 1: "BcICMS"}).set_index('Item')
    df24 = pd.DataFrame(calcVrIcmsProduto().items()).rename(columns={0: "Item", 1: "VrICMS"}).set_index('Item')
    df = pd.concat([df0, df1, df2, df3, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17,
                    df18, df19, df20, df21, df22, df23, df24],
                   axis=1, sort=True)
    return df


# itensToDataFrame().to_excel("Itens2.xlsx", sheet_name='Itens')

