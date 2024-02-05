# Importações

import os
from xml.dom import minidom

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_xml = os.path.join(diretorio_atual, "nota_nova.xml")

# Variável para parsear o arquivo .XML
nfe = minidom.parse(caminho_xml)
