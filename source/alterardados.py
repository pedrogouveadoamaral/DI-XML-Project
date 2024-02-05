from lxml import etree

def alterar_valores_tag(arquivo_xml, nome_tag, novo_valor):
    c = 1
    try:
        # Analisar o arquivo XML usando lxml
        tree = etree.parse(arquivo_xml)

        # Encontrar todas as ocorrências da tag desejada
        tags_alterar = tree.findall('.//' + nome_tag)

        if tags_alterar:
            for tag in tags_alterar:
                # Alterar o valor da tag
                tag.text = f'{novo_valor}'
                c += 1

            # Salvar as alterações de volta no arquivo XML com codificação UTF-8
            tree.write(arquivo_xml, encoding='utf-8', xml_declaration=True)
            print(f'Todos os valores da tag "{nome_tag}" foram alterados para "{novo_valor}" com sucesso.')
        else:
            print(f'Tag "{nome_tag}" não encontrada no XML.')

    except Exception as e:
        print(f'Erro ao processar o XML: {e}')

# Exemplo de uso
arquivo_xml = 'nota_nova.xml'
nome_tag = 'numeroDI'
novo_valor = '123456789'

alterar_valores_tag(arquivo_xml, nome_tag, novo_valor)
