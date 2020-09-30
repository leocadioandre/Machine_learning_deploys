import re
import time
import requests as rq
import bs4 as bs4
import json
import os 

# <=================================================   GET DATA   ==========================================================> 

#indicando o ano e as marcas que está procurando.

makers = ["ford", "vw-volkswagen", "gm-chevrolet"]
year_1 = "31" # 2013
year_2 = "38" # 2020

url = "https://pr.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/{maker}/flex?o={page}&re={year_2}&rs={year_1}"

#User-agent usado no chrome

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def download_page(maker, page, header = headers, year_1 = '31', year_2= '38'):

    url = "https://pr.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/{maker}/flex?o={page}&re={year_2}&rs={year_1}"
    urll = url.format(maker = maker, page=page, year_2 = year_2, year_1 = year_1)
    
   # Get request -  to request data from the server.
    response = rq.get(urll, headers= headers)
    
    if response == 403:
        print('403 error - Forbidden! Please identify user-agent')
    
    
    return response.text

#<=================================================   parse_search_page   ===================================================> 


def parse_search_page(page_html, maker):
    
    car_list = []
    
    parsed = bs4.BeautifulSoup(page_html, features = "html.parser")
    
    tags = parsed.findAll("a")
    
    for e in tags:
                if e.has_attr('data-lurker_list_id'):
                    link = e['href'] #Indica que href é a tag no codigo fonte que indica o link do anuncio
                    title = e['title']
                    data = {'link':link,
                               'title':title,
                               'maker': maker}
                    car_list.append(data)
                    
    return car_list


#<=================================================   download_car_page   ===================================================> 

def download_car_page(link):
    
    response = rq.get(link, headers = headers)
    
    return response.text

#<=================================================   is_empty_test   ===================================================>



def is_empty_test(car_info):
    
    '''Testa se o obejto car_info é vazio ou não
    ARG: 
    car_info(bs4 object) : Um objeto beautifulsoup contendo as informações do carro
    
    RETURNS:
    True (bool): Uma variável bool  afirmando se o objeto está vazio ou não'''
    
    is_empty = not car_info
    
    if is_empty == True:
    
        return True


#<=================================================   is_null_test   ====================================================>



def is_null_test(feat_):
    '''Verifica se a variável é nula
    ARG: feat_(re): um objeto re contem a informação do carro
    RETURNS:True(bool): uma variável booleana afirma se o objeto é nulo ou não'''
    
    is_null = 'null' in  feat_.group(0)# group(0) diz que toda a parte do feat_ foi escolhida.
    if is_null == True:
        return True
    
#<=================================================   parse_car_page   ====================================================>     
 
def parse_car_page(page_html, car_link):
    
    parsed = bs4.BeautifulSoup(page_html, 'html.parser')
            
    #Acha o pedaço do HTML onde irei achar a informação do carro
    car_info = parsed.find_all(string=re.compile("window.dataLayer") )
            
    #Testa se o objeto bs4(car_info) está vazio
    if is_empty_test(car_info) == True:
        pass
    else:
        return car_info_parser(car_info,car_link )
    
    
#<=================================================   car_info_parser   ====================================================>     

def car_info_parser(car_info, car_link):
    
    '''Gets car information and put it into a dictionary
    ARG:
    car_info(bs4 object):A beautifulsoup object containing car information
    car_link(string) : A string containing the link of the car
    
    RETURNS:
    data(dictionary): A dictionary containing the car features as key'''

    # features
    car_features = ['brand', 'price','cartype','model','gearbox',
                'regdate', 'mileage', 'motorpower', 'fuel', 
                'car_steering', 'carcolor',  'exchange','version','doors','financial','extra']


    data = {}
    
    # add car link to dict
    data['link'] = car_link 

    for feat in car_features:
        
        
        # Verify whether the feature is in the car_info[0] string
        contain_feature = feat in car_info[0]
        
        
        # Get all features information by using regular expressions
        if contain_feature == True:
            

            if feat in ['version','doors','financial']:

               
                feat_ = re.search("{variable}(([^\,]*))".format(variable = feat), car_info[0])
                
                # null test
                if is_null_test(feat_) == True:
                      data[feat] = 0.0
                else:        
                    feature = re.search(":\"(([^\,]*))",feat_.group(0))
                    text = re.sub(r"[^a-zA-Z0-9ãáéóõç.]", " ",  feature.group(0).lower()) 

                    data[feat] = text.strip()


            elif feat == 'extra':

                feat_ = re.search(".(?=extra)([^\}]*)", car_info[0])
                
                # Null test
                if is_null_test(feat_) == True:
                      data[feat] = 0.0
                    
                else:  
                    feature = re.search(":\"(([^\}]*))",feat_.group(1))#no caso mantendo o zero pega apenas o rimeiro termo do dicionario o que não ocorre com o 1
                    text = re.sub(r"[^a-zA-Z0-9ãáéóõç.,]", " ",  feature.group(1).lower())
                    
                    data[feat] = text.strip()


            else:      

                feat_ = re.search("{variable}(([^\,]*))".format(variable = feat), car_info[0]) 
                
                # Null test
                if is_null_test(feat_) == True:
                    
                    data[feat] = 0.0           
                else:
                    feature = re.search(":\"(([^\,]*))",feat_.group(0))
                    text = re.sub(r"[^a-zA-Z0-9ãáéóõç.]", "",  feature.group(0).lower()) 
                 
                    col = feat
                    data[col] = text.strip()

        # If feature is not in car_info[0] string, sets 0 as value
        elif contain_feature == False:
           
            data[feat] = 0.0
    
    
    return data

#<=================================================   dashboard_car_info   ====================================================> 
    

def dashboard_car_info(car_json_data):
    
    dashb_car_json = {}
    features = ['brand','model', 'price', 'gearbox','cartype',
                'regdate', 'mileage', 'motorpower', 'fuel', 
                'car_steering', 'carcolor', 'doors','financial','extra']
    
    for feature in features:
        dashb_car_json[feature] = car_json_data[feature]
        
   
    return dashb_car_json
                