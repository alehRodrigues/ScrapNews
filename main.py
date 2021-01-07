#pip install newspaper3k

import requests
import re
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
from newspaper import Config
import nltk

url_principal = "https://www.msn.com/pt-br/noticias/brasil"


#Sempre bom usar Headers para que os sites mão bloqueiem o bot
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

#Pega a resposta do site em html, sem abrir o navegador
response = (requests.get(url_principal, headers = headers))

#Tranforma o HTML num HTML mais legível
soup = BeautifulSoup(response.content, 'html.parser')

#Procura todas as categorias no site
categories = soup.find_all('a', attrs = {'data-link-type': "category"})
#Procura todas as notícias
news_list = soup.find_all('a', attrs={'href': re.compile("pt-br/noticias/brasil/")})


print("************* Categorias *****************")
for category in categories:
    if("Página Inicial" not in category.get_text()):
        print(category.get_text())
print("*****************************************")

print("************* Links das Notícias *****************")
i = 0
for news in news_list:
    i = i + 1
    print('Notícia:',i)
    print(news.get_text())
    print("https://www.msn.com/" + news.get('href'))
    print(" ")
print("**************************************************")

#Aqui ele vai puxar a primeira notícia, só alterar o indice para puxar outra 
url_news = "https://www.msn.com/" + news_list[0].get('href') 

#Configuração para evitar que de erro de leitura nas páginas web, algumas possuem proteção contra bots de scraping
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

#Biblioteca para encontrar as tags
nltk.download('punkt')

#Pega a notícia
art = Article(url_news, config=config)

art.download()
art.parse()
art.nlp()

print('Título:',art.title)
print('Imagem:',art.top_image)
print('Video:',art.movies)
print('Tags:',art.keywords)
print('Resumo:',art.summary)
print('Texto:',art.text)
print('Autores',art.authors)

#https://newspaper.readthedocs.io/en/latest/
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
