import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time
import os
st.title("Snow monkey checker")
st.write("Subscribe")
user_input=st.text_input("Your email address")
input=st.button("Subscribe")
if input and user_input:
    st.write("Successfully subscribe!")

