"""
Segue o case:

Você é o responsável por desenvolver um crawler na linguagem Python (obrigatório usar Selenium, BeautifulSoup e orientação a objetos).
O crawler deverá pegar todas os nomes (name), símbolos (symbol) e preços (price (intraday)) do site https://finance.yahoo.com/screener/new.

Deve ser passado o parâmetro de entrada "region" com o nome da região para ser usado como filtro. 

A saída deve ser um arquivo csv.
 

Exemplo buscando por Argentina:

"symbol","name","price"

"AMX.BA","América Móvil, S.A.B. de C.V.","2089.00"
"NOKA.BA","Nokia Corporation","557.50"

...

A entrega deve ser o link do github com o projeto. Imporante ter um ReadMe.

Será considerado um diferencial a implementação de testes unitários.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def get_stock_data():
    url = 'https://finance.yahoo.com/screener/new'
    driver = webdriver.Chrome()  # caminho para o WebDriver
    driver.get(url)
    
    # Espera o carregamento dos resultados
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    
    # Cria um objeto BeautifulSoup com o código fonte da página carregada
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Encontra a tabela HTML
    table = soup.find('table')

    # Encontra todas as linhas da tabela, ignorando a primeira linha (cabeçalho)
    rows = table.find_all('tr')[1:]  # Aqui ignora o cabeçalho
    
    data = []
    for row in rows:
        # Encontra todas as células da linha
        cols = row.find_all('td')

        # Extrai o texto de cada célula
        symbol = cols[0].text
        name = cols[1].text
        price = cols[2].text

        # Adiciona os dados extraídos à lista
        data.append([symbol, name, price])
    
    driver.quit()
    return data

def save_to_csv(data):
    # Cria um DataFrame do pandas e salva em um arquivo CSV
    df = pd.DataFrame(data, columns=['symbol', 'name', 'price'])
    df.to_csv('stocks.csv', index=False)

if __name__ == "__main__":
    data = get_stock_data()
    save_to_csv(data)
    print('Os dados foram salvos em stocks.csv')
