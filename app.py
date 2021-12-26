import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from PIL import Image
# from multiapp import MultiApp
from apps import app1, app2, app3

im = Image.open("image_10.jpg")
st.set_page_config(
    page_title="Missing Customers & Invoices",
    page_icon=im,
#     layout="wide",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

users = pd.read_csv('users.csv')
names = users['name'].to_list()
usernames = users['username'].to_list()
hashed_passwords = users['hashed_password'].to_list()

authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                    'missingCustomersAndInvoices', 'p3jCB8sPxF',
                                    cookie_expiry_days=1)

name, authentication_status = authenticator.login('Login','sidebar')

if authentication_status:
#     app = MultiApp()

#     app.add_app("App 1", app1.function)
#     app.add_app("App 2", app2.function)

#     app.run_app()
    if st.session_state['authentication_status']:
        st.sidebar.write('Welcome, *%s!*' % (st.session_state['name']))
        if st.session_state['name'] == 'Test':
            app3.app()
        if st.session_state['name'] == 'Alexey':
            app2.app()
    elif st.session_state['authentication_status'] == False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] == None:
        st.warning('Please enter your username and password')

elif authentication_status == False:
    st.error('Username/Password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your Username and Password')
