from fileinput import close
from re import S
import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
from PIL import Image

st.set_page_config(page_title="Weather Canaliser")
col1, col2 = st.columns(2)
with col1:
    st.title("The Weather Canaliser 😎")
    ##image title
    image = Image.open('title.png')

with col2:
    st.write("want to change the picture of the title?")
    pictures = st.radio("Choose one of the following",
    ('default','birb','dawg','reeeee'))

    if pictures == 'default':
        image = Image.open('title.png')
    if pictures == 'birb':
        image = Image.open('birb.jpg')
    if pictures == 'dawg':
        image = Image.open('dog.jpg')
    if pictures == 'reeeee':
        image = Image.open('cat.gif')

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
def handleLocation(zipcode):
    if(zipcode):
        api_key = "cd101785cf9a9ea832093a5827bdc77c"
        url = "https://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + ",us&appid=" + api_key
        header = {'content-type': 'application/json',
        'x-access-token': api_key}
        response = requests.get(url).json()
        st.write(response)
        st.success("Successful 🍨") #and success output

##st.write("What's your zip code? Let's check the weather")
##zip = st.text_input("Zip Code")
##handleLocation(zip)


def storeData(city_name):
    api_key = "cd101785cf9a9ea832093a5827bdc77c"
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=" + api_key
    response = requests.get(url)
    if response:
        json = response.json()
        temperature = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humidity = json ['main']['humidity']
        city = json['name']
        long = json['coord']['lon']
        lat = json['coord']['lat']

        result = [temperature,temp_feels,humidity,city,long,lat]
        
        return result, json
    #else:
    #    st.error("woah there buddy 🚨, invalid result")

col1, col2 = st.columns(2)

with st.container():
    st.title("Enter Your City")
    cityname = st.text_input("city")
    res, json = storeData(cityname)
    df = pd.DataFrame(
    {
        "lat" : [res[5]],
        "lon" : [res[4]],
    },
    columns = ["lat","lon"]
    )
    st.map(df)
    st.success("Map successfully displayed")
    values = pd.DataFrame(
            {
                "temp" : [res[0]],
                "temp_feels" : [res[1]],
                "humidity" : [res[2]],
                "name" : [res[3]]
            },
            columns= ["temp","temp_feels","humidity","name"]
        )
    st.checkbox("wide length table", value=False, key="use_container_width") #check box requirement
    st.dataframe(values, use_container_width = st.session_state.use_container_width)   

#1 interactive table //Ethan -------
with st.container():
    st.write("testing interactive table")
    df = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('column %d' % i for i in range(20)))
    st.dataframe(df)   

#2 2 chart Elements //Ethan -------

with st.container():
    st.write("test line graph")
    st.line_chart(df)

with st.container():
    st.write("test area graph")
    st.area_chart(df)

#3 1 Map //Ethan ------

# Add a selectbox to the sidebar:


