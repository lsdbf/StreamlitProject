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
    st.title("The Weather Canaliser 😎")
    ##image title
    image = Image.open('title.png')
    st.image(image, caption="amazing isn't it?", output_format='PNG')
    #not required, I just liked the song --Ethan
    # Cosmic Dance by Joseph Patrick Moore
    st.caption("sit back, relax, don't worry about it")
    audio_file = open('media/CosmicDance.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')
    st.write("What's your zip code? Let's check the weather")
    zip = st.text_input("Zip Code")
    handleLocation(zip)

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


