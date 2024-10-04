from bs4 import BeautifulSoup
import urllib.request
import requests
import random

def get_article_links():    
    parser = 'html.parser'  
    links = []

    #GET BAYEDE NEWS LINKS
    resp = urllib.request.urlopen("https://bayedenews.com/")
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('https://bayedenews.com/20'):
            links.append(link['href'])

    #GET ILANGA NEWS LINKS
    resp = urllib.request.urlopen("https://ilanganews.co.za/")
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('https://ilanganews.co.za/') and not 'category' in link['href'] and not 'author' in link['href']:
            links.append(link['href'])

    return links

def get_article_content():
    
    article_content = []
    article_links = get_article_links()
    count = 1
    for link in article_links:
        print('Reading article {} of {}. .'.format(count, len(article_links)))
        html_content = requests.get(link).text
        soup = BeautifulSoup(html_content, "lxml")
        article_text = ''
        if link.startswith('https://bayedenews.com/'):
            
            article = soup.find("div", {"class":"post-content entry-content"}).findAll('p')
            for element in article:
                article_text += '\n' + ''.join(element.findAll(text = True))
                
            article_content.append(article_text)
        else:
            try:
                article = soup.find("div", {"class":"td-post-content tagdiv-type"}).findAll('p')
                for element in article:
                    article_text += '\n' + ''.join(element.findAll(text = True))
                    
                article_content.append(article_text)
            except Exception:
                pass
            
        count += 1
    return article_content

def generate_corpus():
   
   result = input('Enter your search word:\n')
   res = [ele for ele in get_article_content() if(result in ele)]
   
   if res:
       f = open('corpus.txt', 'w')
       for article in res:
           f.write(str(article))
           f.write('\n\n')
       f.close()
       print("Your corpus has been generated")
   else:
       print("We couldn't find the word you entered")
         

generate_corpus()

