# Importações

from source import ReadXML
import pandas as pd

# Variável com o XML parseado
nfe = ReadXML.nfe

# Informação complementar
def getinformacaoComplementar():
    # Função que retorna uma string com os dados contidos dentro da tag de Informação Complementar.
    get = nfe.getElementsByTagName('informacaoComplementar')
    informacao_complementar = get[0].firstChild.data
    return informacao_complementar


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

# Números das adições:
def getNrAdicao():
    # Função que retorna os números de cada adição.
    get = nfe.getElementsByTagName('numeroAdicao')
    nr_adicoes_dict = dict()
    c = 0
    for i in get:
        item = int(get[c].firstChild.data)
        nr_adicoes_dict.update({c + 1: item})
        c += 1
    return nr_adicoes_dict

# Valores por Adição

def getVrProdutosXmlAdicao():
    # Função que retorna os valores totais de produtos por adição.
    get = nfe.getElementsByTagName('valorTotalCondicaoVenda')
    produtos_dict = dict()
    c = 0
    for i in get:
        tag_value = get[c].firstChild.data
        if len(tag_value) == 8:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:1] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tag_value) == 9:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:2] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tag_value) == 10:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:3] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})

        if len(tag_value) == 11:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:4] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tag_value) == 12:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:5] +
                                                "." + get[c].firstChild.data[-7:]) * getCambioMoedaProd(), 2)})
        if len(tag_value) == 13:
            produtos_dict.update({c + 1: round(float(get[c].firstChild.data[:6] +
                                                "." + get[c].firstChild.data[-6:]) * getCambioMoedaProd(), 2)})
        c += 1
    return produtos_dict


def getVrFreteAdicao():
    # Função que retorna os valores de Frete por adição.
    get = nfe.getElementsByTagName('freteValorReais')
    frete_dict = dict()
    c = 0
    for i in get:
        frete_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return frete_dict


def getSeguroAdicao():
    # Função que retorna os valores de Seguro por adição.
    get = nfe.getElementsByTagName('valorReaisSeguroInternacional')
    seguro_dict = dict()
    c = 0
    for i in get:
        seguro_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return seguro_dict


def getVrAcrescimoAdicao():
    # Função que retorna os valores de Acréscimo por adição.
    get_adicao = nfe.getElementsByTagName('adicao')
    vr_acrescimo_dict = dict()
    c = 1
    for i in get_adicao:
        get_acrescimo = i.getElementsByTagName('acrescimo')
        if get_acrescimo:
            # Se a tag <acrescimo> existir no XML, recupera os valores das tags <valorReais>
            valor_reais = get_acrescimo[0].getElementsByTagName('valorReais')[0].firstChild.nodeValue
            if len(valor_reais) == 15:
                vr_acrescimo_dict.update({c: float(valor_reais[:13] + "." + valor_reais[-2:])})
        else:
            vr_acrescimo_dict.update({list(getNrAdicao().values())[c -1]: 0.0})
        c += 1
    return vr_acrescimo_dict


def getCIFAdicao():
    # Função que calcula e retorna os valores de CIF por adição.
    # A fórmula é: Vr Produtos + VrFrete + VrSeguro + VrAcréscimo
    cif_dict = dict()
    for adicao, produtos, frete, seguro, acrescimo in zip(
            getNrAdicao().values(), getVrProdutosXmlAdicao().values(),
            getVrFreteAdicao().values(), getSeguroAdicao().values(), getVrAcrescimoAdicao().values()):
        soma = round(float(produtos + frete + seguro + acrescimo), 2)
        cif_dict.update({adicao: soma})
    return cif_dict


def getBcIIAdicao():
    # Função que retorna as bases de cálculo de Imposto de Importação (I.I.) por adição.
    get = nfe.getElementsByTagName('iiBaseCalculo')
    bc_ii_dict = dict()
    c = 0
    for i in get:
        bc_ii_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return bc_ii_dict


def getAliqII():
    # Função que retorna as alíquotas de Imposto de Importação (I.I.) por adição.
    get = nfe.getElementsByTagName('iiAliquotaAdValorem')
    aliq_ii_dict = dict()
    c = 0
    for i in get:
        aliq_ii_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliq_ii_dict


def getVrIIAdicao():
    # Função que retorna que os valores de Imposto de Importação (I.I.) por adição.
    get = nfe.getElementsByTagName('iiAliquotaValorRecolher')
    vr_ii_dict = dict()
    c = 0
    for i in get:
        vr_ii_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vr_ii_dict


def getBcPisCofinsAdicao():
    # Função que retorna que os valores de base de cálculo de Pis e Cofins por adição.
    get = nfe.getElementsByTagName('pisCofinsBaseCalculoValor')
    bc_piscofins_dict = dict()
    c = 0
    for i in get:
        bc_piscofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return bc_piscofins_dict


