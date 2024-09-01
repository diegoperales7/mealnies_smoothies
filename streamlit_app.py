# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want your custom Smoothie!
    """
)

name_on_order=st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list=[]
ingredients_list = st.multiselect('Choose up to 5 ingredients: ', my_dataframe, max_selections=5)
# if len(ingredients_list) == 5:
#     st.warning("You've reached the maximum number of selections (5).")
# elif len(ingredients_list) > 5:
#     st.error("You can't select more than 5 ingredients. Please remove one to add another.")
# if len(ingredients_list)<5:
#     ingredients_list=st.multiselect('Choose up to 5 ingredients: ', my_dataframe,default=ingredients_list)
#st.dataframe(data=my_dataframe, use_container_width=True)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
    st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
   
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
    st.stop()

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
