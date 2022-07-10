import string
from unittest import result
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
            myvar1 = "Food is fresh. Consume it under"
            myvar2 = round(time)
            myvar3 = " mins"
            s = ("{}{}{}".format(myvar1, myvar2, myvar3))
            #s = (str("Food is fresh. Consume it under") + round(time) + str("mins"))
        if (quality>=8.7 and quality < 9.15):
            time = (quality - 8.7 ) / 0.001877660059602652
            myvar1 = "Food is cold and needs to be reheated. Heat and eat before "
            myvar2 = round(time)
            myvar3 = " mins"
            s = ("{}{}{}".format(myvar1, myvar2, myvar3))
            #s = (str("Food is cold and needs to be reheated. Heat and eat before") + round(time)+ str(" mins"))
        if (quality>=7.8 and quality < 8.7) :
            time = (quality - 7.8 ) /  0.0024480416168478265
            myvar1 = "It needs to be stored in the refrigerator before the given time. Time left to spoil is "
            myvar2 = round(time)
            myvar3 = " mins"
            s = ("{}{}{}".format(myvar1, myvar2, myvar3))
            #s = (str("Time left to spoil is") + round(time) + str("mins. Store in the refrigerator before") + round(time) + str("mins"))
        elif (quality< 7.8):
            s = ("Food is spoiled, discard it.")

        return s

header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()



with header:
    st.title('Welcome to my IOT PROJECT')
    st.text('Here we will see how good is our cooked dal sample')
with dataset:
    st.header('Dal Dataset I created')
    st.text('Created this dataset using arduino')

df = pd.read_csv('TestFinal.csv')


with features:
    st.header('The features I created')

    st.markdown('*Ethanol*')
    st.markdown('*Methane*')
    st.markdown('*Temperature*')
    st.markdown('*Humidity*')


def CheckFood():
    while True:
    
        url1 = "https://api.thingspeak.com/channels/1785779/feeds/last.json?api_key=64LX24ENHBDW3JZV"   #methane
        url2 = "https://api.thingspeak.com/channels/1780792/feeds/last.json?api_key=6PKCOVRLO9U2HFJ7"   #ethanol
        url3 = "https://api.thingspeak.com/channels/1744711/feeds/last.json?api_key=LQYCBT76OZKU05HV"   #humidity
        url4 = "https://api.thingspeak.com/channels/1744701/feeds/last.json?api_key=2HY016JWRK0O7IFI"   #temp


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

        loaded_model = pickle.load(open('trained_model.sav', 'rb'))

        input_data = (input1 ,input2 ,input3, input4)
        input_data = list(np.float_(input_data))                                #methane, ethanol, humidity, temp 
        print(input_data)

        input_data_as_numpy = np.asarray(input_data)

        input_data_reshaped = input_data_as_numpy.reshape(1,-1)

        prediction = loaded_model.predict(input_data_reshaped)
        print(prediction)

        q = prediction[0]
        k = timetaken(q) 
        st.success(k)
        methane = input_data[0]
        ethanol = input_data[1]
        humidity = input_data[2]
        temp = input_data[3]
        var0 = "Methane: "
        var1 = "Ethanol: "
        var2 = "Humidity: "
        var3 = "Temperature: "

        st.text("{}{}".format(var0, methane))

        st.text("{}{}".format(var1, ethanol))
        st.text("{}{}".format(var2, humidity))
        st.text("{}{}".format(var3, temp))
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperature", temp)
        col2.metric("Humidity", humidity)
        col3.metric("Ethanol", ethanol)
        col4.metric("Methane", methane)

        time.sleep(30)
        break

result = st.button("Click here to find current food qualiy")
st.write(result)
if result:
    CheckFood()
    result = False    