# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)
if ingredient_list:
    ingredients_string = " ".join(ingredient_list)
    
    st.write (ingredients_string)
    
    my_insert_stmt = "INSERT INTO smoothies.public.orders (Name_on_order, ingredients) VALUES ('" + name_on_order + "', '" + ingredients_string + "')"
    
    time_to_insert = st.button ("Submit Order")
    
    #st.write (my_insert_stm)
    if  time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
