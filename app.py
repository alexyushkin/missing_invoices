import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from multiapp import MultiApp
from apps import app1, app2

users = pd.read_csv('users.csv')
names = users['name'].to_list()
usernames = users['username'].to_list()
hashed_passwords = users['hashed_password'].to_list()

authenticator = stauth.authenticate(names, usernames, hashed_passwords,
                                    'missingCustomersAndInvoices', 'p3jCB8sPxF',
                                    cookie_expiry_days=1)

name, authentication_status = authenticator.login('Login','sidebar')

if authentication_status:
    app = MultiApp()

    app.add_app("App 1", app1.function)
    app.add_app("App 2", app2.function)

    app.run_app()

elif authentication_status == False:
    st.error('Username/Password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your Username and Password')
