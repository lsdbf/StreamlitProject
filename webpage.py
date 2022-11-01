from fileinput import close
from re import S
import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
from PIL import Image

st.set_page_config(page_title="Weather Canaliser", layout="wide")

#Added UI widget function to show weather. Can delete just an idea - Chris
def showTemperatureUI(name, temperature, wind, humidty):
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Location", name)
        col2.metric("Temperature", temperature)
        col3.metric("Wind", wind)
        col4.metric("Humidity", humidty)

#text input requirement --ethan
def handleLocation(zipcode):
    if(zipcode):
        api_key = "cd101785cf9a9ea832093a5827bdc77c"
        url = "https://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + ",us&appid=" + api_key + "&units=imperial"
        header = {'content-type': 'application/json',
        'x-access-token': api_key}
        response = requests.get(url).json()
        name = response["name"]
        temperature = response["main"]["temp"]
        wind = response["wind"]["speed"]
        humidty = response["main"]["humidity"]
        with st.container():
            showTemperatureUI(name, temperature, wind, humidty)
        st.write(response)
        st.success("Successful 🍨") #and success output

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

#Added a sidebar - Chris
add_selectbox = st.sidebar.selectbox(
    "Choose an option",
    ["Homepage", "5-Day Forecast", "Compare Cities"]
)

#Line graph to show weather for 5 day period - Chris
if add_selectbox == "5-Day Forecast":
    st.write("To be constructed")

#Bar chart to let user compare weather for multiple cities - Chris
elif add_selectbox == "Compare Cities":
    st.write("To be constructed")

else:
    col1, col2 = st.columns(2)
    with col1:
        st.title("The Weather Canaliser 😎")
        ##image title
        image = Image.open('title.png')

    with col2:
        st.write("want to change the picture of the title?")
        pictures = st.radio("Choose one of the following",
                            ('default', 'birb', 'dawg', 'reeeee'))

        if pictures == 'default':
            image = Image.open('title.png')
        if pictures == 'birb':
            image = Image.open('media/birb.jpg')
        if pictures == 'dawg':
            image = Image.open('media/dog.jpg')
        if pictures == 'reeeee':
            image = Image.open('media/cat.gif')

    st.image(image, caption="amazing isn't it?", output_format='PNG')

    st.caption("sit back, relax, don't worry about it")
    audio_file = open('media/CosmicDance.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    st.write("What's your zip code? Let's check the weather")
    zip = st.text_input("Zip Code")
    handleLocation(zip)
##st.write("What's your zip code? Let's check the weather")
##zip = st.text_input("Zip Code")
##handleLocation(zip)

    col1, col2 = st.columns(2)

    with st.container():
        try:
            st.title("Enter Your City")
            cityname = st.text_input("city")

            if cityname:
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
        except TypeError:
            st.error('Please type correct city name', icon="🚨")








