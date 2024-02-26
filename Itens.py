# Importações

from source import ReadXML
import pandas as pd
from PorAdicao import getSeguroAdicao, getVrFreteAdicao, afrmm_global, getVrSiscomexAdicao, getVrIIAdicao, \
    getBcIIAdicao, getVrProdutosXmlAdicao, getVrAcrescimoAdicao, aliqicms_global, bcicms_global, getVrIcmsAdicao, \
    getVrIpiAdicao, getVrPisAdicao, getVrCofinsAdicao, getCIFAdicao, getBcPisCofinsAdicao

# Variável com o XML parseado
nfe = ReadXML.nfe

# Moedas negociadas
def getCambioMoedaProd():
    # Função que retorna o valor de câmbio de produtos usando a fórmula: Dividindo o valor da tag
    # condicaoVendaValorReais pelo da tag condicaoVendaValorMoeda
    get_vr_moeda_negociada = nfe.getElementsByTagName('condicaoVendaValorMoeda')
    vr_moeda_negociada = float(get_vr_moeda_negociada[0].firstChild.data[:13] + "."
                               + get_vr_moeda_negociada[0].firstChild.data[-2:])
    get_vr_reais = nfe.getElementsByTagName('condicaoVendaValorReais')
    vr_reais = float(get_vr_reais[0].firstChild.data[:13] + "." + get_vr_reais[0].firstChild.data[-2:])
    vr_moeda_negociada = round((vr_reais / vr_moeda_negociada), 4)
    return vr_moeda_negociada

def getVMLE():
    # Função que retorna o valor de VMLE
    get = nfe.getElementsByTagName('localEmbarqueTotalReais')
    vr_vmle = float(get[0].firstChild.data[:13] + "." + get[0].firstChild.data[-2:])
    return vr_vmle
# Itens

def getNrAdicaoItens():
    # Função que retorna o número da adição a qual o item pertence
    get = nfe.getElementsByTagName("adicao")
    nr_adicao_dict = dict()
    adicao = 1
    c = 1
    for adicao_tag in get:
        nr_seq_item = adicao_tag.getElementsByTagName("mercadoria")
        for i in nr_seq_item:
            nr_adicao_dict.update({c: adicao})
            c += 1
        adicao += 1
    return nr_adicao_dict

def getNrSeqItem():
    # Função que retorna o número sequencial do item de acordo com sua adição
    get = nfe.getElementsByTagName('numeroSequencialItem')
    nr_item_dict = dict()
    c = 0
    for i in get:
        item = get[c].firstChild.data
        nr_item_dict.update({c + 1: item})
        c += 1
    return nr_item_dict

def getItemDescricao():
    # Função que retorna as descrições dos itens
    get = nfe.getElementsByTagName('descricaoMercadoria')
    c = 0
    descricao_dict = dict()
    for i in get:
        item = get[c].firstChild.data
        descricao_dict.update({c + 1: item})
        c = c + 1
    return descricao_dict

def getUnMedidaProduto():
    # Função que retorna as unidades de medidas estatística dos itens
    get = nfe.getElementsByTagName('unidadeMedida')
    un_medida_dict = dict()
    c = 0
    for i in get:
        unmedida = i.firstChild.data.replace(' ', '')
        if unmedida == 'QUILOGRAMA LIQUIDO':
            un_medida_dict.update({c + 1: 'KG'})
        elif unmedida == 'UNIDADE':
            un_medida_dict.update({c + 1: 'UN'})
        elif unmedida == 'PECA':
            un_medida_dict.update({c + 1: 'PC'})
        else:
            un_medida_dict.update({c + 1: unmedida})
        c += 1
    return un_medida_dict

def getItemValorMoedaOriginal():
    # Função que retorna os valores unitários dos itens em sua moeda original
    get = nfe.getElementsByTagName('valorUnitario')
    valor_dict = dict()
    c = 0
    for i in get:
        item = float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-7:])
        valor_dict.update({c + 1: item})
        c = c + 1
    return valor_dict

def getItemValorReal():
    # Função que retorna os valores unitários dos itens em Real Brasileiro R$
    get = nfe.getElementsByTagName('valorUnitario')
    vr_dict = dict()
    c = 0
    for i in get:
        item = round(float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-7:])
                     * getCambioMoedaProd(), 6)
        vr_dict.update({c + 1: item})
        c = c + 1
    return vr_dict

