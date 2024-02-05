# Importações

from source import ReadXML
import pandas as pd

# Variável com o XML parseado
nfe = ReadXML.nfe

# Informação complementar
def getinformacaoComplementar():
    get = nfe.getElementsByTagName('informacaoComplementar')
    informacaoComplementar = get[0].firstChild.data
    return informacaoComplementar

# Moedas negociadas
def getCambioMoedaProd():#Dividindo o valor da tag condicaoVendaValorReais pelo da tag condicaoVendaValorMoeda
    getVrMoedaNegociada = nfe.getElementsByTagName('condicaoVendaValorMoeda')
    vrMoedaNegociada = float(getVrMoedaNegociada[0].firstChild.data[:13] + "." + getVrMoedaNegociada[0].firstChild.data[-2:])
    getVrReais = nfe.getElementsByTagName('condicaoVendaValorReais')
    vrReais = float(getVrReais[0].firstChild.data[:13] + "." + getVrReais[0].firstChild.data[-2:])
    vrMoedaNegociada = round((vrReais / vrMoedaNegociada), 4)
    return vrMoedaNegociada

# Números das adições:
def getNrAdicao():
    get = nfe.getElementsByTagName('numeroAdicao')
    nradicoes_dict = dict()
    c = 0
    for i in get:
        item = int(get[c].firstChild.data)
        nradicoes_dict.update({c + 1: item})
        c += 1
    return nradicoes_dict

# Valores por Adição

def getVrProdutosXmlAdicao():
    get = nfe.getElementsByTagName('valorTotalCondicaoVenda')
    produtos_dict = dict()
    c = 0
    for i in get:
        tagvalue = get[c].firstChild.data
        if len(tagvalue) == 8:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:1] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tagvalue) == 9:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:2] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tagvalue) == 10:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:3] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})

        if len(tagvalue) == 11:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:4] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tagvalue) == 12:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:5] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tagvalue) == 13:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:6] +
                                                "." + get[c].firstChild.data[-6:]) * getCambioMoedaProd(), 2)})
        c += 1
    return produtos_dict

def getVrFreteAdicao():
    get = nfe.getElementsByTagName('freteValorReais')
    frete_dict = dict()
    c = 0
    for i in get:
        frete_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return frete_dict

def getSeguroAdicao():
    get = nfe.getElementsByTagName('valorReaisSeguroInternacional')
    seguro_dict = dict()
    c = 0
    for i in get:
        seguro_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return seguro_dict


def getCIFAdicao():
    cif_dict = dict()
    for adicao, produtos, frete, seguro in zip(
        getNrAdicao().values(), getVrProdutosXmlAdicao().values(),
        getVrFreteAdicao().values(), getSeguroAdicao().values()):
        soma = round(float(produtos + frete + seguro), 2)
        cif_dict.update({adicao: soma})
    return cif_dict

def getBcIIAdicao():
    get = nfe.getElementsByTagName('iiBaseCalculo')
    bcii_dict = dict()
    c = 0
    for i in get:
        bcii_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return bcii_dict

def getAliqII():
    get = nfe.getElementsByTagName('iiAliquotaAdValorem')
    aliqii_dict = dict()
    c = 0
    for i in get:
        aliqii_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliqii_dict

def getVrIIAdicao():
    get = nfe.getElementsByTagName('iiAliquotaValorRecolher')
    vrii_dict = dict()
    c = 0
    for i in get:
        vrii_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vrii_dict

def getBcPisCofinsAdicao():
    get = nfe.getElementsByTagName('pisCofinsBaseCalculoValor')
    bcpiscofins_dict = dict()
    c = 0
    for i in get:
        bcpiscofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return bcpiscofins_dict

def getBcPisCofinsTotal():
    get = nfe.getElementsByTagName('pisCofinsBaseCalculoValor')
    bcpiscofins_dict = dict()
    c = 0
    for i in get:
        bcpiscofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    bcPisCofinsTotal = sum(bcpiscofins_dict.values())
    return bcPisCofinsTotal

def getAliqCofinsAdicao():
    get = nfe.getElementsByTagName('cofinsAliquotaAdValorem')
    aliqcofins_dict = dict()
    c = 0
    for i in get:
        aliqcofins_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliqcofins_dict

def getVrCofinsAdicao():
    get = nfe.getElementsByTagName('cofinsAliquotaValorRecolher')
    vrcofins_dict = dict()
    c = 0
    for i in get:
        vrcofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vrcofins_dict

def getAliqPisAdicao():
    get = nfe.getElementsByTagName('pisPasepAliquotaAdValorem')
    aliqpis_dict = dict()
    c = 0
    for i in get:
        aliqpis_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliqpis_dict

def getVrPisAdicao():
    get = nfe.getElementsByTagName('pisPasepAliquotaValorRecolher')
    vrcofins_dict = dict()
    c = 0
    for i in get:
        vrcofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vrcofins_dict

def getNCMAdicao():
    get = nfe.getElementsByTagName('dadosMercadoriaCodigoNcm')
    ncm_dict = dict()
    c = 0
    for i in get:
        ncm_dict.update({c + 1: int(get[c].firstChild.data)})
        c += 1
    return ncm_dict

def getAliqIpi():
    get = nfe.getElementsByTagName('ipiAliquotaAdValorem')
    aliqipi_dict = dict()
    c = 0
    for i in get:
        aliqipi_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliqipi_dict

def getVrIpiAdicao():
    get = nfe.getElementsByTagName('ipiAliquotaValorRecolher')
    vripi_dict = dict()
    c = 0
    for i in get:
        vripi_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vripi_dict

def getVrSiscomexAdicao():
    dados = getinformacaoComplementar().replace('-', '').replace('.', '').splitlines()
    busca = ['Taxa Siscomex', 'SCOMEX: R$']
    valorSiscomex_dict = dict()
    c = 0
    totalbc = getBcPisCofinsTotal()
    for i in dados:
        for j in busca:
            if j in i:
                valorSiscomex_dict.update({c + 1: float(i[-7:].replace(',', '.').translate(str.maketrans('', '', ' R$Xx:')))})
                c += 1

    if len(valorSiscomex_dict) > len(getNrAdicao()):
        if sum(valorSiscomex_dict.values()) - list(valorSiscomex_dict.values())[0] \
                == list(valorSiscomex_dict.values())[0]:
            newdict = dict()
            for key, value in zip(valorSiscomex_dict.keys(), valorSiscomex_dict.values()):
                newdict.update({key - 1: value})
            valorSiscomex_dict = newdict
            valorSiscomex_dict.pop(0)
            return valorSiscomex_dict

    if len(valorSiscomex_dict) == 0:
        for iv in getNrAdicao().values():
            valorSiscomex_dict.update({iv: 0.0})
        return valorSiscomex_dict

    if len(valorSiscomex_dict) == len(getNrAdicao()):
        return valorSiscomex_dict

    if len(valorSiscomex_dict) == 1 and len(getNrAdicao()) > 1:
        for vrUSiscomex, iv in zip(valorSiscomex_dict.values(), valorSiscomex_dict.keys()):
            for nrAdicao, vrBcAdicao, in zip(getNrAdicao(), getBcPisCofinsAdicao().values()):
                valorSiscomex_dict.update({nrAdicao: round(float(vrUSiscomex * (vrBcAdicao / totalbc)), 2)})
            return valorSiscomex_dict

def inAliqIcms():
    # Variáveis
    aliqicms_dict = dict()
    # Variáveis para trabalhar com as decisões
    # Listas para os ifs e whiles
    nao = ['N', 'Não', 'n', 'não', 'nao']
    sim = ['S', 'Sim', 's', 'sim']
    simnao = sim + nao
    # Decisão 1
    textdecisao1 = 'A DI possui incidência de ICMS?\nDigite S para Sim e N para Não: '
    # Decisão 2
    textdecisao2 = 'Todas as adições possuem a mesma alíquota de ICMS?\nDigite S para Sim e N para Não: '
    # Se opção errada
    opcaoerrada = 'Opção errada! Informe a opção correta!'

    # Inicio

    # Decisão 1
    decisao1 = input(f'{textdecisao1}')
    while decisao1 not in simnao:
        print(opcaoerrada)
        decisao1 = input(f'{textdecisao1}')

    if decisao1 in nao:
        for i in decisao1:
            for ii in getNrAdicao().values():
                aliqicms_dict.update({ii: 0.00})
            return aliqicms_dict

    if decisao1 in sim:
        # Decisão 2
        decisao2 = input(f'{textdecisao2}')
        while decisao2 not in simnao:
            print(opcaoerrada)
            decisao2 = input(f'{textdecisao2}')

        if decisao2 in sim:
            while True:
                entrada = input('Informe o valor da alíquota ICMS: ')
                try:
                    valor = float(entrada)
                    if valor.is_integer():
                        valor = int(valor)
                        for i in getNrAdicao().values():
                            aliqicms_dict.update({i: valor})
                    return aliqicms_dict
                except ValueError:
                    print('Não é um número válido! Informe um valor correto.')

        if decisao2 in nao:
            for i in getNrAdicao().values():
                while True:
                    entrada = input(f'Informe o valor da alíquota ICMS da adição {i}: ')
                    try:
                        valor = float(entrada)
                        if valor.is_integer():
                            valor = int(valor)
                            aliqicms_dict.update({i: float(valor)})
                        break
                    except ValueError:
                        print('Não é um número válido! Informe um valor correto.')

        return aliqicms_dict
