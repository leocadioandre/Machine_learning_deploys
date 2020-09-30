import streamlit as st
from util import *
import altair as alt
import pandas as pd

# <===============================================   load_df    ========================================================>

def load_data():
    
    path = "dashboard_cars.json"
    car_data = pd.read_json(path, lines = True)
    add_extra_features = extra_variables(car_data)
    clean_data = clean_df(add_extra_features)
    
    
    
    
    return clean_data


# <===============================================   clean_df    ========================================================>

def clean_df(df):
    
    """ Renomeia as colunas e subistitue os missings values e 0s
    
    Arg:
    df(dataframe): df com as informações
    
    Returns:
    df(dataframe): retorna o dataframe formatado
    """
    
    cols = ['marca', 'modelo', 'preço', 'transmissão', 'tipo', 'ano' , 'kilometragem',
            'potência', 'combustível', 'direção', 'cor', 'portas', 'financiamento']
    
    #Retorna valores missing como 'sem_informacao' string
    df[cols] = df[cols].replace(0, 'sem informacao')
    
    #formato o nome da marca
    df[cols] = df[cols].replace('gmchevrolet', 'chevrolet')
    
    df[cols] = df[cols].replace('vwvolkswagen', 'volkswagen')
    
    #formata o valor da potência
    
    df[cols] = df[cols].replace('2.02.9', '2.0_2.9')
    df[cols] = df[cols].replace('4.0oumais', '4.0+')
    
    #formata a quilometragem pela média
    
    df['kilometragem'] = df['kilometragem'].replace(0, int(df['kilometragem'].mean()))
    
    
    
    return df
    
# <===============================================   extrafeatures    ========================================================>        
        
    
def extra_variables(df):
    
    
    """ Cria colunas individuais para cada opcional (extra)
    
    Arg:
    
    df(dataframe): dataframe que será modificado

    Returns:
    
     df(dataframe): dataframe com as colunas indicativos dos extras do carro.
     
     """
    
    string_length = [len(x) if type(x) == str else x for x in df.extra]
    
    greater_length = max(string_length)
    
    greater_length_index = max([(v, i) for i, v in enumerate(string_length)])[1]
    
    extra_variables = df.iloc[greater_length_index].extra
    
    number_of_variables = len(extra_variables.rsplit(','))
    
    
    for feature in range(number_of_variables):
        colname = extra_variables.rsplit(',')[feature].strip()
        df[colname] = 0.0
        
   
    df = df.rename(columns = {'brand':'marca', 'model':'modelo', 'price': 'preço', 'gearbox': 'transmissão', 'cartype': 'tipo', 
                              'regdate': 'ano' , 'mileage': 'kilometragem', 'motorpower':'potência', 
                              'fuel': 'combustível','car_steering':'direção', 'carcolor': 'cor', 'doors': 'portas', 
                              'financial': 'financiamento', 'c mera de ré': 'camera de ré'})
    
    df = fill_in_features(df)
    
    return df

# <===============================================   extrafeatures    ========================================================>

def fill_in_features(df):
    '''Preenche as células da variável informando se o carro contém o respectivo equipamento.
    
    ARG: df(dataframe): O dataframe que será preenchido
    
    RETURNS: df(dataframe): Retorna o dataframe com  as colunas que contém os equipamentos preenchidas.
    '''
    
    #index da coluna 'extra'
    
    columns = list(df.columns)
    index = columns.index('extra')
    
    
    for feature in df.columns[(index+1):]: #Indica as colunas que devem ser preenchidas
        
        total_rows = df.shape[0] #número maximo de linhas a serem iteradas
        
        for row in range(total_rows): #iteração das linhas
            
            is_zero = (df.extra[row] == 0) #se a coluna extra para o item é 0, continuar 0
            
            if is_zero == True:
                
                df[feature].values[row] = 0.0
                
            else:
                
                contains_feature = feature in df.extra[row] 
                
                if contains_feature == True:
                    df[feature].values[row] = 1
                else: 
                    continue
                    
    
    df.drop('extra', axis = 1, inplace = True)
    
    return df