def getItemQuantidade():
    # Função que retorna as quantidades adquiridas dos itens
    get = nfe.getElementsByTagName('quantidade')
    quantidade_dict = dict()
    c = 0
    for i in get:
        item = int(get[c].firstChild.data[:9])
        quantidade_dict.update({c + 1: item})
        c = c + 1
    return quantidade_dict

def calcVrTotalProdutoReal():
    # Função que calcula e retorna os valores totais de cada item em Real Brasileiro R$
    vr_total_dict = dict()
    c = 1
    for i in getItemQuantidade():
        vr_total = round(getItemValorReal().get(c) * getItemQuantidade().get(c), 4)
        vr_total_dict.update({c: vr_total})
        c += 1
    return vr_total_dict
valor_total_real = calcVrTotalProdutoReal() # Variável que armazena os valores totais de cada item em Real Brasileiro R$
soma_vr_total_produtos = sum(valor_total_real.values()) # Variável que armazena o valor total em Real Brasileiro R$
                                                        # de todos os itens da DI

def calcVrSeguroProduto():
    # Função que calcula e retorna os valores de seguro de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao valor total de produtos * Valor total do seguro da adição
    vr_seguro_dict = dict()
    c = 1
    for i in getItemQuantidade():
        vr_seguro = round(valor_total_real[c] / soma_vr_total_produtos * float(sum(getSeguroAdicao().values())), 2)
        vr_seguro_dict.update({c: vr_seguro})
        c = c + 1
    return vr_seguro_dict

def calcVrFreteProduto():
    # Função que calcula e retorna os valores de frete de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor total do frete da adição
    vr_frete_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_frete_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrFreteAdicao().values(),
                                                   getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_frete_adicao, 2)
                vr_frete_dict.update({c: valor})
                c += 1
    return vr_frete_dict

def calcVrCIFProduto():
    # Função que calcula e retorna os valores CIF de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor CIF da adição
    vr_cif_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_cif_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getCIFAdicao().values(),
                                                   getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_cif_adicao, 2)
                vr_cif_dict.update({c: valor})
                c += 1
    return vr_cif_dict

def calcVrAFRMMProduto():
    # Função que calcula e retorna os valores de AFRMM de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao valor total de produtos * Valor total de AFRMM da adição
    vr_afrmm_dict = dict()
    c = 1
    for i in getItemQuantidade():
        vr_afrmm = round(valor_total_real[c] / soma_vr_total_produtos * float(sum(afrmm_global.values())), 2)
        vr_afrmm_dict.update({c: vr_afrmm})
        c = c + 1
    return vr_afrmm_dict

def calcVrSiscomexProduto():
    # Função que calcula e retorna os valores de Siscomex de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao valor total de produtos * Valor total de Siscomex da adição
    vr_siscomex_dict = dict()
    c = 1
    for i in getItemQuantidade():
        vr_siscomex = round(valor_total_real[c] / soma_vr_total_produtos *
                              float(sum(getVrSiscomexAdicao().values())), 2)
        vr_siscomex_dict.update({c: vr_siscomex})
        c = c + 1
    return vr_siscomex_dict

def calcVrIpiProduto():
    # Função que calcula e retorna os valores de Ipi de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Ipi da adição
    vr_ipi_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_ipi_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrIpiAdicao().values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_ipi_adicao, 2)
                vr_ipi_dict.update({c: valor})
                c += 1
    return vr_ipi_dict

def calcBcIIProduto():
    # Função que calcula e retorna os valores da base de cálculo do I.I. de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Bc I.I. da adição
    bc_ii_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_bc_ii_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getBcIIAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_bc_ii_adicao, 2)
                bc_ii_dict.update({c: valor})
                c += 1
    return bc_ii_dict

def calcVrIIProduto():
    # Função que calcula e retorna os valores de I.I. de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de I.I. da adição
    vr_ii_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_ii_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrIIAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_ii_adicao, 2)
                vr_ii_dict.update({c: valor})
                c += 1
    return vr_ii_dict

def calcBcPisCofinsProduto():
    # Função que calcula e retorna os valores da base de cálculo de Pis/Cofins de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Bc Pis/Cofins da adição
    bc_pis_cofins_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_bc_piscofins_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getBcPisCofinsAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_bc_piscofins_adicao, 2)
                bc_pis_cofins_dict.update({c: valor})
                c += 1
    return bc_pis_cofins_dict

def caclVrPisProduto():
    # Função que calcula e retorna os valores de Pis de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Pis da adição
    vr_pis_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_pis_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrPisAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_pis_adicao, 2)
                vr_pis_dict.update({c: valor})
                c += 1
    return vr_pis_dict

