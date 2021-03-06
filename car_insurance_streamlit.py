import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

st.sidebar.image('https://lms.aub.edu.lb/pluginfile.php/1/theme_lambda9/logo/1645015980/moodle-AUB_OSB_logo.png', use_column_width=True)
#st.image('https://github.com/SalemGrayzi/car_insurance/blob/main/image_2022-02-16_170524.png?raw=true', width=400)


inf='At Protsance (an insurance company) we would like to know:'
inf1='1- Who will run our insurance incase of an accident?'
inf2= '2- What attributes increase the risk of an accident?'
inf3='Data from 10k of our current customers was collected to achieve our goal of changing our rates according to specific conditions'
infs=inf,inf1,inf2,inf3
if(st.button("Intro")):
    st.markdown("Welcome To My First Streamlit Website")
    st.markdown('At Protsance (an insurance company) we would like to know:')
    st.markdown('1- Who will run our insurance incase of an accident?')
    st.markdown('2- What attributes increase the risk of an accident?')
    st.markdown('Data from 10k of our current customers was collected to achieve our goal of changing our rates according to specific conditions')


df =pd.read_csv("https://raw.githubusercontent.com/SalemGrayzi/car_insurance/main/car_insurance.csv")

st.title('Car Insurance')

@st.cache
def load_data(nrows):
    data =pd.read_csv("https://raw.githubusercontent.com/SalemGrayzi/car_insurance/main/car_insurance.csv")
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000000)
data_load_state.text("")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)



values = st.sidebar.slider('Credit range for education levels', float(data.credit_score.min()), 1., (0., .5))
f = px.histogram(data.query(f'credit_score.between{values}'), x='education',
nbins=15, title='Average Credit Score Per Education Level')
f.update_xaxes(title='Education Level')
f.update_yaxes(title='Sum of Customers of Selected Scores')

if st.checkbox('Show Education and Avg Credit Score'):
    st.subheader('Avg Credit Score per Education Level')
    st.write((data.groupby("education").credit_score.mean().reset_index()\
.sort_values("credit_score")),f)


Age_Group = st.sidebar.radio ("Age Group", ("16-25","26-39","40-64","65+",'All'))
if Age_Group == '16-25':
    AP=px.histogram(data, x=(data['age']=="16-25"),y=data['past_accidents'],
    histfunc="sum",barmode='stack',text_auto='.2s')
elif Age_Group == '26-39':
    AP=px.histogram(data, x=(data['age']=="26-39"),y=data['past_accidents'],
    histfunc="sum",barmode='stack',text_auto='.2s')
elif Age_Group == '40-64':
    AP=px.histogram(data, x=(data['age']=="40-64"),y=data['past_accidents'],
    histfunc="sum",barmode='stack',text_auto='.2s')

elif Age_Group == '65+':
    AP=px.histogram(data, x=(data['age']=="65+"),y=data['past_accidents'],
    histfunc="sum",barmode='stack',text_auto='.2s')
elif Age_Group=='All':
    AP=px.histogram(data, x=data['age'],y=data['past_accidents'],
    histfunc="sum",barmode='stack',text_auto='.2s').update_xaxes(categoryorder="total ascending")
if st.checkbox('Show Age and Past Accidents'):
    st.write(st.write(AP.update_layout(
        title="Age and Past Accidents",
        yaxis_title="Sum of Customers",
        xaxis_title="Had Accidents")))


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


vy=df['VEHICLE_YEAR'].value_counts()
vys=df['VEHICLE_YEAR'].value_counts().index
fig4=px.pie(values=vy,names=vys)
fig4.update_layout(
    title="Percentage of Vehicle Age",
    legend_title="Age of Vehicle")
fig4.update_traces(textinfo = 'percent+label')

fig5 = px.violin(df, x="OUTCOME", y="ANNUAL_MILEAGE",box=True,color='GENDER')
fig5.update_layout(
    title="Annual Mileage for Claiming Insurance",
    xaxis_title="Not Claimed or Claimed Insurance",
    yaxis_title="Annual Mileage",
    legend_title="Gender")

fig6=px.pie(values=df['DUIS'].value_counts().values,names=df['DUIS'].value_counts().index)
fig6.update_layout(
    title="Percentage of DUIS Offense",
    legend_title="Number/s of Offense")
fig6.update_traces(textinfo = 'percent+label')

pa=df['PAST_ACCIDENTS'].value_counts().nlargest(7)
pas=df['PAST_ACCIDENTS'].value_counts().nlargest(7).index
fig7=px.pie(values=pa,names=pas)
fig7.update_layout(
    title="Percentage of Past Accidents",
    legend_title="Number/s of Past Accidents")
fig7.update_traces(textinfo = 'percent+label')

pv=df['SPEEDING_VIOLATIONS'].value_counts().nlargest(7)
pvs=df['SPEEDING_VIOLATIONS'].value_counts().nlargest(7).index
fig8=px.pie(values=pv,names=pvs)
fig8.update_layout(
    title="Percentage of Speeding Offense",
    legend_title="Number/s of Offense")
fig8.update_traces(textinfo = 'percent+label')

fig9 = go.Figure()
fig9.add_trace(go.Histogram(x=df['OUTCOME'],y=df['SPEEDING_VIOLATIONS'],histfunc="avg",name="SPEEDING_VIOLATIONS"))
fig9.add_trace(go.Histogram(x=df['OUTCOME'],y=df['PAST_ACCIDENTS'],histfunc="avg",name="PAST_ACCIDENTS"))
fig9.add_trace(go.Histogram(x=df['OUTCOME'],y=df['DUIS'],histfunc="avg",name="DUIS"))
fig9.update_layout(
    title="Does Violation Increase Claiming Insurance?",
    xaxis_title="Violation of Law",
    yaxis_title="Claimed Insurance",
    legend_title="Violation Type")

fig10 = px.histogram(df, x=df['RACE'],y=df['OUTCOME'],histfunc="sum",color='INCOME', barmode='group',text_auto='.2s')
fig10.update_layout(
    title="Does Income Affect Claiming Insurance?",
    xaxis_title="Race",
    yaxis_title="Claimed Insurance",
    legend_title="Income Group")

fig11 = px.icicle(
    df,
    path= [px.Constant("Distribution of Customers"),'AGE','INCOME',"RACE"],
    values="OUTCOME",color_continuous_scale='Edge')

chart_visual = st.sidebar.selectbox('Select Histogram',
                                    ['None','Gender and Vehicle','Age of Vehicle',
                                    'Annual Mileage','Does Violation Increase Claiming Insurance?',
                                    'Income Group'])

if chart_visual == 'Gender and Vehicle':
        fig1
        st.write('As we can see from our visualization,we can conclude that male customers will have accidents more than females.')
elif chart_visual == 'Age of Vehicle':
        fig3,st.markdown('As we can see vehicles that fall below 2015 are at a higher risk of an accident, with male drivers crashing more than female drivers.')
elif chart_visual == 'Annual Mileage':
        fig5, st.markdown('We can conclude from this boxplot customers who drove more annually have a higher chance of an accident than driving less. Females drive more than males and have a more volatile violin compared to their not claimed counterpart')
elif chart_visual == 'Does Violation Increase Claiming Insurance?':
        fig9,st.markdown('As we can see from our data the number of customers using their insurance are much lower compared to not using it even though the violations are higher for customers who did not crash. This shows that violations are not correlated greatly to crashing.')
elif chart_visual == 'Income Group':
        fig10,st.markdown('Most people that are prone to having an accident are poverty and working class, in both races. This shows us that people in those groups are reckless drivers due to high numbers compared to other groups.')
elif chart_visual == 'None':
    st.write(str(''))
st.sidebar.write("You selected", chart_visual)

pie_visual = st.sidebar.selectbox('Select Pie Chart',
                                    ['None','Percentage of Vehicle Type',
                                    'Percentage of Vehicle Age',
                                    'Percentage of DUIS Offense',
                                    'Percentage of Past Accidents',
                                    'Percentage of Speeding Offense'])
if pie_visual == 'Percentage of Vehicle Type':
        fig2,st.markdown('majority of our customers crash in a sedan rather than sports car, this could be due to low numbers of sports car owners in  our data base of just 4.77%.')
elif pie_visual == 'Percentage of Vehicle Age':
        fig4,st.markdown('')
elif pie_visual == 'Percentage of DUIS Offense':
        fig6
elif pie_visual == 'Percentage of Past Accidents':
        fig7
elif pie_visual == 'Percentage of Speeding Offense':
        fig8
elif chart_visual == 'None':
    st.write(str(''))

st.sidebar.write("You selected", pie_visual)

if st.sidebar.checkbox('Show Distribution of Customers'):
    st.subheader("Customer Distribution")
    st.markdown('Overview of our customers in our data base who are prone to an accident')
    st.write(px.icicle(
        df,
        path= [px.Constant("Distribution of Customers"),'AGE','INCOME',"RACE"],
        values="OUTCOME",color_continuous_scale='Edge'))

if st.sidebar.checkbox('Show all graphs'):
    st.subheader('All Graphs')
    st.write(fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10,fig11)

if(st.button("About Me")):
    st.markdown("My name is Salem Grayzi,and the link to my Github: https://github.com/SalemGrayzi/car_insurance")
   
