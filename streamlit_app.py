# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

name_on_order = st.text_input('Name on Smoothie')
st.write('The Name on your Smoothie will be', name_on_order)
#SiS to SniS
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)    #for demonstration only
#st.stop()                                                    #for demonstration only       
    
ingredients_list = st.multiselect(          #Variable: ingredients _list -> wird als Liste ausgegeben
'Choose up to 5 ingredients:'
, my_dataframe
, max_selections=6
)

#IF: Es muss etwas ausgewaehlt sein
if ingredients_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
#Storing orders in snowflake
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""

    #check SQL output
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order') #submit button to prevent doublings

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered',icon="✅")
        
