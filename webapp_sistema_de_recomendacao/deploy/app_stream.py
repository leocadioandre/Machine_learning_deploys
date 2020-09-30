import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import webbrowser
from utils import *



def main():
    st.image("static\logo_andre.png")
    st.write("# Sistema de recomendação - Dashboard ")
    opcoes = ['Dashboard', 'Motivações para o projeto', 'Contatos']
    choice = st.sidebar.selectbox("Escolha uma opção", opcoes)
    
    if choice == 'Dashboard':
        st.sidebar.info("Dashboard")
        st.subheader('Principais informações')
        st.info('Nesta seção apresento as informações dos carros com melhor pontuação no sistema (score > 0.7)')
        data = load_data()
                
        if st.checkbox('Mostrar os dados'):
            st.write('(0: possui - 1: não possui)')
            st.dataframe(data.head())
            if st.checkbox('Shape'):
                st.write('(linhas, colunas)')
                st.write(data.shape)
            if st.checkbox('Colunas'):
                columns = data.columns
                st.write(columns)
            if st.checkbox('Informações extras'):
                data_info(data)
            if st.checkbox('Marcas'):
                st.write(data['marca'].value_counts())
            if st.checkbox('Modelos'):
                st.write(data['modelo'].value_counts())
                
        st.header('Gráfico de Disperção')
        st.subheader('Preço x Kilometragem')
        scatter = scater_price_mileage(data)
        scatter
                
        st.header('Gráficos de Barras')
        st.subheader('Modelo x Preço médio')
        scatter1 = mean_price(data)
        scatter1

        st.subheader('Modelo x Ano')
        scatter2 = model_regdate_count(data)
        scatter2
                
        st.subheader('Status do financiamento')
        scatter3 = financial_(data)
        scatter3
                
        st.subheader('Modelo x Potência')
        scatter4 = model_power_count(data)
        scatter4    
                
        st.subheader('Preço x Potência')
        scatter5 = model_power_price(data)
        scatter5

    elif choice == 'Motivações para o projeto':
        st.sidebar.info('Projeto')
        st.markdown(motivacao)
        st.subheader("Fases do Projeto:")
        st.image("static\diagram_project.png")
                
    
    elif choice == 'Contatos':
        st.sidebar.info("André Leocádio")
        url1 = "https://www.linkedin.com/in/andr%C3%A9-leoc%C3%A1dio-80824115b/"
        url2 = "https://github.com/leocadioandre"
        if st.sidebar.button('Linkedin'):
            webbrowser.open_new_tab(url1)
        if st.sidebar.button('Github'):
            webbrowser.open_new_tab(url2)
                
                
        #st.sidebar.image("", width =  300)
        st.subheader('Sobre mim:')
        st.markdown(sobre_mim)     
        
motivacao = """ A motivação para o desenvolvimento do projeto, veio em realizar parte das tarefas que contemplam um projeto de ciências de dados. Onde utilizei uma motivação pessoal em analisar carros para uma futura compra familiar, portanto treinei os dados com características que eu buscava, e desse modo tornei possível realizar a otimização de uma busca que poderia durar dias dentro de sites de vendas de automóveis. Por meio deste projeto é possivel realizar uma analise em minutos e obter os scores indicando os carros com as melhores características, evitando assim  a utilização de tempo próprio. Portanto o sistema de recomendação utiliza um aplicativo da web que procura por carros em uma página web, processa os dados e os passa por um modelo de Machine Learning para listar e exibir os carros que estão mais relacionados ao que estou procurando.

Realiza: web scraping, análise de dados, machine learning e aplicação web
"""

sobre_mim = """ Economista e estudante do background em cientista de dados, que desde o início da graduação, se viu impressionado de como a junção entre a matemática, estatística e os dados que existem em nossa volta, podem apresentar um caminho abrangente para retiradas de insights em negócios e nos trazer um aumento de produtividade e melhorar nossas previsões. Entrei assim na área de ciências de dados, a qual me trouxe ferramentas que me permitem desnevolver uma visão mais exata e analítica do mundo em nossa volta. Mestre em economia aplicada, com foco no desenvolvimento de modelos em econometria. Busco por meio de minha experiência prévia, novos caminhos em que possa aprender e repassar os conhecimentos adquiridos. """
        
if __name__ == '__main__':
    main()
                
                
                
