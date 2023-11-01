import pandas as pd
import requests
import streamlit as st
import snowflake.connector

my_cnx = snowflake.connector.connect(streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
st.text('Hello from Snowflake')
st.text(my_data_row)

    
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

# Fruityvice
st.header('Fruityvice Fruit Advice!')
fruit_default = 'Kiwi'
fruit_question = 'What fruit would you like information about?'
fruit_choice = st.text_input(fruit_question, fruit_default)
fruity_url = f'https://fruityvice.com/api/fruit/{fruit_choice}'
response = requests.get(fruity_url)
fruity_tabular = pd.json_normalize(response.json())
# pd.json_normalize converts JSON to a flat table/dataframe
# type of fruity_tabular is
# <class 'pandas.core.frame.DataFrame'>
st.dataframe(fruity_tabular)
