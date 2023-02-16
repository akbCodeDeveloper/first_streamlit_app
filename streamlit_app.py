import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

streamlit.header('My Breakfast Menu')
streamlit.text('\N{bowl with spoon} Omega 3 & Blueberry Meal' ) 
streamlit.text('\N{green salad} Kale , Spinach & Rocket Smoothie')
streamlit.text('\N{chicken} Hard-Boiled Free-Range Egg')
streamlit.text('\N{avocado} \N{bread} Avocado Toast')

streamlit.text('\N{banana} \N{strawberry} Build your own fruit smoothie \N{peach} \N{grapes} ')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'] )
fruits_to_show= my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)
# New section of display fruitvice api response
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
# New section of code to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select the fruit to get the information.")
    else:
        back_from_function = get_fruitvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
     streamlit.error()
    


# import snowflake.connector

streamlit.header("The fruit load list containts:")
# Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select fruit_name from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
    
# Add a Button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

    
#streamlit.stop()
streamlit.header("Fruityvice Fruit Advice!")
# Allow end user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ( '"+ new_fruit +"' ) ")
        return "Thanks for adding "+new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like add ?')
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_button = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_button)
    