aliqicms_global = inAliqIcms()

def getVrAFRMMAdicao():
    dados = getinformacaoComplementar().replace('-', '').replace('.', '').replace(':', '') .splitlines()
    # Variáveis para trabalhar com as decisões
    # Listas para os ifs e whiles
    nao = ['N', 'Não', 'n', 'não', 'nao']
    sim = ['S', 'Sim', 's', 'sim']
    simnao = sim + nao
    # Decisão
    textdecisao = 'A DI possui incidência de AFRMM?\nDigite S para Sim e N para Não: '
    # Se opção errada
    opcaoerrada = 'Opção errada! Informe a opção correta!'
    # Verificação do valor AFRMM digitado
    valorerrado = 'Valor errado!\n Informe um valor numérico inteiro ou decimal com . na separação dos décimos.'
    # Demais variáveis
    busca = ['Afrmm', 'AFRMM', 'Marinha Mercante']
    afrmm_dict = dict()
    totalfrete = sum(getVrFreteAdicao().values())
    c = 0

    # Início
    # Decisão 1
    decisao = input(f'{textdecisao}')
    while decisao not in simnao:
        print(opcaoerrada)
        decisao = input(f'{textdecisao}')

    if decisao in nao:
        for i in decisao:
            for ii in getNrAdicao().values():
                afrmm_dict.update({ii: 0.00})
            return afrmm_dict

    for iii in dados:
        for iv in busca:
            if iv in iii:
                afrmm_dict.update({c + 1: float(iii[-8:].replace(' R$ ', '').replace('$', '').replace(',', '.'))})
                c += 1
    # Veriricação 1 = Se o tamanho do dict for = a 0, retorna um dict com as chaves de valores 0
    if len(afrmm_dict) == 0:
        for v in getNrAdicao().values():
            afrmm_dict.update({v: 0.0})
        return afrmm_dict

    # Verificação 2 = Se o tamanho do dict for = a 0 e o valor do value for = a 0, retorna um dict com valores 0
    if len(afrmm_dict) == 1 and 0 in [a for a in afrmm_dict.values()]:
        for vi in getNrAdicao().values():
            afrmm_dict.update({vi: 0.0})
        return afrmm_dict

    # Verificação 3 - Pode acontecer de encontrar duas ou mais vezes a sigla AFRMM, mas serem sobre a mesma taxa e
    # com o mesmo valor. Nesse caso, está sendo realizada uma vericação, em que se o tamanho do dict for maior que,
    # uma lista será criada dentro de um for para armazenar os valores encontrados no dict, e caso os valores sejam os
    # mesmos, é solicitado ao usuário que informe o valor total correto da AFRMM.
    # Com o valor informado, são feitos os cálculos para encontrar o valor da AFRMM de cada adição.
    # A fórmula é: Valor total da AFRMM * (Valor do Frete por adição / Valor total de Frete)
    if len(afrmm_dict) > 1:
        if all(valor == list(afrmm_dict.values())[0] for valor in afrmm_dict.values()):
            print("Todos os valores da AFRMM encontrados no XML são iguais!")
            afrmm_dict.clear()
            while True:
                entrada = input(f'Informe o valor total correto da AFRMM: ')
                try:
                    valor = float(entrada)
                    if valor.is_integer():
                        valor = int(valor)
                    break
                except ValueError:
                    print('Não é um número válido! Informe um valor correto.')
            for adicao in getNrAdicao().values():
                afrmm_dict.update({adicao: valor})
            for vrUAfrmm, vii in zip(afrmm_dict.values(), afrmm_dict.keys()):
                for nrAdicao, vrFreteAdicao, in zip(getNrAdicao(), getVrFreteAdicao().values()):
                    afrmm_dict.update({nrAdicao: round(float(vrUAfrmm * (vrFreteAdicao / totalfrete)), 2)})
                return afrmm_dict
            if len(afrmm_dict) > 1 and len(getNrAdicao()) > 1:
                return afrmm_dict

    # Verificação 4: Se o tamando do dic for = a 1 a quantidade de adições for maior que 1. Faz os cálculos para
    # encontrar o valor da AFRMM de cada adição. A fórmula é:
    # Valor total da AFRMM * (Valor do Frete por adição / Valor total de Frete)
    if len(afrmm_dict) == 1 and len(getNrAdicao()) > 1:
        for vrUAfrmm, viii in zip(afrmm_dict.values(), afrmm_dict.keys()):
            for nrAdicao, vrFreteAdicao, in zip(getNrAdicao(), getVrFreteAdicao().values()):
                afrmm_dict.update({nrAdicao: round(float(vrUAfrmm * (vrFreteAdicao / totalfrete)), 2)})
            return afrmm_dict
