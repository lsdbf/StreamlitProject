from fileinput import close
from re import S
import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
from PIL import Image

st.set_page_config(page_title="Weather Canaliser", layout="wide")
st.title("The Weather Canaliser 😎")
##image title
image = Image.open('title.png')

st.image(image, caption="amazing isn't it?",output_format='PNG')

#not required, I just liked the song --Ethan
# Cosmic Dance by Joseph Patrick Moore
st.caption("sit back, relax, don't worry about it")
audio_file = open('CosmicDance.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')
#------------------------------------------------------

#------------------------------------------------------
#text input requirement --ethan
#modified output - displaying icon for better user visualization --mariela
def handleLocation(city):
    if(city):
        api_key = "cd101785cf9a9ea832093a5827bdc77c"
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + ",us&appid=" + api_key
        header = {'content-type': 'application/json',
        'x-access-token': api_key}
        response = requests.get(url).json()
        #st.json(response)
        #st.success("Successful 🍨") #and success output
        general = response['weather'][0]['main']
        icon_id = response['weather'][0]['icon']
        icon = f'http://openweathermap.org/img/wn/{icon_id}@2x.png'
        st.write(general)
        st.image(icon)


st.write("What's your city? Let's check the weather")
city = st.text_input("City")
handleLocation(city)


#1 1 interactive table //Ethan -------
with st.container():
    st.write("testing interactive table")
    df = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('column %d' % i for i in range(20)))

    st.dataframe(df) # same as st.write(df)    

#2 2 chart Elements //Ethan -------

with st.container():
    st.write("test line graph")
    st.line_chart(df)

with st.container():
    st.write("test area graph")
    st.area_chart(df)

#3 1 Map //Ethan ------
with st.container():
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.map(df)

# Add a selectbox to the sidebar:




