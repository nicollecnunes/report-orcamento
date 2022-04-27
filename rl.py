from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import re
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date


dirAtual = os.path.dirname(__file__)
canvas = canvas.Canvas(dirAtual + "\\RelatorioOrcamento.pdf", pagesize = A4)

canvas.setFont("Helvetica-Bold", 30)
canvas.drawCentredString(300, 770, "Orçamento - " + "produto tal")
canvas.setFont("Helvetica", 15)
canvas.drawCentredString(300, 740, "Por: " + "Nicolle Nunes" + " | Gerado em: " + date.today().strftime("%B %d, %Y"))
canvas.line(30, 720, 550, 720)
linhaAtual = 690

canvas.setFont("Helvetica-Bold", 18)
canvas.drawString(40, linhaAtual, "titulo do produto")
linhaAtual = linhaAtual - 25
canvas.setFont("Helvetica", 12)
canvas.drawString(50, linhaAtual, "Avalicação: " + "nava" + " | Preço: " + "R$0,00" + " | Vendas: " + "999" + "| " + "infojhdf" + " em estoque")
linhaAtual = linhaAtual - 20
canvas.drawString(50, linhaAtual, "Link: " + "www.cocjdskf")
linhaAtual = linhaAtual - 20
canvas.drawString(50, linhaAtual, "dfhsjakdfjbjdksldjfdksl")
linhaAtual = linhaAtual - 40

canvas.save()