import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import pickle
import requests
import time
import json

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, train_test_split

def timetaken(quality):
        if (quality>=9.15):
            time = (quality - 9.15 ) / 0.003979646611374403
            return("Food is fresh. Consume it under ", round(time) , " mins")
        if (quality>=8.7 and quality < 9.15):
            time = (quality - 8.7 ) / 0.001877660059602652
            return("Food is cold and needs to be reheated. Heat and eat before", round(time) ," mins")
        if (quality>=7.8 and quality < 8.7) :
            time = (quality - 7.8 ) /  0.0024480416168478265
            return("Time left to spoil=" , round(time) ," mins. Store in the refrigerator before", round(time) ,"mins")
        elif (quality< 7.8):
            return("Food is spoiled, discard it.")

url1 = "https://api.thingspeak.com/channels/1785779/feeds/last.json?api_key=64LX24ENHBDW3JZV"
url2 = "https://api.thingspeak.com/channels/1780792/feeds/last.json?api_key=6PKCOVRLO9U2HFJ7"
url3 = "https://api.thingspeak.com/channels/1744711/feeds/last.json?api_key=LQYCBT76OZKU05HV"
url4 = "https://api.thingspeak.com/channels/1744701/feeds/last.json?api_key=2HY016JWRK0O7IFI"

while True:
    response1 = requests.get(url1)
    data_disc1 = json.loads(response1.text)
    input1 =  data_disc1['field1']

    response2 = requests.get(url2)
    data_disc2 = json.loads(response2.text)
    input2 =  data_disc2['field1']

    response3 = requests.get(url3)
    data_disc3 = json.loads(response3.text)
    input3 = data_disc3['field1']

    response4 = requests.get(url4)
    data_disc4 = json.loads(response4.text)
    input4 = data_disc4['field1']

    
    loaded_model = pickle.load(open('C:/Users/naren/Downloads/IOT_DAL/Streamlit app/trained_model.sav', 'rb'))

    input_data = (input1 ,input2 ,input3, input4)
    input_data = list(np.float_(input_data))
    print(input_data)
    
    input_data_as_numpy = np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy.reshape(1,-1)

    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    q = prediction[0]
    k = timetaken(q) 
    print(k)

    time.sleep(30)



























