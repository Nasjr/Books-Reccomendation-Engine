import streamlit as st
import pandas as pd
import numpy as np
import pickle
from streamlit_jupyter import StreamlitPatcher, tqdm
from streamlit_option_menu import option_menu
from PIL import Image
import requests
from io import BytesIO


popular_50books=pickle.load(open('Assets//top50boock.pkl','rb'))
similarity_matrix=pickle.load(open('Assets//similaritymatrix.pkl','rb'))
#Reading Data
popular_50books.set_index('Book-Title',inplace=True)
Books=pd.read_csv('Assets//recco_data.csv')
Books.set_index('Book-Title',inplace=True)
Books_list=Books.index.values
st.set_page_config(layout="wide")
st.title("Books Reccomendation app")
image_not_found="https://th.bing.com/th/id/OIP.nGMs9gQ4Oyx1WBikTgVtKAAAAA?pid=ImgDet&w=270&h=270&rs=1"
def get_top_similar_books(book_name):
    scores=similarity_matrix.loc[book_name]
    scores=scores.sort_values(ascending=False)[1:7]
    distances=scores.index
    names=scores.values
    return names,distances
def draw_cols(df,names,interval=2,p_num=2):
        col1,col2,col3=st.columns(3)
        with col1:
            for i in range(0,interval):
                st.divider()
                st.markdown(f"""<h3>{names[i]}</h3>""",unsafe_allow_html=True)
                st.divider()
                try:
                    img_url=df.loc[names[i]]['Image-URL-L']
                    st.image(img_url,use_column_width=True)
                except :
                   st.image(image_not_found)
                st.write(df.loc[str(names[i])]['Book-Author'])
                st.write(df.loc[str(names[i])]['Year-Of-Publication'])
                st.write(df.loc[str(names[i])]['Publisher'])
            st.divider()
        with col2:
            for i in range(interval,interval*p_num):
                st.divider()
                st.markdown(f"""<h3>{names[i]}</h3>""",unsafe_allow_html=True)
                st.divider()
                try:
                    img_url=df.loc[names[i]]['Image-URL-L']
                    st.image(img_url,use_column_width=True)
                except :
                    st.image(image_not_found)
                st.write(df.loc[str(names[i])]['Book-Author'])
                st.write(df.loc[str(names[i])]['Year-Of-Publication'])
                st.write(df.loc[str(names[i])]['Publisher'])
        with col3:
            for i in range(interval*p_num,interval*p_num+interval):
                st.divider()
                st.markdown(f"""<h3>{names[i]}</h3>""",unsafe_allow_html=True)
                st.divider()
                try:
                    img_url=df.loc[names[i]]['Image-URL-L']
                    st.image(img_url,use_column_width=True)
                except :
                    st.image(image_not_found)
                st.write(df.loc[str(names[i])]['Book-Author'])
                st.write(df.loc[str(names[i])]['Year-Of-Publication'])
                st.write(df.loc[str(names[i])]['Publisher'])
def Reccomendation_page(df,Books_list):
    #Streamlit app
    st.write("Pick a Book and we will Reccomend")
    selected_book=st.selectbox("Choose your favourit Book",Books_list)
    st.divider()
    if st.button('Reccomend Books'):
        distances,names=get_top_similar_books(selected_book)
        draw_cols(Books,names,interval=2,p_num=2)

def main_page(df):
    st.header('The most Popular 50 Books Based on Average Ratings')
    st.divider()
    df=popular_50books
    names=popular_50books.index.values
    draw_cols(df,names,interval=15,p_num=2)
       
selected=option_menu(menu_title=None,options=['Home',"Reccomendations"],
                     icons=["House","Books"],
                     default_index=0,
                     orientation='horizontal')
if selected == "Home":
    main_page(popular_50books)
elif selected == "Reccomendations":
    Reccomendation_page(Books,Books_list)

