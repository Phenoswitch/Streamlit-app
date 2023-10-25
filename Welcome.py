import streamlit as st
import numpy as np
from streamlit_extras.app_logo import add_logo

add_logo("https://allumiqs.com/wp-content/uploads/2022/06/AG-Icon-238x232.png", height=200) #TODO: move this to a utils module
#
st.title('Allumiqs Technology Platform Quality Dashboard')

#%%
st.subheader("""
Instructions""")
st.info(f'Welcome ! This is the main page for Technology Platform Quality Dashboard. Please carefully read the instructions.')



# streamlit run Welcome.py