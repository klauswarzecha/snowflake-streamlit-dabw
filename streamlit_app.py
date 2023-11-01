import pandas as pd
import requests
import streamlit as st

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruit_url = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt' 

my_fruit_list = pd.read_csv(fruit_url, index_col='Fruit')
# The tutorial uses two steps instead of one
# my_fruit_list = pd.read_csv(fruit_url)
# my_fruit_list = my_fruit_list.set_index('Fruit')

# Provide some defaults for the multiselect picker
fruits_selected = st.multiselect(
    'Pick some fruits', 
    list(my_fruit_list.index), 
    ['Avocado', 'Strawberries']
)

fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

fruityvice_response = requests.get('https://fruityvice.com/api/fruit/watermelon')
streamlit.text(fruityvice_response.status_code)
