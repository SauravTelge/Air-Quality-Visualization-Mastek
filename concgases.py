import requests
from pandas import json_normalize 
import json
import pandas as pd
import plotly
import plotly.express as px
import pickle
dat = pd.read_csv('m-ward.csv')
risk = [[x for x in range(432)] for y in range(432)]
dict1={"AQI":[],"time":[],"M-Ward regions :":[],"pm2.5":[],"risk":risk,"o3":[],"pm10":[],"no2":[],"co":[],"so2":[]}
for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
    querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
    url = "https://air-quality.p.rapidapi.com/forecast/airquality"
    headers = {
        'x-rapidapi-key': "9d950a324fmshdef5c119c4e8cd1p174f6bjsn6dc9cc60214b",
        'x-rapidapi-host': "air-quality.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
 
    pretty_json = json.loads(response.text)



    for i in range(0,72):
        time1 = pretty_json['data'][i]['timestamp_local']
        aqi=pretty_json['data'][i]['aqi']
        pm25=pretty_json['data'][i]['pm25']
        o3=pretty_json['data'][i]['o3']
        so2=pretty_json['data'][i]['so2']
        no2=pretty_json['data'][i]['no2']
        pm10=pretty_json['data'][i]['pm10']
        co=pretty_json['data'][i]['co']
        dict1['o3'].append(o3)
        dict1['AQI'].append(aqi)
        dict1['time'].append(time1)
        dict1['M-Ward regions :'].append(place)
        dict1['pm2.5'].append(pm25)
        dict1['pm10'].append(pm10)
        dict1['co'].append(co)
        dict1['so2'].append(so2)
        dict1['no2'].append(no2)
    for i in range(len(dict1['pm2.5'])):
        # print(dict1['risk'][i])
        if dict1['pm2.5'][i]>0 and dict1['pm2.5'][i]<50:
            dict1['risk'][i]='0'
        elif dict1['pm2.5'][i]>50 and dict1['pm2.5'][i]<100:
            dict1['risk'][i]='1'
        elif dict1['pm2.5'][i]>100 and dict1['pm2.5'][i]<200:
            dict1['risk'][i]='2'
        elif dict1['pm2.5'][i]>200 and dict1['pm2.5'][i]<300:
            dict1['risk'][i]='3'
        elif dict1['pm2.5'][i]>300 and dict1['pm2.5'][i]<400:
            dict1['risk'][i]='4'
        elif dict1['pm2.5'][i]>400 and dict1['pm2.5'][i]<500:
            dict1['risk'][i]='5'
df=pd.DataFrame(dict1)


fig = px.scatter(df, x='pm2.5', y='risk', color='M-Ward regions :', size='pm2.5', size_max=60, 
                hover_name='M-Ward regions :' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

filename = 'pm25.sav'
pickle.dump(graphJSON, open(filename, 'wb'))
# fig.write_html("templates/concpm25.html")
fig = px.scatter(df, x='pm10', y='risk', color='M-Ward regions :', size='pm10', size_max=60, 
                hover_name='M-Ward regions :' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])

# fig.write_html("templates/concpm10.html")
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

filename = 'pm10.sav'
pickle.dump(graphJSON, open(filename, 'wb'))
fig = px.scatter(df, x='no2', y='risk', color='M-Ward regions :', size='no2', size_max=60, 
                hover_name='M-Ward regions :' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])

# fig.write_html("templates/concno2.html")
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

filename = 'no2.sav'
pickle.dump(graphJSON, open(filename, 'wb'))
fig = px.scatter(df, x='so2', y='risk', color='M-Ward regions :', size='so2', size_max=60, 
                hover_name='M-Ward regions :' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])

# fig.write_html("templates/concso2.html")
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

filename = 'so2.sav'
pickle.dump(graphJSON, open(filename, 'wb'))
fig = px.scatter(df, x='o3', y='risk', color='M-Ward regions :', size='o3', size_max=60, 
                hover_name='M-Ward regions :' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])

# fig.write_html("templates/conco3.html")
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

filename = 'o3.sav'
pickle.dump(graphJSON, open(filename, 'wb'))
fig = px.scatter(df, x='co', y='risk', color='M-Ward regions :', size='co', size_max=60, 
                hover_name='M-Ward regions :' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 2000],range_y=[-1,6])
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

filename = 'co.sav'
pickle.dump(graphJSON, open(filename, 'wb'))
# fig.write_html("templates/concco.html")

