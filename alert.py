import os
import sys


src_path = "/Users/shuqiyang/Desktop/TrainYourOwnYOLO/2_Training/src"
utils_path = "/Users/shuqiyang/Desktop/TrainYourOwnYOLO/Utils"

print(src_path,utils_path)

sys.path.append(src_path)
sys.path.append(utils_path)


from keras_yolo3.yolo import YOLO, detect_video


model_path="/Users/shuqiyang/Desktop/TrainYourOwnYOLO/Data/Model_Weights/trained_weights_final.h5"
anchors_path="/Users/shuqiyang/Desktop/TrainYourOwnYOLO/2_Training/src/keras_yolo3/model_data/yolo_anchors.txt"
classes_path="/Users/shuqiyang/Desktop/TrainYourOwnYOLO/Data/Model_Weights/data_classes.txt"
yolo = YOLO(
        **{
            "model_path": model_path,
            "anchors_path": anchors_path,
            "classes_path":classes_path,
            "score":0.3,
            "model_image_size": (416, 416),
        }
    )

model=yolo.yolo_model

from PIL import Image
from timeit import default_timer as timer
from utils import load_extractor_model, load_features, parse_input, detect_object
import test
import utils
import pandas as pd
import numpy as np
from Get_File_Paths import GetFileList
import random
from Train_Utils import get_anchors
from selenium import webdriver
import pyautogui
import time
import shutil,os
import bs4
from tqdm import *

x=1
while x<300:
    out_df=pd.DataFrame()
    image=pyautogui.screenshot(region=(500,500,800,450))
    image.save('/Users/shuqiyang/Desktop/scrapedata/pic/'+time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))+'.png')
    img_path=('/Users/shuqiyang/Desktop/scrapedata/pic/'+time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))+'.png')
    prediction, image = detect_object(
            yolo,
            img_path,
            save_img=time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))+'test.png',
            save_img_path='/Users/shuqiyang/Desktop/TrainYourOwnYOLO/Data/Source_Images/Test_Images/',
            postfix="monkeys",
            )
    y_size, x_size, _ = np.array(image).shape
    for single_prediction in prediction:
        out_df = out_df.append(
            pd.DataFrame(
                [
                    [
                        os.path.basename(img_path.rstrip("\n")),
                        img_path.rstrip("\n"),
                    ]
                    + single_prediction
                    + [x_size, y_size]
                ],
                columns=[
                    "image",
                    "image_path",
                    "xmin",
                    "ymin",
                    "xmax",
                    "ymax",
                    "label",
                    "confidence",
                    "x_size",
                    "y_size",
                ],
            )
        )
    for i in tqdm(range(60)):
        time.sleep(0.1)
    time.sleep(60)
out_df.to_csv("/Users/shuqiyang/Desktop/scrapedata/result.csv")
count=pd.to_csv("/Users/shuqiyang/Desktop/scrapedata/result.csv",index=False)
print(count)




