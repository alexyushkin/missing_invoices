import streamlit as st


def app():
    st.markdown("## This is App 2 for Someone")

    st.write("\n")

    if st.button("Ok", key='2'):
        st.markdown("**You hit Ok button**")
