import numpy as np
import os.path
from flask import Flask, render_template
import os
import json
import backend
import time
from datetime import datetime

app = Flask(__name__)


def get_predictions():
    
    
    cars = []
    
    novos_carros_json = "novos_carros.json"
    if not os.path.exists(novos_carros_json):
        backend.update_db()
        
    last_update = os.path.getmtime(novos_carros_json)*1e9
    
    if time.time_ns() - last_update > (60*60*24*1e9): #aprox 1 day
        run_backend.update_db()
        last_update = datetime.datetime.today().strftime('%Y-%m-%d')
        

        
    with open("novos_carros.json", "r") as data_file:
        for line in data_file:
            line_json = json.loads(line)
            cars.append(line_json)
            
  
    
    
    predictions = []
    
    for car in cars:
        predictions.append(
                            {"car_link":car['car_id'],
                             "car":car['car'],
                             "score": np.round(float(car['score']),4)
                           }
                            )

    predictions = sorted(predictions, key = lambda x: x['score'], reverse = True)[:30]
   

        
    return predictions, last_update

@app.route('/')
def main_page():
    
    
    predictions,last_update = get_predictions()
    
    return render_template("index.html", predictions = predictions)




if __name__ ==  '__main__':
    app.run(debug = True, host = 'localhost')