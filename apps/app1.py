import streamlit as st


def app():
    st.markdown("## This is App 1 for Test")

    st.write("\n")

    if st.button("Ok", key='1'):
        st.markdown("**You hit Ok button**")
