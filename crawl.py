import urllib
import sqlite3
from bs4 import BeautifulSoup
import requests

conferences = ['www']                                 # conference shortcut on dblp
context_key = set(['change'])                         # keyword in title
arthur_key = set(['Kuo Yu Huang'])                    # arthur's full name
months = ['{:0>2d}'.format(i+1) for i in range(12)]   # month for arxiv
years = ['{:0>2d}'.format(i) for i in range(17, 20)]  # year for conference and arxiv
fields = ['CL']   


def arxiv(results):
    url = 'http://arxiv.org/list/cs.{}/{}{}?show=10000'

    for field in fields:
        for year in years:
            for month in months:
                try:
                    query_url = url.format(field, year, month)
                    print('Retrieving {}'.format(query_url))
                    html_doc = r = requests.get(query_url)
                    soup = BeautifulSoup(html_doc.text, 'html.parser')
                except:
                    continue
                titles = soup.findAll('div', {'class': 'list-title'})
                authors = soup.findAll('div', {'class': 'list-authors'})
                paper_urls = soup.findAll('span', {'class': 'list-identifier'})

                if len(titles) != len(authors):
                    print('number of titles and authors mismatch')
                else:
                    for title, author, paper_url in zip(titles, authors, paper_urls):
                        flag = False
                        titles = title.contents[-1].strip()
                        paper_url = 'https://arxiv.org/abs/' + paper_url.a.text[6:]
                        paper_authors = [au.string.strip() for au in author.findAll('a')]

                        for paper_author in paper_authors:
                            if(paper_author in arthur_key):
                                flag = True
                                break

                        for key in context_key:
                            if(key in titles):
                                flag = True
                                break

                        if(flag):
                            results[titles.strip()] = paper_url
                            continue
                        """
                        html_doc = requests.get(paper_url)
                        soup = BeautifulSoup(html_doc.text, 'html.parser')
                        for word in  soup.find('meta', {'property': 'og:description'})['content'].strip().split():
                            if(title in context_key):
                                flag = True
                                break
                        if(flag):
                            results.append('{0}\t{1}\n'.format(titles,paper_url))
                        """

def dblp(results):
    for conference in conferences:
        query_url = 'https://dblp1.uni-trier.de/db/conf/{0}/'.format(conference)
        html_doc = requests.get(query_url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        temp = soup.find_all('li',{ 'class':"entry editor toc"})
        for _ in temp:
            query_url = _.find('div',{ 'class':"body"}).find('a')['href']
            for year in years:
                if('20{0}'.format(year) in query_url):
                    break
            else:
                continue
            print('Retrieving {}'.format(query_url))
            html_doc = requests.get(query_url)
            soup = BeautifulSoup(html_doc.text, 'html.parser')
            links = soup.find_all('nav',{ 'class':"publ"})
            articles = soup.find_all('article',{ 'class':"data"})
            
            
            for link, article in zip(links, articles):
                flag = False
                paper_url = link.find('a')['href']
                infos = article.find_all('span',{'itemprop':"name"})

                for paper_author in infos[:-1]:
                    if(paper_author.text in arthur_key):
                        flag = True
                        break

                for key in context_key:
                    if(key in infos[-1].text.lower()):
                        flag = True
                        break

                if(flag):
                    results[infos[-1].text.strip()] = paper_url
                    continue

def main():
    results = {}
    arxiv(results)
    dblp(results)

    with open('papers','w') as f:
        for title, data in results.items():
            f.write( "{0}\t{1}\n".format(title, data))

if(__name__ == '__main__'):
    main()