# <===============================================   data_info    ========================================================>


def data_info(df):
    
    
    cols = ['vidro elétrico',
            'air bag',
            'trava elétrica',
            'ar condicionado',
            'direção hidráulica',
            'alarme',
            'som',
            'sensor de ré',
            'camera de ré']

    st.write("Equipamentos com maior presença: ")
    st.write(df[cols].sum())
    st.write("Modelos com maior presença: ")
    st.write(df['modelo'].value_counts())
    st.write("Estatística descritiva - Kilometragem ")
    st.write(df['kilometragem'].describe().T)
    st.write("Estatística descritiva - Preço ")
    st.write(df['preço'].describe())
    
# <===============================================   Gráficos    ========================================================>

def scater_price_mileage(df):  
    selection = alt.selection_multi(fields =['marca'], bind='legend')

    domain = ['chevrolet', 'volkswagen', 'ford']
    range_ = ['steelblue', 'mediumvioletred', 'silver']

    chart = alt.Chart(df).transform_calculate(
        ).mark_point().encode(
            x='preço:Q',
            y='kilometragem',
            color=alt.Color('marca', scale=alt.Scale(domain=domain, range=range_)),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
            tooltip=['marca:N', 'modelo:N', 'preço:N', 'kilometragem:N']
        ).add_selection(
            selection
    )
    return chart

# <======================================================================================================================>


def mean_price(df):
    selection = alt.selection_multi(fields=['modelo'], bind='legend')
    
    domain = ['focus', 'cruze', 'ecosport', 'fiesta', 'spin', 'cobalt', 'onix', 'prisma', 'fusion', 
              'tracker', 'polo', 'jetta', 'golf', 'escort']
    range_ = ['#416ca6', '#7b9bc3', '#e9e9e9', '#7eb6d9','#4f4b43','#2c4786', '#425559', '#dce2f2','#011c40', '#DC143C',
             '#32CD32', '#8A2BE2', '#D2691E', '#000080']

    chart = alt.Chart(df).mark_bar().encode(
        alt.X('mean(preço)', axis=alt.Axis(tickSize=0)),
        alt.Y('modelo', stack='center'),
        #alt.Color('model:N', scale=alt.Scale(scheme='tableau20')),
        color=alt.Color('modelo', scale=alt.Scale(domain=domain, range=range_)),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
    ).add_selection(
        selection
    )
    return chart

# <======================================================================================================================>

def model_regdate_count(df):

    selection = alt.selection_multi(fields=['ano'], bind='legend')


    chart = alt.Chart(df).mark_bar().encode(
    alt.X('count()', axis=alt.Axis(tickSize=0)),
    alt.Y('modelo', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['ano','count()'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'ano:O'
    ).add_selection(
    selection
    )
    return chart
# <======================================================================================================================>

def financial_(df):

    selection = alt.selection_multi(fields=['financiamento'])


    chart = alt.Chart(df).mark_bar().encode(
    alt.X('count()', axis=alt.Axis(tickSize=0)),
    alt.Y('financiamento', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['count()'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'financiamento:O'
    ).add_selection(
    selection
    )
    return chart
# <======================================================================================================================>

def model_power_count(df):
    
    selection = alt.selection_multi(fields=['potência'], bind='legend')
    
    chart = alt.Chart(df).mark_bar().encode(
    x = 'count()',
    y = alt.Y('modelo', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['potência','count()'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'potência:O'
    ).add_selection(
    selection
    )
    
    return chart

# <======================================================================================================================>

def model_power_price(df):
    
    selection = alt.selection_multi(fields=['potência'], bind='legend')
    
    chart = alt.Chart(df).mark_bar().encode(
    x = 'mean(preço)',
    y = alt.Y('modelo', sort = alt.Sort(encoding = 'x', order= 'descending')),
    tooltip = ['potência','mean(preço)'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    color = 'potência:O'
    ).add_selection(
    selection
    )
    return chart