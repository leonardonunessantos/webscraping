# Imports

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json


# 1 - pegar o conteúdo HTML a partir da url

url = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2021'

option = Options()
option.headless = True

# Abrindo o FireFox
driver = webdriver.Firefox()
# options=option   Para não aparecer o mozille abrindo

# Acessando a URL
driver.get(url)

# Aguardando 10 segundos para o carregamento da pagina
time.sleep(10)


# driver.find_element_by_xpath("//div[@class= 'col-md-8 col-lg-9']//table[@class= 'table m-b-20 tabela-expandir']//thead//tr//th[class= 'p-b-15 p-t-15']").click()
element = driver.find_element_by_xpath(
    "//div[@class= 'col-md-8 col-lg-9']//table[@class= 'table m-b-20 tabela-expandir']")

html_content = element.get_attribute('outerHTML')

# 2 - Parsear o conteúdo HTML - BeautifulSoup - parsea o html e transforma em dado estruturado.
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# 3 - Estruturar o conteúdo em um Data Frame - Pandas - Elimina os dados html e transforma em dado puro
# Aqui, transformamos em string e ja pegamos o top 10!!
df_completo = pd.read_html(str(table))[0].head(6)

df = df_completo[['Posição', 'PTS']]
print(df_completo)
df.columns = ['Time', 'Pontos']

# 4 -Transformando os dados em um dicionário
classificados_liberta = {}
classificados_liberta['G6'] = df.to_dict('records')

driver.quit()

# 5 - Convertendo em um arquivo json
# Transformando o dicionário em json
arq_json = json.dumps(classificados_liberta)
# Abrindo (ou criando) um arquivo
tabela_final = open('Tabela_G6.json', 'w')
# Passando o conteúdo json para o arquivo
tabela_final.write(arq_json)
# Fechando o arquivo
tabela_final.close()
