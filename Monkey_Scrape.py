#!/usr/bin/env python
# coding: utf-8

# In[81]:

import time
import requests
import datetime
import pytz
from urllib.request import urlretrieve


# In[84]:


IMAGE_URL = "https://jigokudani-yaenkoen.co.jp/livecam/monkey/image.jpg"
 
def urllib_download():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Tokyo"))
    dt_string = pst_now.strftime('%Y-%m-%d-%H-%M-%S') 
    urlretrieve(IMAGE_URL, 'webcam/'+dt_string+'.png')
    
x=1
while x<72:
    urllib_download()
    time.sleep(60*10)
    x+=1


# In[ ]:




