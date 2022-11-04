from fileinput import close
from re import S

import dateutil.utils
import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
from PIL import Image

# Added UI widget function to show weather. Can delete just an idea - Chris
def showTemperatureUI(name, temperature, temp_feels, wind, humidty):
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Location", name)
        col2.metric("Temperature", temperature)
        col3.metric("Feels like", temp_feels)
        col4.metric("Wind", wind)
        col5.metric("Humidity", humidty)


# API call that gets 5 day forecast and creates chart
def getFiveDayForecast(zipcode, option):
    if (zipcode):
        api_key = "cd101785cf9a9ea832093a5827bdc77c"
        url = "https://api.openweathermap.org/data/2.5/forecast?zip=" + zipcode + ",us&appid=" + api_key + "&units=imperial"
        header = {'content-type': 'application/json',
                  'x-access-token': api_key}
        response = requests.get(url).json()
        array_to_pass = []
        label = None

        days_list = []
        for dt in response["list"]:
            days_list.append(dt["dt_txt"])

        if option == "Temp":
            temp_per_day = []
            for dt in response["list"]:
                temp_per_day.append(dt["main"]["temp"])
                array_to_pass = temp_per_day
                label = "Temperature in Fahrenheit"
        elif option == "Humidity":
            humidity_per_day = []
            for dt in response["list"]:
                humidity_per_day.append(dt["main"]["humidity"])
                array_to_pass = humidity_per_day
                label = "Humidity Percentage"

        elif option == "Wind":
            wind_per_day = []
            for dt in response["list"]:
                wind_per_day.append(dt["wind"]["speed"])
                array_to_pass = wind_per_day
                label = "Wind miles per hour"

        elif option == "Rain":
            rain_per_day = []
            for dt in response["list"]:
                rain_per_day.append(dt["pop"] * 100)
                array_to_pass = rain_per_day
                label = "Probability of precipitation"

        st.write("5-Day Forecast")
        data = pd.DataFrame({
            'index': days_list,
            label: array_to_pass,
        }).set_index('index')

        st.info('This information is from OpenWeatherMap.org', icon="ℹ️")
        st.line_chart(data)



# text input requirement --ethan
def handleLocation(zipcode):
    if (zipcode):
        api_key = "cd101785cf9a9ea832093a5827bdc77c"
        url = "https://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + ",us&appid=" + api_key + "&units=imperial"
        header = {'content-type': 'application/json',
                  'x-access-token': api_key}
        response = requests.get(url).json()
        name = response["name"]
        temperature = response["main"]["temp"]
        wind = response["wind"]["speed"]
        humidty = response["main"]["humidity"]

        st.success("Successful 🍨")  # and success output


def storeData(city_name):
    api_key = "cd101785cf9a9ea832093a5827bdc77c"
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=" + api_key + "&units=imperial"
    response = requests.get(url)
    if response:
        json = response.json()
        temperature = json['main']['temp']
        temp_feels = json['main']['feels_like']
        humidity = json['main']['humidity']
        wind = json['wind']['speed']
        city = json['name']
        long = json['coord']['lon']
        lat = json['coord']['lat']

        result = [temperature, temp_feels, humidity, city, long, lat, wind]

        return result, json


# Added a sidebar - Chris
add_selectbox = st.sidebar.selectbox(
    "Choose an option",
    ["Homepage", "5-Day Forecast", "Compare Cities Weather"]
)

# Line graph to show weather for 5 day period - Chris
if add_selectbox == "5-Day Forecast":
    weather = st.select_slider(
        'Select your favorite type of weather',
        options=['sunny', 'overcast', 'rainy', 'thunder', 'snow'])

    icon = ' '
    if weather == 'sunny':
        icon = '☀️'
    elif weather == 'overcast':
        icon = '🌥'
    elif weather == 'rainy':
        icon = '🌧'
    elif weather == 'thunder':
        icon = '🌩'
    elif weather == 'snow':
        icon = '🌨'
    st.title(icon)

    with st.container():
        st.write("Pick your city to check the weather for the next 5 days.")
        zip = st.text_input("Zip Code")
        option = st.selectbox(
            'What would you like to see the 5-day forecast for?',
            ('Temp', 'Humidity', 'Wind', 'Rain'))
        getFiveDayForecast(zip, option)


# Bar chart to let user compare weather for multiple cities - Chris
elif add_selectbox == "Compare Cities Weather":
    options = st.multiselect(
        'Compare the Temperature in Major Cities',
        ['New York', 'Miami', 'Chicago', 'Dallas', "Boston", "Los Angeles"],
    )
    columns = []
    temp_array = []

    for x in options:
        columns.append(x)
        res, json = storeData(x)
        showTemperatureUI(res[3], res[0], res[1], res[5], res[2])
        temp_array.append(res[0])


    data = pd.DataFrame({
        'index': columns,
        'Temperature in Fahrenheit': temp_array,
    }).set_index('index')

    st.bar_chart(data)

else:
    col1, col2 = st.columns(2)
    with col1:
        st.title("The Weather Canaliser 😎")
        ##image title
        image = Image.open('title.png')
        if st.button('Click Here To Learn About the App'):
            st.write('This Weather App allows you to check the weather!')
        else:
            st.write('HELLLLLLOOOOOO')

    with col2:
        st.write("Want to change the picture of the title?")
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

    col1, col2 = st.columns(2)

    with st.container():
        try:
            st.title("Enter Your City")
            cityname = st.text_input("city")

            if cityname:
                res, json = storeData(cityname)
                showTemperatureUI(res[3], res[0], res[1], res[5], res[2])
                df = pd.DataFrame(
                    {
                        "lat": [res[5]],
                        "lon": [res[4]],
                    },
                    columns=["lat", "lon"]
                )
                st.map(df)
                st.success("Map successfully displayed")
                values = pd.DataFrame(
                    {
                        "temp": [res[0]],
                        "temp_feels": [res[1]],
                        "humidity": [res[2]],
                        "name": [res[3]]
                    },
                    columns=["temp", "temp_feels", "humidity", "name"]
                )
                st.checkbox("wide length table", value=False, key="use_container_width")  # check box requirement
                st.dataframe(values, use_container_width=st.session_state.use_container_width)
        except TypeError:
            st.error('Please type correct city name', icon="🚨")
