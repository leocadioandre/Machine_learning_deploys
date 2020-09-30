import numpy as np
import pandas as pd


# <===============================================   del_rows    ========================================================>

def del_rows(df, features):
    
    '''Deleta as linhas onde a variável especificada é zero
    
    ARG:
    df(dataframe): O dataframe que irá ser processado
    features: As variáveis que podem possuir zeros e devem ser retiradas do data frame
    
    RETURNS:
    df_drop(dataframe): O dataframe com as variáveis especificadas deletadas.'''
    
    df_drop = df.copy()
    
    for feature in features:
        #Linhas onde as variáveis são igual a zero, indicando o index
        zeros_index = df_drop.loc[df_drop[feature] == 0, : ].index
        #dropando as linhas
        df_drop = df_drop.drop(zeros_index, axis = 0)

    df_drop = df_drop.reset_index(drop=True)
    
    return df_drop

# <===============================================   del_rows    ========================================================>

def one_hot_encode(df, variable_name, toplabels_x):
    
    """ Cria variáveis dummies para as categorias mais frequentes.
    O restante das categorias serão consideradas ruido.
    
    Arg:
    
    df(dataframe): dataframe que será modificado
    variable_name(string): Nomes das variáveis
    toplabels_x (integer): Número das variáveis mais frequentes
    
    Returns:
    
     df(dataframe): dataframe com as variáveis mais frequentes recodificadas.
     """
    
    top_x = [x for x in df[variable_name].value_counts().sort_values(ascending = False).head(toplabels_x).index]
    
    
    for label in top_x:
         
        df[variable_name+ '_' + string(label)] = np.where(df[variable_name] == label,1,0)
        
    df.drop([variable_name], axis = 1, inplace = True)
    
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
        
    
    df = fill_in_features(df)
    
    
    return df

# <=============================================    fill_in_features  =================================================>

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


# <=============================================         empty_price         =================================================>

def empty_price(df):
    
    """ Deleta as linhas com valores vazios de preços
    
    ARG: df(dataframe): O dataframe que será modificado
    
    RETURNS: df(dataframe): Retorna o dataframe com  as colunas sem os valores vazios.
    """
    
    #checa se existe linha com preço vazios.
    empty_price = np.where(df.applymap(lambda x: x == ''))[0]
    
    #deleta as linhas com preços vazios e reseta o index.
    
    empty_df = df.drop(index = empty_price, inplace= True)
    
    empty_df  = empty_df.reset_index(drop=True)
    
    return empty_df
    
    
# <===============================================   clean_df    ========================================================>

def clean_df(df):
    
    #drop preços vazios.
    cleaned_price = empty_price(df)
    
    #deleta as linhas em que os valores das colunas indicadas é zero
    colnames = [ 'price', 'model', 'mileage']

    df = del_rows(df, colnames)
    
    #Converte para numérico
    df.astype({'price': 'int64',
               'regdate': 'int',
               'mileage': 'int64'}).dtypes
    
    #Criando colunas bool (0 e 1) para as extra features (One hot encode)
    df = extra_variables(cleaned_price)
    
    #nas variáveis categóricas, aplicando one hot encoder nas que possuem maiores frequências
    
    to_dummies = ['financial', 'brand', 'cartype', 'model','gearbox', 'motorpower', 'fuel', 'car_steering','carcolor',
             'exchange']

    
    top_x_labels = [5, 3, 7, 24, 4, 7, 3, 5, 8, 3]
    
    for feature, top_x in zip(to_dummies, top_x_feat):
        df_dummies = one_hot_encode(df, variable_name = feature, toplabels_x = top_x)
        
    return df
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


