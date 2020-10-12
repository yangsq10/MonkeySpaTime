import streamlit as st
import numpy as np
import pandas as pd
import time
import os
import requests
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime
import pytz
import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1000px;
        padding-top: 3.5rem;
        padding-right: 2.0rem;
        padding-left: 2.0rem;
        padding-bottom: 2.0rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

set_png_as_page_bg('monkey2.jpg')


current_monkey=pd.read_csv("result.csv")
print(current_monkey)
count=current_monkey[-1:]
img=count["image"].to_string(index=False).strip()
num=current_monkey[current_monkey['image']==img]['image'].count()
date=img[5:10]
timee=img[11:16]
utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone("Asia/Tokyo"))
time_m10=(utc_now.astimezone(pytz.timezone("Asia/Tokyo")) + datetime.timedelta(minutes=10)).strftime("%H-%M")
time_l10=(utc_now.astimezone(pytz.timezone("Asia/Tokyo")) + datetime.timedelta(minutes=-10)).strftime("%H-%M")
output=('Last update: On '+ date + ', at ' + timee + ': there are ' + str(num) + ' monkeys')

st.markdown('''
    <span style="text-align: center; color:white;font-weight:bold;font-size: 40px;font-weight:bold;margin-left: auto">
        Monkey Spa Time <br />
    </span>
    ''',
unsafe_allow_html=True)

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone("Asia/Tokyo"))
hour = pst_now.strftime('%H')
day=utc_now.astimezone(pytz.timezone("US/Eastern")).strftime('%D')
hour=int(hour)
if hour>17 or hour<9:
    st.markdown(
    '''
    <span style="color: black; font-weight: bold; font-size:32px">
        The park is currently closed. Please check back at 9 am to 4 pm in Tokyo Time (20 pm to 3 am in New York Time).
    </span>
    ''',
    unsafe_allow_html=True
)
    st.header('Last update: on '+ day + ' at 15:50 pm in Tokyo Time')
else:
    if datetime.datetime.strptime(time_l10,'%H-%M')<datetime.datetime.strptime(timee,'%H-%M')<datetime.datetime.strptime(time_m10,'%H-%M'):
        st.header(output)
    else:
        st.header("At"+ cur + "there are no monkeys")
    

st.markdown(
    '''
    <span style="color:white;font-size: 24px">
        Snow monkeys like to soak in the hotspring. The snowmonkey park kindly provide the live camera at the link: https://en.jigokudani-yaenkoen.co.jp/livecam2/video_en.php to capture those monkey's funny moments. However, monkeys are not always around the camera, a lot of times they are in other places. We monitor the monkey park camera and push notifications when there is a significant amount of monkeys. If you want to receive notifications to check monkeys out, please subscribe below!<br />
    </span>
    ''',
    unsafe_allow_html=True
)

st.markdown(
    '''
    <span style="color:white; font-size:30px; font-weight: bold">
        Your email address: <br />
    </span>
    ''',
    unsafe_allow_html=True
)
@st.cache(allow_output_mutation=True)
def get_data():
    return []
user_emailaddress=st.text_input(" ")
input=st.button("Subscribe")
if input and user_emailaddress:
    st.write("Successfully subscribe!")
    get_data().append({"UserID": user_emailaddress})
    email=pd.DataFrame(get_data())
    email.to_csv('email.csv')
    
st.sidebar.title("Check previous days:")
count=pd.read_csv("result.csv")
time = st.sidebar.selectbox('', ['Yesterday', 'Last Week', 'Last Month', 'Last Year'], key='1')
if not st.sidebar.checkbox("Hide", True, key='1'):
    if time == 'Yesterday':
        st.markdown(
        '''
        <span style="color:white; font-weight: bold; font-size:34px">
            Yesterday: <br />
        </span>
        ''',
        unsafe_allow_html=True
        )
        yesterday=count[count['Date']==lastday]
        set2 = { 'x': yesterday.Time, 'y': yesterday.monkey, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'Moving average of 12 periods'}
        data2 = [set2]
        fig2 = go.Figure(data=data2)
        fig2.update_layout(
        autosize=False,
        width=900,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        )
        st.plotly_chart(fig2)
    if time == 'Last Week':
        st.markdown(
        '''
        <span style="color:white; font-weight: bold; font-size:34px">
            Last Week: <br />
        </span>
        ''',
        unsafe_allow_html=True
        )
        count['DateTime']=count['Time']+' '+ count['Date']
        set3 = { 'x': count.DateTime, 'y': count.monkey, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'Moving average of 12 periods'}
        data3 = [set3]
        fig3 = go.Figure(data=data3)
        fig3.update_layout(
        autosize=False,
        width=900,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        )
        st.plotly_chart(fig3)
    if time == 'Last Month':
        st.markdown(
        '''
        <span style="color:white; font-weight: bold; font-size:34px">
            Not Enough Data now <br />
        </span>
        ''',
        unsafe_allow_html=True
        )
    if time == 'Last Year':
        st.markdown(
        '''
        <span style="color:white; font-weight: bold; font-size:34px">
            Not Enough Data now <br />
        </span>
        ''',
        unsafe_allow_html=True
        )
