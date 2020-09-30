from get_data import *
from ml_models import *
import time
import numpy as np

#indicando o ano e as marcas que está procurando.

makers = ["ford", "vw-volkswagen", "gm-chevrolet"]
year_1 = "31" # 2013
year_2 = "38" # 2020

urll = "https://pr.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/{maker}/flex?o={page}&re={year_2}&rs={year_1}"

#User-agent usado no chrome

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def update_db(maker = makers, url = urll, header = headers):
    with open("novos_carros.json", 'w+') as output, open("dashboard_cars.json", 'w+') as file:
        for maker in makers:
            for page in range(1,8):
                search_page = download_page(maker, page)
                car_list = parse_search_page(search_page, maker = maker)
                
                for car in car_list:
                    car_page = download_car_page(car['link'])
                    car_json_data = parse_car_page(car_page, car['link'])
                    if car_json_data == None:
                        pass
                    
                    pred = prediction(car_json_data)
                                                         
                    
                    if float(pred) >= 0.7:
                        dashboard_data = dashboard_car_info(car_json_data)
                        file.write("{}\n".format(json.dumps(dashboard_data)))
                                                         
                    car_id = car_json_data.get('link','')
                                                    
                    if car_json_data['version'] == 0:
                                                         
                        data_front = {'car':car_json_data['model'], 'score': np.round(float(pred),3), 'car_id':car_id}
                                                         
                    else:
                        
                        data_front = {'car':car_json_data['version'], 'score': np.round(float(pred),3), 'car_id':car_id}  
                                                         
                                                         
                    data_front['update_time'] = time.time_ns()
                    print(car_id, json.dumps(data_front))
                    output.write("{}\n".format(json.dumps(data_front)))
                                                         
    return True
                                                         
                                                         
                                                         
                                                         
                                                         
                                                         