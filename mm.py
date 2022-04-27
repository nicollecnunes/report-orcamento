from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import re

def configurarAmbiente():
    opcoesBrowser = webdriver.ChromeOptions()
    opcoesBrowser.add_argument("start-maximized")
    opcoesBrowser.add_experimental_option('excludeSwitches', ['enable-logging'])

    servicos = Service('C:\webdriver\chromedriver.exe')
    navegador = webdriver.Chrome(service = servicos, options = opcoesBrowser)
    return navegador

class Produto:
    def __init__(self, titulo, avaliacao, preco, vendas, informacoes, estoque): 
        self.titulo = titulo 
        self.avaliacao = avaliacao
        self.preco = preco 
        self.vendas = vendas
        self.informacoes = informacoes 
        self.estoque = estoque

def tratarInfoGeral(i):
    i = re.sub('([A-Z])', r' \1', i)
    i = i.replace(" Peças", "Peças: ")
    i = i.split("Quantidade")
    print(i)

listaProdutos = []
url1 = 'https://shopee.com.br/Conjunto-de-Vasilhas-Pl%C3%A1sticas-10-pe%C3%A7as-Oval-M%C3%A9dio-e-Pequena-1-litro-e-600ml-i.363295119.13513455687'
url2 = 'https://shopee.com.br/Kit-4-Pe%C3%A7as-Vasilhas-Plastico-Modelo-Tacho-Qualidade-i.328195416.11152261632?sp_atk=73823ddc-6263-4505-ae2b-aa5c698de90c&xptdk=73823ddc-6263-4505-ae2b-aa5c698de90c'

def pegarInformacoes(url):
    navegador = configurarAmbiente()
    navegador.get(url)

    codigoHTML = navegador.page_source
    soup = BeautifulSoup(codigoHTML, "html.parser")

    titulo = soup.title.string
    
    avaliacao = [element.text for element in soup.find_all("div", {"class": "_3uBhVI"})]
    preco = [element.text for element in soup.find_all("div", {"class": "_2v0Hgx"})]
    vendas = [element.text for element in soup.find_all("div", {"class": "_3b2Btx"})]

    infoGeral = tratarInfoGeral(str([element.text for element in soup.find_all("div", {"class": "flex _3qYU_y _6Orsg5"})]))
    informacoes = infoGeral[0]
    estoque = infoGeral[1]

    listaProdutos.append( Produto(titulo, avaliacao[0], preco[0], vendas[0], informacoes, estoque) )
    navegador.quit()

pegarInformacoes(url1)
pegarInformacoes(url2)

for obj in listaProdutos:
    print( obj.titulo, obj.avaliacao, obj.preco, obj.vendas, obj.informacoes, obj.estoque, sep =' - ' )



