import streamlit as st
st.title("Snow monkey checker")
st.write("Subscribe")
user_input=st.text_input("Your email address")
input=st.button("Subscribe")
if input and user_input:
    st.write("Successfully subscribe!")

