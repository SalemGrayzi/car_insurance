
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import altair as alt

df =pd.read_csv("C:/Users/salem/Desktop/AUB/Courses/spring/msba_325_visualization/week2//h.w1/car_insurance.csv")

st.title('Car Insurance')

@st.cache
def load_data(nrows):
    data =pd.read_csv("C:/Users/salem/Desktop/AUB/Courses/spring/msba_325_visualization/week2//h.w1/car_insurance.csv")
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

if st.checkbox('Show Avg Credit'):
    st.subheader('Credit data')
    st.write((data.groupby("education").credit_score.mean().reset_index()\
.sort_values("credit_score")))

values = st.sidebar.slider('Credit range for education levels', float(data.credit_score.min()), 1., (0., .5))
f = px.histogram(data.query(f'credit_score.between{values}'), x='education',
nbins=15, title='Average Credit Score Per Education Level')
f.update_xaxes(title='Education Level')
f.update_yaxes(title='Credit Score')

if st.checkbox('Show Education and Avg Credit Score'):
    st.subheader('Avg Credit Score per Education Level')
    st.write(f)

AP = px.histogram(data, x=data['age'],y=data['past_accidents'],histfunc="sum",barmode='stack',text_auto='.2s')
AP.update_layout(
    title="Age and Past Accidents",
    yaxis_title="Accidents",
    xaxis_title="Age")
if st.checkbox('Show Age and Past Accidents'):
    st.subheader('Frequency of Age and Accidents')
    st.write(AP)

fig1 = px.histogram(data, x=df['GENDER'],y=df['OUTCOME'],histfunc="sum",barmode='stack',text_auto='.2s')
fig1.update_layout(
    title="Does Gender and Vehicle Type Affect Claiming Insurance?",
    yaxis_title="Claimed Insurance",
    xaxis_title="Gender",
    legend_title="Vehicle Type")

vt=df['VEHICLE_TYPE'].value_counts().nlargest(7)
vts=df['VEHICLE_TYPE'].value_counts().nlargest(7).index
fig2=px.pie(values=vt,names=vts)
fig2.update_layout(
    title="Percentage of Vehicle Type",
    legend_title="Vehicle Type")
fig2.update_traces(textinfo = 'percent+label')

fig3 = px.histogram(df, x=df['VEHICLE_YEAR'],y=df['OUTCOME'],
                   histfunc="sum",color='GENDER', barmode='stack',
                   text_auto='.2s')
fig3.update_layout(
    title="Does Age of Vehicle Affect Claiming Insurance?",
    xaxis_title="Vehicle Age",
    yaxis_title="Claimed Insurance",
    legend_title="Gender")

chart_visual = st.sidebar.selectbox('Select Charts/Plot type',
                                    ['All','Gender and Vehicle', 'Percentage of Vehicle Type'])

if chart_visual == 'Gender and Vehicle':
        fig1
elif chart_visual == 'Percentage of Vehicle Type':
        fig2
elif chart_visual == 'Age of Vehicle':
        fig3


st.sidebar.write("You selected", chart_visual)
