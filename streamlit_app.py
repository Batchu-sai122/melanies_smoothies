# Import python packages
import streamlit as st
import pandas as pd

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

# Add description text
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

#import streamlit as st

name_on_order= st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be", name_on_order)

# Dropdown (selectbox) for favorite fruit


cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()


pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

import requests
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    """
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    """
    
    ingredients_string = ''
    
    import requests
import json

for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

    st.subheader(f"{fruit_chosen} Nutrition Information")

    try:
        url = f"https://fruityvice.com/api/fruit/{search_on.lower()}"
        response = requests.get(url, timeout=5)

        # Check if the response is valid JSON
        if response.status_code == 200:
            try:
                data = response.json()
                st.dataframe(data, use_container_width=True)
            except json.JSONDecodeError:
                st.warning(f"⚠️ Could not decode JSON for {fruit_chosen}. API returned invalid data.")
        else:
            st.warning(f"⚠️ Fruityvice API returned status code {response.status_code} for {fruit_chosen}.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while fetching data for {fruit_chosen}: {e}")
        st.info("Using fallback sample data instead.")
        fallback_data = {"fruit": fruit_chosen, "calories": 50, "sugar": 10, "fiber": 2}
        st.dataframe(fallback_data, use_container_width=True)

        

        
        
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        #st.text(smoothiefroot_response.json())
        #sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    #st.write(ingredients_string)

    my_insert_stmt = """
    insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','""" + name_on_order + """')
    """

    # Uncomment this to debug SQL before execution
    #st.write(my_insert_stmt)


    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    