afrmm_global = getVrAFRMMAdicao()

def getVrAcrescimoAdicao():
    getadicao = nfe.getElementsByTagName('adicao')
    vracrescimo_dict = dict()
    c = 1
    for i in getadicao:
        getacrescimo = i.getElementsByTagName('acrescimo')
        if getacrescimo:
            # Se a tag <acrescimo> existir no XML, recupera os valores das tags <valorReais>
            valor_reais = getacrescimo[0].getElementsByTagName('valorReais')[0].firstChild.nodeValue
            if len(valor_reais) == 15:
                vracrescimo_dict.update({c: float(valor_reais[:13] + "." + valor_reais[-2:])})
        else:
            vracrescimo_dict.update({list(getNrAdicao().values())[c -1]: 0.0})
        c += 1
    return vracrescimo_dict

def getBCIcmsAdicao():
    nradicao = getNrAdicao()
    baseicms_dict = dict()
    vrcif = getCIFAdicao()
    vrii = getVrIIAdicao()
    vripi = getVrIpiAdicao()
    vrpis = getVrPisAdicao()
    vrcofins = getVrCofinsAdicao()
    vrsiscomex = getVrSiscomexAdicao()
    vrafrmm = afrmm_global
    vracrescimo = getVrAcrescimoAdicao()
    aliqicms = aliqicms_global
    for adicao, cif, ii, ipi, pis, cofins, siscomex, afrmm, acrescimo, aliquota in \
            zip(nradicao.values(), vrcif.values(), vrii.values(), vripi.values(),
                vrpis.values(), vrcofins.values(), vrsiscomex.values(), vrafrmm.values(), vracrescimo.values(),
                aliqicms.values()):
        fatorbase = round(float(1 - (aliquota * 0.01)), 2)
        total = (cif + ii + ipi + pis + cofins + siscomex + afrmm + acrescimo)
        calcbase = round(float(total / fatorbase), 2)
        baseicms_dict.update({adicao: calcbase})
    return baseicms_dict
bcicms_global = getBCIcmsAdicao()

def getVrIcmsAdicao():
    aliquota = aliqicms_global
    vricms_dict = dict()
    c = 1
    for baseicms, aliquota in zip(bcicms_global.values(), aliquota.values()):
        vricms_dict.update({c: round(float(baseicms * (aliquota * 0.01)), 2)})
        c += 1
    return vricms_dict

def getPesoLiq():
    getunmedida = nfe.getElementsByTagName('dadosMercadoriaMedidaEstatisticaUnidade')
    getpesoliq = nfe.getElementsByTagName('dadosMercadoriaPesoLiquido')
    unmedida_dict = dict()
    pesoliq_dict = dict()
    c = 0
    for i, ii in zip(getunmedida, getpesoliq):
        if getunmedida[c].firstChild.data == 'QUILOGRAMA LIQUIDO':
            unmedida_dict.update({c + 1: 'KG'})
        if getunmedida[c].firstChild.data == 'UNIDADE':
            unmedida_dict.update({c + 1: 'UN'})
        pesoliq_dict.update({c + 1: float(getpesoliq[c].firstChild.data[:10] + "." + getpesoliq[c].firstChild.data[-5:])})
        c += 1
    return unmedida_dict, pesoliq_dict

