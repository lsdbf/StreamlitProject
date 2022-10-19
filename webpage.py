import streamlit as st
import numpy as np
import pandas as pd
import requests

st.title("The Weather Canaliser 😎")

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
