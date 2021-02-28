import requests
from pandas import json_normalize 
import json
import pandas as pd
import plotly.express as px
dat = pd.read_excel('m-ward.xlsx')
risk = [[x for x in range(240)] for y in range(240)]
dict1={"AQI":[],"time":[],"city":[],"pm2.5":[],"risk":risk,"o3":[]}
for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
    querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
    url = "https://air-quality.p.rapidapi.com/forecast/airquality"
    headers = {
        'x-rapidapi-key': "3b22fa1263mshb51aa6ab6be5039p122353jsn10ddade3b058",
        'x-rapidapi-host': "air-quality.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
 
    pretty_json = json.loads(response.text)



    for i in range(0,48):
        time1 = pretty_json['data'][i]['timestamp_local']
        aqi=pretty_json['data'][i]['aqi']
        city=pretty_json['city_name']
        pm25=pretty_json['data'][i]['pm25']
        o3=pretty_json['data'][i]['o3']
        dict1['o3'].append(o3)
        dict1['AQI'].append(aqi)
        dict1['time'].append(time1)
        dict1['city'].append(city)
        dict1['pm2.5'].append(pm25)
    for i in range(len(dict1['o3'])):
        # print(dict1['risk'][i])
        if dict1['pm2.5'][i]>0 and dict1['pm2.5'][i]<30:
            dict1['risk'][i]='0'
        elif dict1['pm2.5'][i]>30 and dict1['pm2.5'][i]<60:
            dict1['risk'][i]='1'
        elif dict1['pm2.5'][i]>60 and dict1['pm2.5'][i]<90:
            dict1['risk'][i]='2'
        elif dict1['pm2.5'][i]>90 and dict1['pm2.5'][i]<120:
            dict1['risk'][i]='3'
        elif dict1['pm2.5'][i]>120 and dict1['pm2.5'][i]<150:
            dict1['risk'][i]='4'
        elif dict1['pm2.5'][i]>150 and dict1['pm2.5'][i]<500:
            dict1['risk'][i]='5'
df=pd.DataFrame(dict1)


fig = px.scatter(df, x='o3', y='risk', color='city', size='o3', size_max=60, 
                hover_name='city' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])

fig.write_html("templates/conco3.html")