def getBcPisCofinsTotal():
    # Função que retorna o valor total de base de cálculo de Pis e Cofins.
    get = nfe.getElementsByTagName('pisCofinsBaseCalculoValor')
    bc_piscofins_dict = dict()
    c = 0
    for i in get:
        bc_piscofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    bc_pis_cofins_total = sum(bc_piscofins_dict.values())
    return bc_pis_cofins_total


def getAliqCofinsAdicao():
    # Função que retorna as alíquotas de Cofins por adição.
    get = nfe.getElementsByTagName('cofinsAliquotaAdValorem')
    aliq_cofins_dict = dict()
    c = 0
    for i in get:
        aliq_cofins_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliq_cofins_dict


def getVrCofinsAdicao():
    # Função que retorna os valores de Cofins por adição.
    get = nfe.getElementsByTagName('cofinsAliquotaValorRecolher')
    vr_cofins_dict = dict()
    c = 0
    for i in get:
        vr_cofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vr_cofins_dict


def getAliqPisAdicao():
    # Função que retorna as alíquotas de Pis por adição.
    get = nfe.getElementsByTagName('pisPasepAliquotaAdValorem')
    aliq_pis_dict = dict()
    c = 0
    for i in get:
        aliq_pis_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliq_pis_dict


def getVrPisAdicao():
    # Função que retorna os valores de Pis por adição.
    get = nfe.getElementsByTagName('pisPasepAliquotaValorRecolher')
    vr_cofins_dict = dict()
    c = 0
    for i in get:
        vr_cofins_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vr_cofins_dict


def getNCMAdicao():
    # Função que retorna os códigos NCM por adição.
    get = nfe.getElementsByTagName('dadosMercadoriaCodigoNcm')
    ncm_dict = dict()
    c = 0
    for i in get:
        ncm_dict.update({c + 1: int(get[c].firstChild.data)})
        c += 1
    return ncm_dict

