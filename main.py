from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date
import textwrap

listaProdutos = []
dirAtual = os.path.dirname(__file__)
canvas = canvas.Canvas(dirAtual + "\\RelatorioOrcamento.pdf", pagesize = A4)
linhaAtual = 690
class Produto:
    def __init__(self, url, titulo, avaliacao, preco, vendas, informacoes): 
        self.url = url
        self.titulo = titulo 
        self.avaliacao = avaliacao
        self.preco = preco 
        self.vendas = vendas
        self.informacoes = informacoes

def getLinhaAtual():
    global linhaAtual
    return linhaAtual

def subtraiLinhaAtual(valor):
    global linhaAtual
    linhaAtual = linhaAtual - valor

def configurarAmbiente():
    print(">> Configurando ambiente do browser...")
    opcoesBrowser = webdriver.ChromeOptions()
    opcoesBrowser.add_argument("start-maximized")
    opcoesBrowser.add_experimental_option('excludeSwitches', ['enable-logging'])

    servicos = Service('C:\webdriver\chromedriver.exe')
    navegador = webdriver.Chrome(service = servicos, options = opcoesBrowser)
    return navegador

def cabecalhoPDF(nomeProduto, autor):
    print(">> Gerando arquivo PDF...")
    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawCentredString(300, 770, "Orçamento - " + nomeProduto)
    canvas.setFont("Helvetica", 15)
    canvas.drawCentredString(300, 740, "Por: " + autor + " | Gerado em: " + date.today().strftime("%B %d, %Y"))
    canvas.line(30, 720, 570, 720)

def escreveQuebraLinha(coordx, texto):
    if len(texto) > 58:
        textoQuebrado = textwrap.wrap(texto, width=58)
        canvas.drawString(coordx, getLinhaAtual(), textoQuebrado[0])
        subtraiLinhaAtual(20)
        canvas.drawString(coordx, getLinhaAtual(), textoQuebrado[1])
        subtraiLinhaAtual(20)
    else:
        canvas.drawString(coordx, getLinhaAtual(), texto)
        subtraiLinhaAtual(20)

def adicionarProduto(produto, index):
    print(">> Adicionando ao arquivo o produto " + str(index + 1) + "...")

    canvas.setFont("Helvetica-Bold", 18)
    escreveQuebraLinha(40, str(index + 1) + ". " + produto.titulo)
    subtraiLinhaAtual(5)

    canvas.setFont("Helvetica", 12)
    escreveQuebraLinha(50, "Avalicação: " + produto.avaliacao + " | Preço: " + produto.preco + " | Vendas: " + produto.vendas)

    canvas.setFont("Helvetica", 10)
    canvas.drawString(50, getLinhaAtual(), "Link: " + produto.url)
    subtraiLinhaAtual(20)
    
    canvas.setFont("Helvetica", 12)
    escreveQuebraLinha(50, produto.informacoes)
    subtraiLinhaAtual(20)

def tratarInfoGeral(i):
    i = re.sub('([A-Z])', r' \1', i)
    i = i.replace(" Peças", "Peças: ")
    i = i.split("Quantidade")

def pegarInformacoes(url, index):
    print(">> Coletando informações do link " + str(index + 1) + "...")
    navegador = configurarAmbiente()
    navegador.get(url)

    codigoHTML = navegador.page_source
    soup = BeautifulSoup(codigoHTML, "html.parser")
    print("  >> Código HTML recuperado")

    titulo = soup.title.string
    
    avaliacao = [element.text for element in soup.find_all("div", {"class": "_3uBhVI"})]
    preco = [element.text for element in soup.find_all("div", {"class": "_2v0Hgx"})]
    vendas = [element.text for element in soup.find_all("div", {"class": "_3b2Btx"})]
    print("  >> Informações principais coletadas")

    infoGeral = tratarInfoGeral(str([element.text for element in soup.find_all("div", {"class": "flex _3qYU_y _6Orsg5"})]))
    try:
        informacoes = infoGeral[0]
    except:
        informacoes = ""
        print("  >> Erro ao buscar informações secundárias")

    try:
        listaProdutos.append( Produto(url, titulo, avaliacao[0], preco[0], vendas[0], informacoes) )
    except: 
    navegador.quit()

autor = input("Digite o seu nome: ")
nomeProduto = input("Digite o nome do produto: ")
listaLinks = input("Digite a lista de links: ")

if len(listaLinks.split(" ")) == 1:
    listaLinks = [listaLinks]
else:
    listaLinks = listaLinks.split(" ")


print(listaLinks)

for i in range(len(listaLinks)):
    pegarInformacoes(listaLinks[i], i)

cabecalhoPDF(nomeProduto, autor)

for i in range(len(listaProdutos)):
    adicionarProduto(listaProdutos[i], i)

print(">> Arquivo PDF gerado! Encerrando a aplicação...")
canvas.save()

