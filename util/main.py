import urllib.request
from bs4 import BeautifulSoup
from requests_html import HTMLSession

#wiki = 'https://shopee.com.br/Kit-5-Vasilhas-Pl%C3%A1sticas-Bacia-Grande-Media-Pequena-Circular-e-Oval-i.363295119.13013475049?sp_atk=34b671b5-f91f-4e3a-9d2b-4b3669cdfe78&xptdk=34b671b5-f91f-4e3a-9d2b-4b3669cdfe78'
#page = urllib.request.urlopen(wiki)
#soup = BeautifulSoup(page, 'html5lib')
#print(soup.prettify())


#list_item = soup.find('li', attrs={'class': 'toclevel-2 tocsection-26'})
#name = list_item.text.strip()
#print(soup.find_all('span'))


session = HTMLSession()
url = 'https://shopee.com.br/Kit-5-Vasilhas-Pl%C3%A1sticas-Bacia-Grande-Media-Pequena-Circular-e-Oval-i.363295119.13013475049?sp_atk=34b671b5-f91f-4e3a-9d2b-4b3669cdfe78&xptdk=34b671b5-f91f-4e3a-9d2b-4b3669cdfe78'

r = session.get(url)

#Render the page, up the number on scrolldown to page down multiple times on a page
r.html.render(sleep=1, keep_page=True, scrolldown=1)

#take the rendered html and find the element that we are interested in
videos = r.html.find('_3g8My')

#loop through those elements extracting the text and link
print(videos)
