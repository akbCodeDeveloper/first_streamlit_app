import streamlit
import pandas

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
# New section of code to display fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")

# Take the Json version response and normalize it 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output in the screen as a table.
streamlit.dataframe(fruityvice_normalized)
