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
    def __init__(self, url, titulo, avaliacao, preco, vendas, informacoes, estoque): 
        self.url = url
        self.titulo = titulo 
        self.avaliacao = avaliacao
        self.preco = preco 
        self.vendas = vendas
        self.informacoes = informacoes

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
    canvas.line(30, 720, 550, 720)

def escreveQuebraLinha(texto, coordx):
    global linhaAtual
    if len(texto) > 45:
        textoQuebrado = textwrap.wrap(texto, width=45)
        canvas.drawString(coordx, linhaAtual, textoQuebrado[0])
        canvas.drawString(coordx, linhaAtual, textoQuebrado[1])
        linhaAtual - 40
    else:
        canvas.drawString(coordx, linhaAtual, texto)
        linhaAtual - 20

def adicionarProduto(produto, index):
    global linhaAtual
    print(">> Adicionando ao arquivo o produto " + str(index + 1) + "...")
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(40, linhaAtual, str(index + 1) + ". " + produto.titulo)
    linhaAtual = linhaAtual - 25

    canvas.setFont("Helvetica", 12)
    canvas.drawString(50, linhaAtual, "Avalicação: " + produto.avaliacao + " | Preço: " + produto.preco + " | Vendas: " + produto.vendas)
    linhaAtual = linhaAtual - 20
    canvas.drawString(50, linhaAtual, "Link: " + produto.url)
    linhaAtual = linhaAtual - 20
    canvas.drawString(50, linhaAtual, produto.informacoes)
    linhaAtual = linhaAtual - 40

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

    listaProdutos.append( Produto(url, titulo, avaliacao[0], preco[0], vendas[0], informacoes) )
    navegador.quit()

autor = input("Digite o seu nome: ")
nomeProduto = input("Digite o nome do produto: ")
listaLinks = input("Digite a lista de links: ")

if type(listaLinks) is str:
    listaLinks = [listaLinks]

for i in range(len(listaLinks)):
    pegarInformacoes(listaLinks[i], i)

cabecalhoPDF(autor, nomeProduto)

for i in range(len(listaProdutos)):
    adicionarProduto(listaProdutos[i], i)

print(">> Arquivo PDF gerado! Encerrando a aplicação...")
canvas.save()

