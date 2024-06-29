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
from bs4 import BeautifulSoup
import pandas as pd

class CrawlerTest:
    def __init__(self, url):
        self.url = url
        self.data = []

    def initialize_driver(self):
        self.driver = webdriver.Chrome()  # Inicializa o WebDriver do Chrome
        self.driver.implicitly_wait(40)  # Define um tempo de espera implícito de 10 segundos
        self.driver.get(self.url)  # Abre o site de ações

    def scrape_data(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')  # Analisa e cria um objeto BeautifulSoup com o código fonte da página carregada
        table = soup.find('table')  # Encontra a tabela de ações
        rows = table.find_all('tr')[1:]  # Encontra todas as linhas da tabela, ignorando a primeira linha (cabeçalho)
        
        for row in rows:
            cols = row.find_all('td')

            # Extrai os textos de cada célula
            symbol = cols[0].text
            name = cols[1].text
            price = cols[2].text
            self.data.append([symbol, name, price])  # Adiciona os dados extraídos à lista
        
        self.driver.quit()  # Fecha o navegador

    def save_to_csv(self, filename):
        df = pd.DataFrame(self.data, columns=['symbol', 'name', 'price'])  # Cria um DataFrame
        df.to_csv(filename, index=False)  # Salva em um arquivo CSV

if __name__ == "__main__":
    url = 'https://finance.yahoo.com/screener/new'  # URL utilizada (site de ações)

    scraper = CrawlerTest(url)
    scraper.initialize_driver()
    scraper.scrape_data()
    scraper.save_to_csv('stocks.csv')

    print('Os dados foram salvos em stocks.csv')