def caclcVrCofinsProduto():
    # Função que calcula e retorna os valores de Cofins de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Cofins da adição
    vr_cofins_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_cofins_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrCofinsAdicao().values(),
                                                  getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_cofins_adicao, 2)
                vr_cofins_dict.update({c: valor})
                c += 1
    return vr_cofins_dict

def caclcVrAcrescimoProduto():
    # Função que calcula e retorna os valores de Acréscimo de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Acréscimo da adição
    vr_acrescimo_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_acrescimo_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrAcrescimoAdicao().values(),
                                                         getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_acrescimo_adicao, 2)
                vr_acrescimo_dict.update({c: valor})
                c += 1
    return vr_acrescimo_dict

def getAliqIcmsProduto():
    # Função que retorna as alíquotas de Icms de cada item. A fórmula usada é:
    aliq_icms_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_bc_icms_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), aliqicms_global.values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = vr_bc_icms_adicao
                aliq_icms_dict.update({c: valor})
                c += 1
    return aliq_icms_dict

def calcBcIcmsProduto():
    # Função que calcula e retorna os valores de base de cálculo de Icms de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Bc Icms da adição
    vr_bc_icms_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vr_bc_icms_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), bcicms_global.values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vr_bc_icms_adicao, 2)
                vr_bc_icms_dict.update({c: valor})
                c += 1
    return vr_bc_icms_dict

def calcVrIcmsProduto():
    # Função que calcula e retorna os valores de Icms de cada item. A fórmula usada é:
    # Razão do valor do produto em relação ao VMLD da adição * Valor de Icms da adição
    vr_icms_dict = dict()
    c = 1
    for adicao_item in getNrAdicaoItens().values():
        for adicao, vricms_adicao, vmld_adicao in zip(getVrIIAdicao().keys(), getVrIcmsAdicao().values(),
                                                      getVrProdutosXmlAdicao().values()):
            if adicao_item == adicao:
                valor = round((valor_total_real[c] / vmld_adicao) * vricms_adicao, 2)
                vr_icms_dict.update({c: valor})
                c += 1
    return vr_icms_dict

def calcVrFinalProdutoNota():
    # Função que calcula e retorna os valores finais de cada item (Como normalmente o despachante calcula).
    # A fórmula usada é: Vr Produto em Real + Vr Seguro + Vr Frete + Vr Acréscimo + Vr II
    vr_final_dict = dict()
    vr_seguro = calcVrSeguroProduto().values()
    vr_frete = calcVrFreteProduto().values()
    vr_acrescimo = caclcVrAcrescimoProduto().values()
    vr_ii = calcVrIIProduto().values()
    c = 1
    for prod, seguro, frete, acrescimo, ii in zip(valor_total_real.values(), vr_seguro, vr_frete, vr_acrescimo, vr_ii):
        vr_final = round(prod + seguro + frete + acrescimo + ii, 4)
        vr_final_dict.update({c: vr_final})
        c += 1
    return vr_final_dict

def itensToDataFrame():
    # Função para criar os dfs de cada coluna e no final gera o df concatenando todas as colunas
    df0 = pd.DataFrame(getNrAdicaoItens().items()).rename(columns={0: "Item", 1: "Adição"}).set_index('Item')
    df1 = pd.DataFrame(getNrSeqItem().items()).rename(columns={0: "Item", 1: "NrSeqItem"}).set_index('Item')
    df2 = pd.DataFrame(getItemDescricao().items()).rename(columns={0: "Item", 1: "Descricao"}).set_index('Item')
    df3 = pd.DataFrame(getUnMedidaProduto().items()).rename(columns={0: "Item", 1: "UnMedida"}).set_index('Item')
    df5 = pd.DataFrame(getItemValorMoedaOriginal().items()).rename(columns={0: "Item", 1: "Vr un Moeda Original"})\
        .set_index('Item')
    df6 = pd.DataFrame(getItemValorReal().items()).rename(columns={0: "Item", 1: "Vr un R$ - XML"})\
        .set_index('Item')
    df7 = pd.DataFrame(getItemQuantidade().items()).rename(columns={0: "Item", 1: "Quantidade"}).set_index('Item')
    df8 = pd.DataFrame(valor_total_real.items()).rename(columns={0: "Item", 1: "VrProd XML"}).set_index('Item')
    df9 = pd.DataFrame(calcVrFinalProdutoNota().items()).rename(columns={0: "Item", 1: "VrProd Nota"}).set_index('Item')
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
