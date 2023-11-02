import pandas as pd
import requests
import streamlit as st
from snowflake import connector as sfc
from urllib.error import URLError


def get_fruityvice_data(fruit_choice):
    """Return nutrition data for a selected fruit obtained
    from an API call to fruityvice"""
    fruity_url = f'https://fruityvice.com/api/fruit/{fruit_choice}'
    response = requests.get(fruity_url)
    fruity_tabular = pd.json_normalize(response.json())
    return fruity_tabular

def get_fruit_load_list():
    """Fetch the complete fruit list"""
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
    """"Append new fruit to list"""
    with my_cnx.cursor() as my_cursor:
        my_cursor.execute("insert into fruit_load_list values ('" + new_fruit + "')")
        # my_cursor.execute(f"insert into fruit_load_list values ('" +  + "')")
        return f'Thank you for adding {new_fruit}.'
    
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

# Fruityvice advice from API 
st.header('Fruityvice Fruit Advice!')
fruit_question = 'What fruit would you like information about?'
try: 
    fruit_choice = st.text_input(fruit_question)
    if not fruit_choice:
        st.error('Please select a fruit to get information')
    else:
        fruity_tabular = get_fruityvice_data(fruit_choice) 
        st.dataframe(fruity_tabular)
except URLError as e:
    st.error()

# Load fruit list
if st.button('Get Fruit Load List'):
    my_cnx = sfc.connect(**st.secrets.snowflake)
    my_data_rows = get_fruit_load_list()
    st.header('The fruit load list contains:')
    st.dataframe(my_data_rows)

# st.stop()
add_fruit_question = 'What fruit would you like to add?'
add_fruit_choice = st.text_input(add_fruit_question)
if add_fruit_choice:
    my_cnx = sfc.connect(**st.secrets.snowflake)
    message = insert_row_snowflake(add_fruit_choice)
    st.text(message)
