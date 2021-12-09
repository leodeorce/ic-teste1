import requests
from bs4 import BeautifulSoup


## Primeira página ##

url = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Obtém o "div" pai do "h2" que identifica o link desejado
content = soup.find(id="parent-fieldname-text")
h2_tags = content.find_all("h2")

# Procura tag "h2" com o texto que identifica a última versão do padrão TISS
for tag in h2_tags:
	if "Padrão TISS" in tag.text and "Versão" in tag.text:
		h2_tag = tag
		break

# Encontra URL da página onde se encontra o botão de download do arquivo
p_tag = h2_tag.find_next("p")
a_tag = p_tag.a
url = a_tag["href"]


## Segunda página ##

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# A única tabela da página contém o botão que procuramos
table_tag = soup.find("table")
tbody_tag = table_tag.find("tbody")
tr_tags = tbody_tag.find_all("tr")

# Procura linha da tabela cuja primeira coluna contém "Componente Organizacional"
for tag in tr_tags:
	if "Componente Organizacional" in tag.find("td").text:
		tr_tag = tag
		break

# Guarda versão para uso no nome do arquivo final
version = tr_tag.find_all("td")[1].text

# Terceira coluna contém tag "a" com URL para download do arquivo desejado
td_tag = tr_tag.find_all("td")[2]
a_tag = td_tag.find("a")
url = a_tag["href"]


## Arquivo PDF ##

# Download do arquivo
response = requests.get(url)

# Escrita do arquivo na pasta de execução
filename = "padrao-tiss_componente-organizacional_" + version + ".pdf"
open(filename, "wb").write(response.content)
