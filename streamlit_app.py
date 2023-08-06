import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
st.title('My parents New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avacado Tost')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple','Strawberries'])
fruit_to_show = my_fruit_list.loc[fruit_selected]
st.dataframe(fruit_to_show)

# new section to see Fruityvice response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('please select a fruit to get information.')
  else:  
    st.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    st.dataframe(fruityvice_normalized)
except URLErorr as e:
    st.error()
  
st.stop()
#adding code to fetch data from snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
st.header("The Fruit load List Contains: ")
st.dataframe(my_data_rows)
add_my_fruit = st.text_input('What fruit would you like to add?','jackfruit')
st.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")


