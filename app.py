
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import json
import plotly
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import folium
import requests
from folium.plugins import MarkerCluster, FeatureGroupSubGroup, Fullscreen
import plotly.express as px
from plotly.subplots import make_subplots
# Initialize the Flask app
app = Flask(__name__)

# Handle requests to the root of the web site, returning the home page
stations = ['Powai', 'Worli', 'Kurla', 'Mahape', 'Colaba']
aqilist = []
timeStamp = ""
for station in stations:
    response = requests.get(f"https://api.waqi.info/search/?token=ec81c94493eacdee259a68cd8ceef4754afcae04&keyword={station},mumbai")
    res = response.json()
    timeStamp = res['data'][0]['time']['stime']
    aqi2 = res['data'][0]['aqi']
    aqilist.append(aqi2)

for i in range(0, len(aqilist)): 
    aqilist[i] = int(aqilist[i]) 
maxAqi = max(aqilist)
maxInd = aqilist.index(maxAqi)
maxStn = stations[maxInd]
minAqi = min(aqilist)
minInd = aqilist.index(minAqi)
minStn = stations[minInd]
count = len(aqilist)
time = timeStamp

dat = pd.read_csv('m-ward-new.csv')
for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
    querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
    url = "https://air-quality.p.rapidapi.com/forecast/airquality"
    headers = {
        'x-rapidapi-key': "9a6ba754b5mshc3a4204662632f8p195c72jsn3c383b057633",
        'x-rapidapi-host': "air-quality.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    pretty_json = json.loads(response.text)
    aqi = [x['aqi'] for x in pretty_json["data"]]
    pm10 = [x['pm10'] for x in pretty_json["data"]]
    pm25 = [x['pm25'] for x in pretty_json["data"]]
    o3 = [x['o3'] for x in pretty_json["data"]]
    so2 = [x['so2'] for x in pretty_json["data"]]
    no2 = [x['no2'] for x in pretty_json["data"]]
    date = [x['datetime'] for x in pretty_json["data"]]
    co = [x['co'] for x in pretty_json["data"]]
    fin = [date,aqi,pm10,pm25,o3,so2,no2,co]
    lst  =[]

    for i in range(len(aqi)):
        lst.append([fin[j][i] for j in  range(len(fin))])
    dict1={}
    dict1["Data"]=lst 
    out_file = open(f"templates/{place}.txt", "w") 
    json.dump(dict1, out_file, indent = 6)  

dat = pd.read_excel('E:\deepBlueGit\Trial-aqv\m-ward.xlsx')
risk = [[x for x in range(240)] for y in range(240)]
dict1={"AQI":[],"time":[],"city":[],"pm2.5":[],"risk":risk,"o3":[]}
for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
    querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"48"}
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


fig = px.scatter(df, x='pm2.5', y='risk', color='city', size='pm2.5', size_max=60, 
                hover_name='city' , log_x=True,animation_frame='time',
                 animation_group='risk',range_x=[1, 500],range_y=[-1,6])

fig.write_html("templates/conc.html")


@app.route("/")
def home():
    return render_template("index.html",maxAqi = maxAqi, minAqi = minAqi, count = count, time = time, minStn = minStn, maxStn = maxStn )
@app.route("/map",methods=['POST','GET'])
def map():
    return render_template("name1.html" )
@app.route("/conc")
def conc():
    return render_template("conc.html" )
@app.route("/mapbox1.html",methods=['POST','GET'])
def barg():
    mapbox_access_token = 'pk.eyJ1IjoidGVqYXMyMDAwIiwiYSI6ImNrbDVhdnZmcDI0ZXYyc3FvNDN2c2I1eW0ifQ.qBCt-xKnG1nCx7ibUcIOcg'
    return render_template("mapbox1.html",mapbox_access_token=mapbox_access_token )
@app.route("/mapbox3.html",methods=['POST','GET'])
def heatg():
    return render_template("mapbox3.html" )
@app.route("/graphs.html")
def graphe():
    return render_template("graphs.html" )
@app.route("/tables.html")
def tables():
    
    
    return render_template("tables.html" )
@app.route("/predict",methods=['POST','GET'])
def forecast():
    
    featuredict = request.form["inpt"]
    feature = str(featuredict)
    dat = pd.read_excel('m-ward.xlsx')
    
    for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
        if place==feature:
            querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
            url = "https://air-quality.p.rapidapi.com/forecast/airquality"
            headers = {
                'x-rapidapi-key': "9a6ba754b5mshc3a4204662632f8p195c72jsn3c383b057633",
                'x-rapidapi-host': "air-quality.p.rapidapi.com"
                }
        
            response = requests.request("GET", url, headers=headers, params=querystring)
            pretty_json = json.loads(response.text)
            dict1={"AQI":[],"time":[]}
            for i in range(0,48):
                time1 = pretty_json['data'][i]['timestamp_local']
                aqi=pretty_json['data'][i]['aqi']
                dict1['AQI'].append(aqi)
                dict1['time'].append(time1)
            
            df=pd.DataFrame(dict1)
            

    def create_plot():
        fig = px.bar(df,
                    x='time',
                    y='AQI',
                    color='AQI',
                    barmode='stack')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
    bar = create_plot()
    return render_template('index.html',plot=bar, maxAqi = maxAqi, minAqi = minAqi, count = count, time = time, minStn = minStn, maxStn = maxStn)

if __name__ == '__main__':
    app.run(debug=True)