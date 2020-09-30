import pandas as pd
import re
import joblib as jb
import numpy as np
import json
from scipy.sparse import hstack, csr_matrix

# <=================================================      MODEL        =====================================================> 

#Load models

model_rf = jb.load('model/model_rf.pk.z')
model_lgbm = jb.load('model/model_lgbm.pk;.z')

# <===================================================== Predicoes =========================================================> 

def prediction(data):
    
    feature_array = clean_data(data)
    
    if feature_array is None:
        return 0
    
    pred_rf = model_rf.predict_proba(feature_array)[0][1]
    pred_lgbm = model_lgbm.predict_proba(feature_array)[0][1]
    
    pred = 0.2*pred_rf + 0.8*pred_lgbm   

    return pred

# <=================================================          Limpando os dados        =======================================> 

def clean_data(data):

    cols = ['price','regdate','mileage', 'vidro_elétrico','air_bag',
            'trava_elétrica','ar_condicionado','direção_hidráulica','alarme','som',
            'sensor_de_ré', 'financial_com_multas','financial_de_leilão','financial_financiado','financial_ipva_pago',
            'brand_ford','brand_gmchevrolet', 'brand_vwvolkswagen','model_agile','model_captiva',
            'model_celta', 'model_cobalt','model_compass','model_corsa','model_crossfox',
            'model_cruze', 'model_focus','model_fox', 'model_gol','model_golf',
            'model_grandsaveiro','model_jetta','model_joy','model_ka','model_parati',
            'model_passat','model_polo','model_prisma','model_ranger','model_s10',
            'model_sandero','model_saveiro', 'car_steering_assistida','car_steering_elétrica','car_steering_hidráulica','car_steering_mecnica']


    clean_df = pd.DataFrame(columns = cols, index = [0])
    
    clean_df = clean_price(data, clean_df)
    clean_df = clean_regdate(data, clean_df)
    clean_df = clean_mileage(data, clean_df)
    clean_df = clean_model(data, clean_df)
    #clean_df = clean_steering(data, clean_df)
    clean_df = clean_extra(data, clean_df)
    clean_df = clean_financial(data, clean_df)
    clean_df = clean_brand(data,clean_df)

    if any(clean_df.isnull().iloc[0]):
        return None
    
    feature_array = clean_df.iloc[0].to_numpy()
    
    #define a ordem para alimentar o modelo
    feature_array = feature_array.reshape(-1,46)
    
    return feature_array

# <=================================================        clean_price        =====================================================> 


def clean_price(data, clean_df):
    
        if data['price'] =='':
            clean_df['price'] = None
            
        else:
            numeric_price = int(data['price'])
            clean_df['price'] = numeric_price
            
        return clean_df


# <=================================================        clean_price        =====================================================>

def clean_regdate(data, clean_df):
    
        if data['regdate'] =='0' or data['regdate'] =='' :
            clean_df['regdate'] = None
            
        else:
            numeric_regdate = int(data['regdate'])
            clean_df['regdate'] = numeric_regdate
            
        return clean_df
    
# <=================================================       clean_mileage        =====================================================> 

def clean_mileage(data, clean_df):
    
        if data['mileage'] =='0':
            clean_df['mileage'] = None
            
        else:
            numeric_mileage = int(data['mileage'])
            clean_df['mileage'] = numeric_mileage
            
        return clean_df
    
# <================================================       clean_model            =====================================================> 

def clean_model(data, clean_df):
    
    models = ['agile','captiva','celta', 'cobalt','compass','corsa','crossfox','cruze', 'focus','fox','gol','golf','grandsaveiro',
              'jetta','joy','ka', 'parati','passat','polo','prisma','ranger','s10',
              'sandero','saveiro']
    
    for model in models:
        
        clean_df['model_'+ model] = np.where(data['model'] ==model,1,0)
        
    return clean_df

# <=================================================      clean_steering        =====================================================>  

#def clean_steering(data, clean_df):
    
    #steerings = ['car_steering_assistida','car_steering_elétrica','car_steering_hidráulica','car_steering_mecnica']
    
    #for steering in steerings:
        
        #clean_df['car_steering_' + steering] = np.where(data['steering'] ==steering,1,0)
        
    #return clean_df
        
# <=================================================      clean_extra        =====================================================>  

def clean_extra(data, clean_df):
    
    extras= ['vidro_elétrico',
            'air_bag','trava_elétrica','ar_condicionado','direção_hidráulica','alarme',
            'som','sensor_de_ré', 'car_steering_assistida','car_steering_elétrica','car_steering_hidráulica','car_steering_mecnica']
    
    for extra in extras:
        
        clean_df[extra] = np.where(data['extra'] ==extra,1,0)
        
    return clean_df
        
# <=================================================      clean_financial        =====================================================> 

def clean_financial(data,clean_df):
    
    financials = [ 'com_multas','de_leilão',
                   'financiado','ipva_pago']
    
    for financial in financials:
        
        clean_df['financial_'+financial] = np.where(data['financial'] == financial,1,0)
        
    return clean_df
    

 # <=================================================      clean_brand        =====================================================> 

def clean_brand(data,clean_df):
    
    brands = [ 'ford','gmchevrolet', 'vwvolkswagen']
    
    for brand in brands:
        
        clean_df['brand_'+brand] = np.where(data['brand'] == brand,1,0)
        
    return clean_df
    
    
    
    