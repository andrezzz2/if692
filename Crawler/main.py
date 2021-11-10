import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'NetshoesTeste'
PALAVRAS_CHAVES = ['tenis', 'sapatenis', 'calcado', 'chinelos', 'vestiario']
HOMEPAGE = 'https://www.netshoes.com.br/'
ROBO_URL = 'https://www.netshoes.com.br/robots.txt'

DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
ROBO_FILE = PROJECT_NAME + '/robots.txt'
NUMBER_PAGE = 1000
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, ROBO_URL)

def search_crawler():
    queued_links = file_to_set(QUEUE_FILE)
    crawler_links = file_to_set(CRAWLED_FILE)
    
    if len(queued_links) > 0 and len(crawler_links) <= NUMBER_PAGE:
        print(str(len(queued_links)) + ' links in the queue')
        #funcao_de_busca(queued_links)
        
        if heuristica(queued_links):
            search_crawler()
        else:
            funcao_de_busca(queued_links)
            search_crawler()

def funcao_de_busca(queued_links):
    url = queued_links.pop()

    queued_links.add(url)
    Spider.crawl_page("Thread-1: Utilizando BFS", url, Spider.robo)

def heuristica(queued_links):
    for link in queued_links:
        for set_links in PALAVRAS_CHAVES:
            if set_links in link:
                print(set_links+"\n")
                Spider.crawl_page("Thread-1: Utilizando euristica", link, Spider.robo)
                return True
    return False

search_crawler()