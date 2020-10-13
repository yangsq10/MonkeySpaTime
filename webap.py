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
cur=pst_now.strftime('%M')
cur=int(cur)//10
cur=cur*10
cur=str(cur)
hor=str(hour)
day=utc_now.astimezone(pytz.timezone("US/Eastern")).strftime('%D')
hour=int(hour)
if hour>17 or hour<9:
    st.markdown(
    '''
    <span style="color: black; font-weight: bold; font-size:32px">
        The park is currently closed. Please check back at 9 am to 4 pm in Tokyo Time (5pm to 12 am San Francisco Time).
    </span>
    ''',
    unsafe_allow_html=True
)
    st.header('Last update: on '+ day + ' at 15:50 pm in Tokyo Time')
else:
    if datetime.datetime.strptime(time_l10,'%H-%M')<datetime.datetime.strptime(timee,'%H-%M')<datetime.datetime.strptime(time_m10,'%H-%M'):
        st.header(output)
    else:
        st.header("At "+ hor + ':' + cur + ", there are no monkeys")
    

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
    email.to_csv('/home/ubuntu/MonkeyTime/email.csv')
    
st.sidebar.title("Check previous days:")

import requests
import pandas as pd
from datetime import datetime
import sqlite3
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import time
import sqlite3
import numpy as np
import math

data=pd.read_csv('result.csv')
conn=sqlite3.connect('monkey.db')
table_name='monkey'
data.to_sql(table_name,conn,if_exists='replace')

data2=pd.read_sql_query('''SELECT substr(image,6,5) as Date, 
ROUND(Sum(CASE WHEN substr(image,12,2)='09' THEN 1 ELSE 0 end)/6,2) as '09 AM',
ROUND(Sum(CASE WHEN substr(image,12,2)='10' THEN 1 ELSE 0 end)/6,2) as '10 AM',
ROUND(Sum(CASE WHEN substr(image,12,2)='11' THEN 1 ELSE 0 end)/6,2) as '11 AM',
ROUND(Sum(CASE WHEN substr(image,12,2)='12' THEN 1 ELSE 0 end)/6,2) as '12 PM',
ROUND(Sum(CASE WHEN substr(image,12,2)='13' THEN 1 ELSE 0 end)/6,2) as '13 PM',
ROUND(Sum(CASE WHEN substr(image,12,2)='14' THEN 1 ELSE 0 end)/6,2) as '14 PM',
ROUND(Sum(CASE WHEN substr(image,12,2)='15' THEN 1 ELSE 0 end)/6,2) as '15 PM',
ROUND(Sum(CASE WHEN substr(image,12,2)='16' THEN 1 ELSE 0 end)/6,2) as '16 PM'
from monkey
where Date in (select distinct substr(image,6,5) as Date from monkey 
order by image desc limit 1)'''.format(table_name),conn)
last_day=data2['Date']
last_day=pd.DataFrame(last_day)['Date'].tolist()
last_day=' '.join([str(elem) for elem in last_day]) 


data3=np.transpose(data2).reset_index()
data3=data3.rename(columns={'index':'hour',0:'num'})[1:]


data4=pd.read_sql_query('''SELECT 
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Mon 09',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Mon 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Mon 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Mon 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Mon 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Mon 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 1') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Mon 15',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Tue 9',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Tue 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Tue 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Tue 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Tue 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Tue 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 2') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Tue 15',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Wed 9',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Wed 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Wed 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Wed 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Wed 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Wed 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 3') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Wed 15',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Thur 9',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Thur 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Thur 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Thur 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Thur 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Thur 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 4') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Thur 15',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Fri 9',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Fri 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Fri 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Fri 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Fri 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Fri 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 5') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Fri 15',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Sat 9',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Sat 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Sat 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Sat 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Sat 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Sat 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 6') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Sat 15',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='09' Then 1 else 0 end)/7 as 'Sun 9',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='10' Then 1 else 0 end)/7 as 'Sun 10',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='11' Then 1 else 0 end)/7 as 'Sun 11',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='12' Then 1 else 0 end)/7 as 'Sun 12',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='13' Then 1 else 0 end)/7 as 'Sun 13',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='14' Then 1 else 0 end)/7 as 'Sun 14',
SUM(CASE WHEN substr(image,1,10)=DATE('now','start of day','-8 day','weekday 0') AND substr(image,12,2)='15' Then 1 else 0 end)/7 as 'Sun 15'
from monkey'''.format(table_name),conn)
data4=np.transpose(data4).reset_index()
data4=data4.rename(columns={'index':'hour',0:'num'})

data5=pd.read_sql_query('''SELECT DATE('now','start of day','-8 day','weekday 1') as start_date,
DATE('now','start of day','-8 day','weekday 0') as end_date from monkey LIMIT 1'''.format(table_name),conn)
start_date=data5['start_date'].tolist()
end_date=data5['end_date'].tolist()
start_date=' '.join([str(elem) for elem in start_date]) 
end_date=' '.join([str(elem) for elem in end_date])


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
        set2 = { 'x': data3.hour, 'y': data3.num, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'Moving average of 12 periods'}
        da2 = [set2]
        fig2 = go.Figure(data=da2)
        fig2.update_layout(
        title=("On 2020-" + last_day + " :average amount of monkeys at each hour"),
        xaxis_title="Hour",
        yaxis_title="Average amount of monkeys",
        font=dict(
        size=14,
        ),
        autosize=False,
        width=936,
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

        set3 = { 'x': data4.hour, 'y': data4.num, 'type': 'scatter', 'mode': 'lines', 'line': { 'width': 1, 'color': 'blue' },'name': 'Moving average of 12 periods'}
        da3 = [set3]
        fig3 = go.Figure(data=da3)
        fig3.update_layout(
        title=("From " + start_date + " to " + end_date + ":average amount of monkeys at each day"),
        xaxis_title="Hour",
        yaxis_title="Average amount of monkeys",
        font=dict(
        size=14,
        ),
        autosize=False,
        width=935,
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
