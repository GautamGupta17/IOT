import streamlit as st

#### app

header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()
model_training = st.beta_container()

with header:
    st.title('Welcome to my IOT PROJECT')
    st.text('Here we will see how good is our cooked dal sample')
with dataset:
    st.header('Dal Dataset I created')

with features:
    st.header('The features I created')

with model_training:
    st.header('Time to train the model')
