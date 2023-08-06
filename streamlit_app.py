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

#adding function here
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# new section to see Fruityvice response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error('please select a fruit to get information.')
  else:  
    st.write('The user entered ', fruit_choice)
    back_from_function = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_function)
except URLErorr as e:
    st.error()
  
#adding code to fetch data from snowflake
st.header("The Fruit load List Contains: ")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
  return my_cur.fetchall()
#Adding a Button to the fruit
if st.button('get fruit load list'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)
#st.stop()  
def insert_row_snowflake(new_fruit):
  with mycnx.cursor() as my_cur:
    my_cur.execute("insert into FRUIT_LOAD_LIST values (add_my_fruit)")
    return "Thanks for adding "+new_fruit
    
add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_snowflake (add_my_fruit)
st.text(back_from_function)