def getAliqIpi():
    # Função que retorna as alíquotas de Ipi por adição.
    get = nfe.getElementsByTagName('ipiAliquotaAdValorem')
    aliq_ipi_dict = dict()
    c = 0
    for i in get:
        aliq_ipi_dict.update({c + 1: float(get[c].firstChild.data[:3] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return aliq_ipi_dict

def getVrIpiAdicao():
    # Função que retorna os valores de Ipi por adição.
    get = nfe.getElementsByTagName('ipiAliquotaValorRecolher')
    vr_ipi_dict = dict()
    c = 0
    for i in get:
        vr_ipi_dict.update({c + 1: float(get[c].firstChild.data[:13] + "." + get[c].firstChild.data[-2:])})
        c += 1
    return vr_ipi_dict


def getVrSiscomexAdicao():
    # Função que retorna os valores de Siscomex por adição.
    # Variáveis
    dados = getinformacaoComplementar().replace('-', '').replace('.', '').splitlines()
    busca = ['Taxa Siscomex', 'SCOMEX: R$', 'SISCOMEX ( 7811 )', 'SISCOMEX 7811']
    vr_siscomex_dict = dict()
    c = 0
    total_bc = getBcPisCofinsTotal()
    # Loop para ler a informação complentar e procuras as string informadas na variável busca.
    for i in dados:
        for j in busca:
            if j in i:
                vr_siscomex_dict.update({c + 1: float(i[-7:].replace(',', '.')
                                                      .translate(str.maketrans('', '', ' R$Xx:')))})
                c += 1
    # Verificações
    # 1 - Verifica se o tamanho de vr_siscomex_dict é maior que a quantidade de adições. Se for True, então verifica
    # se o valor da soma dos valores dentro de vr_siscomex_dict é igual ao primeiro valor de Siscomex encontrado.
    # Caso seja True, então a primeira chave com seu valor é removido do dict. Isso pode ocorrer em casos de o Siscomex
    # ser informado totalizado no início da informação complementar, e também ter os valores descritos por adição.
    if len(vr_siscomex_dict) > len(getNrAdicao()):
        if round(sum(vr_siscomex_dict.values()) - list(vr_siscomex_dict.values())[0], 2) \
                == list(vr_siscomex_dict.values())[0]:
            new_dict = dict()
            for key, value in zip(vr_siscomex_dict.keys(), vr_siscomex_dict.values()):
                new_dict.update({key - 1: value})
            vr_siscomex_dict = new_dict
            vr_siscomex_dict.pop(0)

            return vr_siscomex_dict

    # 2 - Verifica se o tamanho de vr_siscomex_dict é igual a 0. Se for True, quer dizer que a DI não possui Siscomex
    # e então é passado o valor de 0 em cada chave.
    if len(vr_siscomex_dict) == 0:
        for iv in getNrAdicao().values():
            vr_siscomex_dict.update({iv: 0.0})
        return vr_siscomex_dict

    # 3 - Verifica se o tamanho de vr_siscomex_dict é igual a quantidade de adições. Se for True, então quer dizer que
    # os valores de Siscomex foram informados para cada adição, e então retorna o vr_siscomex_dict sem alteração.
    if len(vr_siscomex_dict) == len(getNrAdicao()):
        return vr_siscomex_dict

    # 4 - Verifica se o tamanho de vr_siscomex_dict é = a 1 e a quantidade de adições é > que 1. Se for True, calcula o
    # valor de Siscomex por adição e retorna o vr_siscomex_dict com os valores atualizados.
    if len(vr_siscomex_dict) == 1 and len(getNrAdicao()) > 1:
        for vr_u_siscomex, iv in zip(vr_siscomex_dict.values(), vr_siscomex_dict.keys()):
            for nr_adicao, vr_bc_adicao, in zip(getNrAdicao(), getBcPisCofinsAdicao().values()):
                vr_siscomex_dict.update({nr_adicao: round(float(vr_u_siscomex * (vr_bc_adicao / total_bc)), 2)})
            return vr_siscomex_dict


def inAliqIcms():
    # Função que retorna as alíquitos de ICMS por adição.
    # Variáveis
    aliq_icms_dict = dict()
    # Variáveis para trabalhar com as decisões
    # Listas para os ifs e whiles
    nao = ['N', 'Não', 'n', 'não', 'nao']
    sim = ['S', 'Sim', 's', 'sim']
    simnao = sim + nao
    # Decisão 1
    texto_decisao_1 = 'A DI possui incidência de ICMS?\nDigite S para Sim e N para Não: '
    # Decisão 2
    texto_decisao_2 = 'Todas as adições possuem a mesma alíquota de ICMS?\nDigite S para Sim e N para Não: '
    # Se opção errada
    opcao_errada = 'Opção errada! Informe a opção correta!'

    # Inicio

    # Decisão 1
    decisao_1 = input(f'{texto_decisao_1}')
    while decisao_1 not in simnao:
        print(opcao_errada)
        decisao_1 = input(f'{texto_decisao_1}')

    if decisao_1 in nao:
        for i in decisao_1:
            for ii in getNrAdicao().values():
                aliq_icms_dict.update({ii: 0.00})
            return aliq_icms_dict

    if decisao_1 in sim:
        # Decisão 2
        decisao_2 = input(f'{texto_decisao_2}')
        while decisao_2 not in simnao:
            print(opcao_errada)
            decisao_2 = input(f'{texto_decisao_2}')

        if decisao_2 in sim:
            while True:
                entrada = input('Informe o valor da alíquota ICMS: ')
                try:
                    valor = float(entrada)
                    for i in getNrAdicao().values():
                        aliq_icms_dict.update({i: valor})
                    return aliq_icms_dict
                except ValueError:
                    print('Não é um número válido! Informe um valor correto.')

        if decisao_2 in nao:
            for i in getNrAdicao().values():
                while True:
                    entrada = input(f'Informe o valor da alíquota ICMS da adição {i}: ')
                    try:
                        valor = float(entrada)
                        aliq_icms_dict.update({i: float(valor)})
                        break
                    except ValueError:
                        print('Não é um número válido! Informe um valor correto.')

        return aliq_icms_dict
aliqicms_global = inAliqIcms() # Variável global que armazena as alíquiros de ICMS de cada adição.


def getVrAFRMMAdicao():
    # Função que retorna o valor de AFRMM por adição.
    get = getinformacaoComplementar().replace('-', '').replace('.', '').replace(':', '') .splitlines()
    # Variáveis para trabalhar com as decisões
    # Listas para os ifs e whiles
    nao = ['N', 'Não', 'n', 'não', 'nao']
    sim = ['S', 'Sim', 's', 'sim']
    sim_nao = sim + nao
    # Decisão
    texto_decisao = 'A DI possui incidência de AFRMM?\nDigite S para Sim e N para Não: '
    # Se opção errada
    opcao_errada = 'Opção errada! Informe a opção correta!'
    # Verificação do valor AFRMM digitado
    valorerrado = 'Valor errado!\n Informe um valor numérico inteiro ou decimal com . na separação dos décimos.'
    # Demais variáveis
    busca = ['Afrmm', 'AFRMM', 'Marinha Mercante']
    afrmm_dict = dict()
    totalfrete = sum(getVrFreteAdicao().values())
    c = 0

    # Início
    # Decisão 1
    decisao = input(f'{texto_decisao}')
    while decisao not in sim_nao:
        print(opcao_errada)
        decisao = input(f'{texto_decisao}')

    if decisao in nao:
        for i in decisao:
            for ii in getNrAdicao().values():
                afrmm_dict.update({ii: 0.00})
            return afrmm_dict

    for iii in get:
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
afrmm_global = getVrAFRMMAdicao() # Variável global que armazena os valores da AFRMM por adição


def getBCIcmsAdicao():
    # Função que calcula e retorna o valor da base de ICMS de cada adição.
    nr_adicao = getNrAdicao()
    base_icms_dict = dict()
    vr_cif = getCIFAdicao()
    vr_ii = getVrIIAdicao()
    vr_ipi = getVrIpiAdicao()
    vr_pis = getVrPisAdicao()
    vr_cofins = getVrCofinsAdicao()
    vr_siscomex = getVrSiscomexAdicao()
    vr_afrmm = afrmm_global
    aliq_icms = aliqicms_global
    for adicao, cif, ii, ipi, pis, cofins, siscomex, afrmm, aliquota in \
            zip(nr_adicao.values(), vr_cif.values(), vr_ii.values(), vr_ipi.values(),
                vr_pis.values(), vr_cofins.values(), vr_siscomex.values(), vr_afrmm.values(), aliq_icms.values()):
        fatorbase = round(float(1 - (aliquota * 0.01)), 2)
        total = (cif + ii + ipi + pis + cofins + siscomex + afrmm)
        calcbase = round(float(total / fatorbase), 2)
        base_icms_dict.update({adicao: calcbase})
    return base_icms_dict
bcicms_global = getBCIcmsAdicao() # Variável global que armazena os valores de base de ICMS por adição


def getVrIcmsAdicao():
    # Função que calcula e retorna o valor de ICMS de cada adição.
    aliquota = aliqicms_global
    vr_icms_dict = dict()
    c = 1
    for base_icms, aliquota in zip(bcicms_global.values(), aliquota.values()):
        vr_icms_dict.update({c: round(float(base_icms * (aliquota * 0.01)), 2)})
        c += 1
    return vr_icms_dict


def getPesoLiq():
    # Função que retorna as informações de peso líquido e unidade de medida estatística dos itens das adições.
    get_un_medida = nfe.getElementsByTagName('dadosMercadoriaMedidaEstatisticaUnidade')
    get_peso_liq = nfe.getElementsByTagName('dadosMercadoriaPesoLiquido')
    un_medida_dict = dict()
    peso_liq_dict = dict()
    c = 0
    for i, ii in zip(get_un_medida, get_peso_liq):
        if get_un_medida[c].firstChild.data == 'QUILOGRAMA LIQUIDO':
            un_medida_dict.update({c + 1: 'KG'})
        if get_un_medida[c].firstChild.data == 'UNIDADE':
            un_medida_dict.update({c + 1: 'UN'})
        peso_liq_dict.update({c + 1: float(get_peso_liq[c].firstChild.data[:10] + "."
                                           + get_peso_liq[c].firstChild.data[-5:])})
        c += 1
    return un_medida_dict, peso_liq_dict


def getVrProdutosNotaAdicao():
    # Função que retorna o cálculo do valor final dos produtos. Normalmente esse valor final é calculado pelos
    # despachantes somando o valor CIF + o valor do II.
    adicoes = getNrAdicao().values()
    vr_cif = getCIFAdicao().values()
    vr_ii = getVrIIAdicao().values()
    vr_produtos_nota_dict = dict()
    for adicao, cif, ii in zip(adicoes, vr_cif, vr_ii):
        soma = round(float(cif + ii), 2)
        vr_produtos_nota_dict.update({adicao: soma})

    return vr_produtos_nota_dict


def totaisAdicaoToDataFrame():
    # Função para criar os dfs de cada coluna e no final gera o df concatenando todas as colunas.
    df0 = pd.DataFrame(getNCMAdicao().items()).rename(columns={0: "Adição", 1: "NCM"}).set_index("Adição")
    df1 = pd.DataFrame(getPesoLiq()[0].items()).rename(columns={0: "Adição", 1: "UnMedida"}).set_index("Adição")
    df2 = pd.DataFrame(getPesoLiq()[1].items()).rename(columns={0: "Adição", 1: "PesoLiq"}).set_index("Adição")
    df3 = pd.DataFrame(getVrProdutosXmlAdicao().items()).rename(columns={0: "Adição", 1: "VrProdutosXml"})\
        .set_index("Adição")
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
    df17 = pd.DataFrame(getAliqCofinsAdicao().items()).rename(columns={0: "Adição", 1: "AliqCofins"})\
        .set_index("Adição")
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