def getVrProdutosNotaAdicao():
    adicoes = getNrAdicao().values()
    vrcif = getCIFAdicao().values()
    vrii = getVrIIAdicao().values()
    vracrescimo = getVrAcrescimoAdicao().values()
    vrprodutosnota_dict = dict()

    for adicao, cif, ii, acrescimo in zip(adicoes, vrcif, vrii, vracrescimo):
        soma = round(float(cif + ii + acrescimo), 2)
        vrprodutosnota_dict.update({adicao: soma})

    return vrprodutosnota_dict

def totaisAdicaoToDataFrame():
    df0 = pd.DataFrame(getNCMAdicao().items()).rename(columns={0: "Adição", 1: "NCM"}).set_index("Adição")
    df1 = pd.DataFrame(getPesoLiq()[0].items()).rename(columns={0: "Adição", 1: "UnMedida"}).set_index("Adição")
    df2 = pd.DataFrame(getPesoLiq()[1].items()).rename(columns={0: "Adição", 1: "PesoLiq"}).set_index("Adição")
    df3 = pd.DataFrame(getVrProdutosXmlAdicao().items()).rename(columns={0: "Adição", 1: "VrProdutosXml"}).set_index("Adição")
    df4 = pd.DataFrame(getVrProdutosNotaAdicao().items()).rename(columns={0: "Adição", 1: "VrProdutosNota"}).set_index(
        "Adição")
    df5 = pd.DataFrame(getVrFreteAdicao().items()).rename(columns={0: "Adição", 1: "FreteR$"}).set_index("Adição")
    df6 = pd.DataFrame(getSeguroAdicao().items()).rename(columns={0: "Adição", 1: "SeguroR$"}).set_index("Adição")
    df7 = pd.DataFrame(getCIFAdicao().items()).rename(columns={0: "Adição", 1: "CIF"}).set_index("Adição")
    df8 = pd.DataFrame(getBcIIAdicao().items()).rename(columns={0: "Adição", 1: "BcII"}).set_index("Adição")
    df9 = pd.DataFrame(getAliqII().items()).rename(columns={0: "Adição", 1: "AliqII"}).set_index("Adição")
    df10 = pd.DataFrame(getVrIIAdicao().items()).rename(columns={0: "Adição", 1: "ValorII"}).set_index("Adição")
    df11 = pd.DataFrame(getAliqIpi().items()).rename(columns={0: "Adição", 1: "AliqIPI"}).set_index("Adição")
    df12 = pd.DataFrame(getVrIpiAdicao().items()).rename(columns={0: "Adição", 1: "ValorIPI"}).set_index("Adição")
    df13 = pd.DataFrame(getVrSiscomexAdicao().items()).rename(columns={0: "Adição", 1: "Siscomex"}).set_index("Adição")
    df14 = pd.DataFrame(getBcPisCofinsAdicao().items()).rename(columns={0: "Adição", 1: "BcPisCofins"}).set_index(
        "Adição")
    df15 = pd.DataFrame(getAliqPisAdicao().items()).rename(columns={0: "Adição", 1: "AliqPis"}).set_index("Adição")
    df16 = pd.DataFrame(getVrPisAdicao().items()).rename(columns={0: "Adição", 1: "VrPis"}).set_index("Adição")
    df17 = pd.DataFrame(getAliqCofinsAdicao().items()).rename(columns={0: "Adição", 1: "AliqCofins"}).set_index("Adição")
    df18 = pd.DataFrame(getVrCofinsAdicao().items()).rename(columns={0: "Adição", 1: "VrCofins"}).set_index("Adição")
    df19 = pd.DataFrame(afrmm_global.items()).rename(columns={0: "Adição", 1: "AFRMM"}).set_index("Adição")
    df20 = pd.DataFrame(getVrAcrescimoAdicao().items()).rename(columns={0: "Adição", 1: "VrAcrescimo"}).set_index(
        "Adição")
    df21 = pd.DataFrame(aliqicms_global.items()).rename(columns={0: "Adição", 1: "AliqICMS"}).set_index("Adição")
    df22 = pd.DataFrame(bcicms_global.items()).rename(columns={0: "Adição", 1: "BcICMS"}).set_index("Adição")
    df23 = pd.DataFrame(getVrIcmsAdicao().items()).rename(columns={0: "Adição", 1: "VrICMS"}).set_index("Adição")


    df = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17,
                    df18, df19, df20, df21, df22, df23],
                   axis=1, sort=True)
    return df

# totaisAdicaoToDataFrame().to_excel("totaisAdicao.xlsx", sheet_name='DI')
