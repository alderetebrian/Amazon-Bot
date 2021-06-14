from amazon_config import(
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    DIRECTORY,
    BASE_URL,
    URL_TESTING
)

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
import time
import os

class AmazonAPI:
    def __init__(self, test_url, base_url):
        self.base_url = base_url
        self.test_url = test_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)

    def run(self):
        #self.driver.get(URL_TESTING)
        #soup = self.soup_file()
        #categorias = self.get_categorias('https://www.amazon.es/b/261-1419186-8055963?ie=UTF8&node=14627860031&ref_=sd_allcat_urban')
        #print(categorias)
        categorias = self.get_categorias_principal(URL_TESTING)
        #print(categorias)
        time.sleep(6)
        cargando = json.loads(categorias)
        self.recursive(cargando)
        '''
        nueva_lista = []
        for item in cargando:
            nueva_lista.append(self.analizar(item))
        self.makeJson('test',nueva_lista)
        self.driver.quit()
        '''

    def recursive(self, archivo_json):
        nueva_lista = []
        for item in archivo_json:
            nueva_lista.append(self.analizar(item))
        self.makeJson('test',nueva_lista)
        print('cargando json...')
        json_load = self.loadJson('test')
        print('escribiendo json...')
        self.recursive(json_load)
        self.driver.quit()

    def loadJson(self,name):
        with open(f'{name}.json') as json_file:
            data = json.load(json_file)
            return data

    def makeJson(self, name,element):
        print('json creado')
        with open(f'{name}.json', 'w') as outfile:  
            json.dump(element, outfile)
        

    def analizar(self, data):
        for key, value in data.items():
            #if key == 'flag' and value == False:
            if key == 'sub_categoria' and value != '':
                data['flag'] = True

            if key == 'sub_categoria' and value == '':
                try:              
                    for link in data['sub_categoria']:
                        lista = [
                                    {
                                        "titulo": "Echo Flex",
                                        "link": "https://www.amazon.es/dp/B07PFG54H7/257-0017454-4718533?_encoding=UTF8&ref_=sd_allcat_k_echo_cs",
                                        "sub_categoria": "",
                                        "flag": False
                                    }
                                ]
                        link['sub_categoria'] = lista
                        
                        #link['sub_categoria'] = self.get_categorias(link['link'])
                    return data
                except:
                    return data

            elif type(value) is list:
                for item in value:
                    if type(item) is dict:
                        self.analizar(item)



    def get_categorias_principal(self, url):
        time.sleep(6)
        self.driver.get(url)
        soup = self.soup_file()
        try:
            categorias = soup.find_all("div", class_="popover-grouping")
            exclusiones = ["Amazon Prime Video", "Amazon Music", "Amazon Photos", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas", "E-readers y eBooks Kindle", "Juguetes y Bebé", "Alimentación y bebidas", "Moda", "Handmade", "Amazon Launchpad"]
            
            json_terminado = []
            lista_terminada = []
            for categoria in categorias:
                titulo_h2 = categoria.find("h2")
                titulo_principal = titulo_h2.text.strip().replace('\n', ' ')
                titulo_principal = titulo_principal.replace('\t', ' ')
                titulo_principal = titulo_principal.replace('\r', ' ')
                validador = any(titulo_principal in exclusion for exclusion in exclusiones)
                if validador:
                    continue
                else:
                    categorias_validas = titulo_h2.parent
                    links_list = categorias_validas.find_all("a") 
                    lista_terminada = []
                    for link in links_list:
                        titulos_categorias = link.text.strip()
                        titulos_categorias = titulos_categorias.replace('\n', ' ')
                        links_categorias = BASE_URL + link['href']
                        json_data = {
                            'titulo': titulos_categorias,
                            'link': links_categorias,
                            'sub_categoria': '',
                            'flag': False
                        }
                        lista_terminada.append(json_data)
                    
                    categoria_info = {
                        'titulo': titulo_principal,
                        'sub_categoria': lista_terminada,
                        'flag': False
                    }
                json_terminado.append(categoria_info)
            return json.dumps(json_terminado)

        except Exception as e:
            print(e)

    def get_categorias(self, url):
        time.sleep(6)
        #pasa categoria por categoria, en caso de no encontrar nada devolveria None lo cual significa que seria el final.
        self.driver.get(url)
        soup = self.soup_file()
        try:
            left_categorias = soup.find("div", class_='a-column a-span12 apb-browse-left-nav apb-browse-col-pad-right a-span-last')
            get_links = left_categorias.find_all('a', href=True)             
            all_products = soup.find("span", class_="a-size-medium a-color-link a-text-bold")
            arrow_text = left_categorias.find_all("a", class_="a-color-base a-link-normal")
            arrow_icon = left_categorias.find_all("span", class_="apb-browse-back-arrow-icon aok-inline-block")
            links_info = []
            for link in get_links:
                if len(arrow_icon) == len(arrow_text):
                    all_products = BASE_URL + all_products.parent['href']
                    return {'final_url': all_products}
                else:
                    titulo = link.text.strip()
                    titulo = titulo.replace('\n', ' ')
                    titulo = titulo.replace('\t', ' ')
                    titulo = titulo.replace('\r', ' ')
                    sub_link = BASE_URL + link['href']
                    subcategoria = {}
                    subcategoria['titulo'] = titulo
                    subcategoria['link'] = sub_link
                    subcategoria['sub_categoria'] = ''
                    subcategoria['flag'] = False
                    links_info.append(subcategoria)
            #return json.dumps(links_info)
            return links_info
        except Exception as e:
            return {'otro_link': self.driver.current_url}

    def soup_file(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup

if __name__ == "__main__":
    print("HEY!!!")
    amazon = AmazonAPI(URL_TESTING, BASE_URL)
    data = amazon.run()
    print(data)
