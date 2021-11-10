import gzip
from io import BytesIO
from urllib.request import Request, urlopen
from urllib import request
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    project_name = ''
    base_url = ''
    robo_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    robo_file = ''
    queue = set()
    crawled = set()
    robo = set()

    def __init__(self, project_name, base_url, domain_name, robo_url):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.robo_url = robo_url
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.robo_file = Spider.project_name + '/robots.txt'

        ##
        self.boot()
        self.roboInit(robo_url, Spider.robo_file, Spider.base_url)
        self.crawl_page('First spider', Spider.base_url, Spider.robo)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url, Spider.robo_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.robo = file_to_set_robots(Spider.robo_file, Spider.base_url)

    @staticmethod
    def roboInit(robo_url, robo_file, base_url):
        if robo_url not in Spider.robo:
            print('Creating robots.txt\n')
            #request.urlretrieve(robo_url,robo_file)
            req = Request(robo_url, headers={'User-Agent': 'Mozilla/5.0'})
            arquivo = urlopen(req).read()
            write_file(robo_file, arquivo.decode("utf-8"))
    
        Spider.robo = file_to_set_robots(robo_file, base_url)
        set_to_file(Spider.robo, robo_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url, robo):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url, robo))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url, robo):
        html_string = ''
        try:
            req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req)
            if 'text/html' in response.getheader('Content-Type'):   #Verifica se o dado eh text/html
                html_bytes = response.read()                        #Abre o conteudo html normalmente
                html_string = html_bytes.decode("utf-8")            #Converte o conteudo de bytecode em string
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            try:                                                    #Verifica se o dado eh text/html mas com o formato gzip
                if 'text/html' in response.getheader('Content-Type'):
                    buff = BytesIO(html_bytes)
                    buff2 = gzip.GzipFile(fileobj=buff)
                    html_string = buff2.read().decode('utf-8')
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(html_string)

            except Exception as e:
                print(str(e))
                return set()

        return finder.page_links().difference(robo)                 #Vai comparar com os links encontrados com robots.txt e subtrair

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)                                   #Fazendo a pesquisa de modo BFS

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)