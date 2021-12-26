import streamlit as st
from multiapp import MultiApp
from apps import app1, app2


app = MultiApp()

app.add_app("App 1", app1.function)
app.add_app("App2", app2.function)

app.run_app()
