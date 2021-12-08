import requests
from bs4 import BeautifulSoup


## Primeira página

url = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

content = soup.find(id="parent-fieldname-text")
h2_tags = content.find_all("h2")

for tag in h2_tags:
	if "Padrão TISS – Versão" in tag.text:
		h2_tag = tag
		break

p_tag = h2_tag.find_next("p")
a_tag = p_tag.a
url = a_tag["href"]


## Segunda página

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

table_tag = soup.find("table")
tbody_tag = table_tag.find("tbody")
tr_tags = tbody_tag.find_all("tr")

for tag in tr_tags:
	if "Componente Organizacional" in tag.find("td").text:
		tr_tag = tag
		break

version = tr_tag.find_all("td")[1].text
td_tag = tr_tag.find_all("td")[2]
a_tag = td_tag.find("a")
url = a_tag["href"]


## Arquivo PDF

response = requests.get(url)

filename = "padrao-tiss_componente-organizacional_" + version + ".pdf"
open(filename, "wb").write(response.content)
