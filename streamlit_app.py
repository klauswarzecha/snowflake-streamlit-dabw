import pandas as pd
import streamlit as st

st.title('My Parents New Healthy Diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruit_url = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt' 
# the tutorial suggests a misleading name
# my_fruit_list is not a list, but a dataframe!
my_fruit_list = pd.read_csv(fruit_url, index_col='Fruit')

st.multiselect('Pick some fruits', my_fruit_list.index)
st.dataframe(my_fruit_list)
