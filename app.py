from flask import Flask, render_template, request,Response
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
stations = ['Chembur', 'Mahul', 'Govandi', 'Mankhurd', 'Tilak Nagar','Anushakti nagar']
# Handle requests to the root of the web site, returning the home page
data = pd.read_csv(r"m-ward.csv")
aqilist = []
timeStamp = ""
for lon1,lat1 in zip(data['Longitude'],data['Latitude']):
    querystring = {"lat":f"{lat1}","lon":f"{lon1}","hours":"72"}
    url = "https://air-quality.p.rapidapi.com/forecast/airquality"
    headers = {
        'x-rapidapi-key': "a9234b6173mshae3954f7f9751ebp101cafjsn885852508da6",
        'x-rapidapi-host': "air-quality.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    pretty_json = json.loads(response.text)

    aqi2=pretty_json['data'][0]['aqi']

    timeStamp=pretty_json['data'][0]['timestamp_local']
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

# dat = pd.read_csv('m-ward-new.csv')
# for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
#     querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
#     url = "https://air-quality.p.rapidapi.com/forecast/airquality"
#     headers = {
#         'x-rapidapi-key': "9a6ba754b5mshc3a4204662632f8p195c72jsn3c383b057633",
#         'x-rapidapi-host': "air-quality.p.rapidapi.com"
#         }

#     response = requests.request("GET", url, headers=headers, params=querystring)

#     pretty_json = json.loads(response.text)
#     aqi = [x['aqi'] for x in pretty_json["data"]]
#     pm10 = [x['pm10'] for x in pretty_json["data"]]
#     pm25 = [x['pm25'] for x in pretty_json["data"]]
#     o3 = [x['o3'] for x in pretty_json["data"]]
#     so2 = [x['so2'] for x in pretty_json["data"]]
#     no2 = [x['no2'] for x in pretty_json["data"]]
#     date = [x['datetime'] for x in pretty_json["data"]]
#     co = [x['co'] for x in pretty_json["data"]]
#     fin = [date,aqi,pm10,pm25,o3,so2,no2,co]
#     lst  =[]

#     for i in range(len(aqi)):
#         lst.append([fin[j][i] for j in  range(len(fin))])
#     dict1={}
#     dict1["Data"]=lst 
#     out_file = open(f"templates/{place}.txt", "w") 
#     json.dump(dict1, out_file, indent = 6)  


@app.route("/")
def home():
    return render_template("index.html",maxAqi = maxAqi, minAqi = minAqi, count = count, time = time, minStn = minStn, maxStn = maxStn )
# @app.route('/Mahul.txt')
# def ajax_ddl():
#     # content = 
#     # return Response(content, mimetype='text/plain')
#     return Flask.send_file("Mahul.txt")
@app.route("/map",methods=['POST','GET'])
def map():
    return render_template("name1.html" )
# @app.route("/conc")
# def conc():
#     dat = pd.read_csv('m-ward.csv')
#     risk = [[x for x in range(432)] for y in range(432)]
#     dict1={"AQI":[],"time":[],"city":[],"pm2.5":[],"risk":risk,"o3":[],"pm10":[],"no2":[],"co":[],"so2":[]}
#     for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
#         querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
#         url = "https://air-quality.p.rapidapi.com/forecast/airquality"
#         headers = {
#             'x-rapidapi-key': "53a2f1748amsh984a4730615f95ep104028jsnc36cf32edcd9",
#             'x-rapidapi-host': "air-quality.p.rapidapi.com"
#             }

#         response = requests.request("GET", url, headers=headers, params=querystring)
    
#         pretty_json = json.loads(response.text)



#         for i in range(0,72):
#             time1 = pretty_json['data'][i]['timestamp_local']
#             aqi=pretty_json['data'][i]['aqi']
#             pm25=pretty_json['data'][i]['pm25']
#             o3=pretty_json['data'][i]['o3']
#             so2=pretty_json['data'][i]['so2']
#             no2=pretty_json['data'][i]['no2']
#             pm10=pretty_json['data'][i]['pm10']
#             co=pretty_json['data'][i]['co']
#             dict1['o3'].append(o3)
#             dict1['AQI'].append(aqi)
#             dict1['time'].append(time1)
#             dict1['city'].append(place)
#             dict1['pm2.5'].append(pm25)
#             dict1['pm10'].append(pm10)
#             dict1['co'].append(co)
#             dict1['so2'].append(so2)
#             dict1['no2'].append(no2)
#         for i in range(len(dict1['pm2.5'])):
#             # print(dict1['risk'][i])
#             if dict1['pm2.5'][i]>0 and dict1['pm2.5'][i]<50:
#                 dict1['risk'][i]='0'
#             elif dict1['pm2.5'][i]>50 and dict1['pm2.5'][i]<100:
#                 dict1['risk'][i]='1'
#             elif dict1['pm2.5'][i]>100 and dict1['pm2.5'][i]<200:
#                 dict1['risk'][i]='2'
#             elif dict1['pm2.5'][i]>200 and dict1['pm2.5'][i]<300:
#                 dict1['risk'][i]='3'
#             elif dict1['pm2.5'][i]>300 and dict1['pm2.5'][i]<400:
#                 dict1['risk'][i]='4'
#             elif dict1['pm2.5'][i]>400 and dict1['pm2.5'][i]<500:
#                 dict1['risk'][i]='5'
#     df=pd.DataFrame(dict1)

#     def createp():
#         fig = px.scatter(df, x='pm2.5', y='risk', color='city', size='pm2.5', size_max=60, 
#                         hover_name='city' , log_x=True,animation_frame='time',
#                         animation_group='risk',range_x=[1, 500],range_y=[-1,6])
                        
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return graphJSON
#     conce=createp()
#     return render_template("graphs.html" ,concc=conce)
# @app.route("/concpm25")
# def conc1():
#     return render_template("concpm25.html" )
# @app.route("/concpm10")
# def conc2():
#     return render_template("concpm10.html" )
# @app.route("/conco3")
# def conc3():
#     return render_template("conco3.html" )
# @app.route("/concso2")
# def conc4():
#     return render_template("concso2.html" )
@app.route("/mapbox10.html",methods=['POST','GET'])
def barg():
    # mapbox_access_token = 'pk.eyJ1IjoidGVqYXMyMDAwIiwiYSI6ImNrbDVhdnZmcDI0ZXYyc3FvNDN2c2I1eW0ifQ.qBCt-xKnG1nCx7ibUcIOcg'
    return render_template("mapbox10.html" )
@app.route("/mapbox3.html",methods=['POST','GET'])
def heatg():
    return render_template("mapbox3.html" )
@app.route("/graphs.html")
def graphe():

    filename = 'pm25.sav'
    l1 = pickle.load(open(filename, 'rb'))
    l2 = pickle.load(open('pm10.sav', 'rb'))
    l3 = pickle.load(open('no2.sav', 'rb'))
    l4 = pickle.load(open('so2.sav', 'rb'))
    l5 = pickle.load(open('o3.sav', 'rb'))
    l6 = pickle.load(open('co.sav', 'rb'))
    return render_template("graphs.html" ,g1=l1,g2=l2,g3=l3,g4=l4,g5=l5,g6=l6)
@app.route("/templates/tables.html")
def tables():
    
    
    return render_template("tables.html" )
@app.route("/predict",methods=['POST','GET'])
def forecast():
    
    featuredict = request.form["inpt"]
    feature = str(featuredict)
    dat = pd.read_csv('m-ward.csv')
    
    for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
        if place==feature:
            querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
            url = "https://air-quality.p.rapidapi.com/forecast/airquality"
            headers = {
                'x-rapidapi-key': "a9234b6173mshae3954f7f9751ebp101cafjsn885852508da6",
                'x-rapidapi-host': "air-quality.p.rapidapi.com"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            pretty_json = json.loads(response.text)
            dict1={"AQI":[],"time":[]}
            aqic=int(pretty_json['data'][0]['aqi'])
            pm25=int(pretty_json['data'][0]['pm25'])
            pm10=int(pretty_json['data'][0]['pm10'])
            o3=int(pretty_json['data'][0]['o3'])
            no2=int(pretty_json['data'][0]['no2'])
            so2=int(pretty_json['data'][0]['so2'])
            co=int(pretty_json['data'][0]['co'])
            co=co/10
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
    return render_template('index.html',pm25=pm25,pm10=pm10,place=feature,o3=o3,no2=no2,so2=so2,co=co,plot=bar, maxAqi = maxAqi, minAqi = minAqi, count = count, time = time, minStn = minStn, maxStn = maxStn,aqic=aqic)

if __name__ == '__main__':
    app.run(debug=True)