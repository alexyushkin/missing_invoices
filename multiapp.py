import streamlit as st

class MultiApp:
    
    def __init__(self) -> None:
        self.apps = []

    def add_app(self, title, function) -> None:
        self.apps.append(
            {
                'title': title,
                'function': function
            }
        )

    def run_app(self):
        page = st.sidebar.selectbox(
            'Select Application',
            self.apps,
            format_func=lambda page: page['title']
        )
        page['function']()
