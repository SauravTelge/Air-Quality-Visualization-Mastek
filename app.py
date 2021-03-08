
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
model=pickle.load(open('model.pkl', 'rb'))
model1 =pickle.load(open('model1.pkl','rb'))
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
@app.route("/")
def home():
# #     m = folium.Map(location=[19.047010705327335, 72.9126723062795], zoom_start=12.5)
# #     data = pd.read_excel("m-ward.xlsx")
# #     data_aqi = data.iloc[:,1:4]
# #     d43 = pd.read_excel("400043.xlsx")
# #     d71 = pd.read_excel("400071.xlsx")
# #     d74 = pd.read_excel("400074.xlsx")
# #     d88 = pd.read_excel("400088.xlsx")
# #     d89 = pd.read_excel("400089.xlsx")

# #     locations_tuple = []
# #     locations = [[], [], [], [], [], []]
# #     locations_43 = []
# #     locations_71 = []
# #     locations_74 = []
# #     locations_88 = []
# #     locations_89 = []
# #     #*************************************************************************************************************#

# #     def popup_html(aqi, place, color, populationMale, populationFemale, literacy, sexRatio, childPopulation):
# #     response = requests.get(f"https://api.waqi.info/search/?token=ec81c94493eacdee259a68cd8ceef4754afcae04&keyword={place},mumbai")
# #     res=response.json()
            
# #     aqi2=res['data'][0]['aqi']

# #     html = """ 
# #     <!DOCTYPE html>
# #     <html>
# #     <body>
# #     <div style='height: 50px;color:white; opacity: 0.8;background-color:{}'""".format(color)+""">
# #     <p style='padding-top: 10px;'>AQI: {}""".format(aqi2)+"""</p>
# #     </div>

# #     <div>
# #     <p><b>Place:</b> {}""".format(place)+"""</p>
# #     </div>

# #     <div>
# #     <p><b>Population(Male):</b> {}""".format(populationMale)+"""</p>
# #     </div>

# #     <div>
# #     <p><b>Population(Female):</b> {}""".format(populationFemale)+"""</p>
# #     </div>

# #     <div>
# #     <p><b>Literacy Rate:</b> {}""".format(literacy)+"""</p>
# #     </div>

# #     <div>
# #     <p><b>Sex Ratio:</b> {}""".format(sexRatio)+"""</p>
# #     </div>

# #     <div>
# #     <p><b>Child population:</b> {}""".format(childPopulation)+"""</p>
# #     </div>
# #     </body>
# #     </html>
# #     """

# #     return html

# #     def colorEval(aqi):
# #     if aqi in range(0,51):
# #         color='#05F21A'
# #     elif aqi in range(51,101):
# #         color='#1C8D30'
# #     elif aqi in range(101,151):
# #         color='#56CD4D'
# #     elif aqi in range(151,201):
# #         color='#EAF016'
# #     elif aqi in range(201,301):
# #         color='#FE6A09'
# #     else:
# #         color='#F50707'
# #     return color
# #     #*************************************************************************************************************#

# #     for latitude, longitude in zip(d43['Latitude'], d43['Longitude']):
# #     locations_tuple.append(latitude)
# #     locations_tuple.append(longitude)
# #     locations_43.append(tuple(locations_tuple))
# #     locations_tuple = []

# #     for latitude, longitude in zip(d71['Latitude'], d71['Longitude']):
# #     locations_tuple.append(latitude)
# #     locations_tuple.append(longitude)
# #     locations_71.append(tuple(locations_tuple))
# #     locations_tuple = []


# #     for latitude, longitude in zip(d74['Latitude'], d74['Longitude']):
# #     locations_tuple.append(latitude)
# #     locations_tuple.append(longitude)
# #     locations_74.append(tuple(locations_tuple))
# #     locations_tuple = []

# #     for latitude, longitude in zip(d88['Latitude'], d88['longitude']):
# #     locations_tuple.append(latitude)
# #     locations_tuple.append(longitude)
# #     locations_88.append(tuple(locations_tuple))
# #     locations_tuple = []

# #     for latitude, longitude in zip(d89['Latitude'], d89['Longitude']):
# #     locations_tuple.append(latitude)
# #     locations_tuple.append(longitude)
# #     locations_89.append(tuple(locations_tuple))
# #     locations_tuple = []



# #     folium.Polygon(locations_43, popup=None, color='red', weight= 2,opacity = 0.8,fill_color='red').add_to(m)
# #     folium.Polygon(locations_71, popup=None, color='purple', weight= 2,opacity = 0.8, fill_color='purple').add_to(m)
# #     folium.Polygon(locations_74, popup=None, color='green', weight= 2,opacity = 0.8, fill_color='green').add_to(m)
# #     folium.Polygon(locations_88, popup=None, color='yellow', weight= 2,opacity = 0.8, fill_color='yellow').add_to(m)
# #     folium.Polygon(locations_89, popup=None, color='black', weight= 2,opacity = 0.8, fill_color='black').add_to(m)
# #     #****************************************************************************************************************8
# #     def colorDecide(event):
# #     if event=='AQI':
# #         color='red'
# #     elif event=='Health':
# #         color='#1AFAFF'
# #     elif event=='Literacy':
# #         color='green'
# #     return color

# #     events = ['AQI','Health', 'Literacy']

# #     for event in events:

# #     cluster = folium.plugins.MarkerCluster(control=False).add_to(m)

# #     subgroup = FeatureGroupSubGroup(cluster, name=event, control=True, show=True)

# #     for place, lat, lan, aqi, health, populationMale, populationFemale, literacy, sexRatio, childPopulation in zip(data['Place'], data['Latitude'], data['Longitude'], data['AQI'], data['Health'], data['Population-Male'], data['Population-Female'],
# #                                                                                                                     data['Litracy Rate'], data['Sex Ratio'], data['Child Population']):
# #         if event=='AQI':
# #         folium.Circle(location=[lat, lan], popup="AQI : " + str(aqi), tooltip='<strong>Click to view AQI of '+ str(place),
# #                             radius=500,color=colorDecide(event),fill_color=colorDecide(event),
# #                             line_color=colorDecide(event),
# #                             name=event,
# #                             overlay=True).add_to(subgroup)

# #         if event=='Health':
# #         folium.CircleMarker(location=[lat, lan], popup="Health : " + str(health), tooltip='<strong>Click to view Health of '+ str(place),
# #                             radius=25,color=colorDecide(event),fill_color=colorDecide(event),
# #                             line_color=colorDecide(event),
# #                             name=event,
# #                             overlay=True).add_to(subgroup)
# #         if event=='Literacy':
# #         color = colorEval(aqi)
# #         html = popup_html(aqi, place, color, populationMale, populationFemale, literacy, sexRatio, childPopulation)
# #         iframe = branca.element.IFrame(html=html,width=400,height=280)
# #         popup = folium.Popup(iframe,parse_html=True)
# #         folium.Marker(location=[lat, lan], popup=popup, tooltip='<strong>Click to view literacy of '+ str(place),
# #                             icon=folium.Icon(color=colorDecide(event), icon_color='white', icon='cloud' )
# #                             ).add_to(subgroup)


# #     subgroup.add_to(m)
# #     folium.LayerControl(collapsed=False).add_to(m)
    # dat = pd.read_excel('m-ward.xlsx')
    # risk = [[x for x in range(240)] for y in range(240)]

    # dict1={"AQI":[],"time":[],"city":[],"pm2.5":[],"risk":risk,"o3":[]}
    # def create_plot():
    #     # for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
    #     querystring = {"lat":"72.18","lon":"22.56","hours":"72"}
    #     url = "https://air-quality.p.rapidapi.com/forecast/airquality"
    #     headers = {
    #         'x-rapidapi-key': "9a6ba754b5mshc3a4204662632f8p195c72jsn3c383b057633",
    #         'x-rapidapi-host': "air-quality.p.rapidapi.com"
    #         }

    #     response1 = requests.request("GET", url, headers=headers, params=querystring)
    #     if response1:
    #         print("in r1")
    #         pretty_json1 = json.loads(response1.text)

    #         if pretty_json1:
    #             print(pretty_json1['data'][5]['timestamp_local'])
    #         else:
    #             print("null")

        # for i in range(0,48):
        #     time1 = pretty_json1['data'][i]['timestamp_local']
        #     aqi=pretty_json1['data'][i]['aqi']
        #     city=pretty_json1['city_name']
        #     pm25=pretty_json1['data'][i]['pm25']
        #     o3=pretty_json1['data'][i]['o3']
        #     dict1['o3'].append(o3)
        #     dict1['AQI'].append(aqi)
        #     dict1['time'].append(time1)
        #     dict1['city'].append(city)
        #     dict1['pm2.5'].append(pm25)
        # for i in range(len(dict1['pm2.5'])):
        #     # print(dict1['risk'][i])
        #     if dict1['pm2.5'][i]>0 and dict1['pm2.5'][i]<50:
        #         dict1['risk'][i]='0'
        #     elif dict1['pm2.5'][i]>50 and dict1['pm2.5'][i]<100:
        #         dict1['risk'][i]='1'
        #     elif dict1['pm2.5'][i]>100 and dict1['pm2.5'][i]<200:
        #         dict1['risk'][i]='2'
        #     elif dict1['pm2.5'][i]>200 and dict1['pm2.5'][i]<300:
        #         dict1['risk'][i]='3'
        #     elif dict1['pm2.5'][i]>300 and dict1['pm2.5'][i]<400:
        #         dict1['risk'][i]='4'
        #     elif dict1['pm2.5'][i]>400 and dict1['pm2.5'][i]<500:
        #         dict1['risk'][i]='5'
        # df=pd.DataFrame(dict1)

        # fig2 = px.scatter(df, x='pm2.5', y='risk', color='city', size='pm2.5', size_max=40, 
        #             hover_name='city' , log_x=True,animation_frame='time',
        #             animation_group='risk',range_x=[1, 500],range_y=[-1,6])
        # graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

        # return graphJSON2
    # bar = create_plot()
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
    dat = pd.read_excel('m-ward.xlsx')
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
    
    return render_template("tables.html" )
@app.route("/predict",methods=['POST','GET'])
def forecast():
    
    featuredict = request.form["inpt"]
    feature = str(featuredict)
    dat = pd.read_excel('m-ward.xlsx')
    

    # from statsmodels.tsa.stattools import adfuller
    # def ad_test(dataset):
    #     dftest = adfuller(dataset, autolag = 'AIC')
    #     print("1. ADF : ",dftest[0])
    #     print("2. P-Value : ", dftest[1])
    #     print("3. Num Of Lags : ", dftest[2])
    #     print("4. Num Of Observations Used For ADF Regression:",      dftest[3])
    #     print("5. Critical Values :")
    #     for key, val in dftest[4].items():
    #         print("\t",key, ": ", val)
    # ad_test(df['AQI'])

    # # from pmdarima import auto_arima
    # import warnings
    # warnings.filterwarnings("ignore")

    # # stepwise_fit = auto_arima(df['AQI'], trace=True,suppress_warnings=True)
    # # stepwise_fit.summary()

    # from statsmodels.tsa.arima_model import ARIMA
    # model=ARIMA(df['AQI'],order=(1,0,0))
    # model=model.fit()
    # model.summary()

    # index_future_dates = pd.date_range(start='2021-01-23', end = '2021-01-29')
    # pred = model.predict(start=len(df),end=len(df)+6,typ='levels',dynamic=False).rename("ARIMA predictions")
    # pred.index = index_future_dates
    # print(pred)

    # aqival=pred.to_frame()
    # aqival.rename(columns={'ARIMA predictions':'AQI'}, inplace=True)
    # aqival.index.name = "Date"
    # print(aqival)

    # dfnew = pd.concat([df,aqival])
    # dfnew['Date'] = dfnew.index

    # model1[0].read_csv(feature)
    # dfnew=model1[1]
    for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
        if place==feature:
            querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
            url = "https://air-quality.p.rapidapi.com/forecast/airquality"
            headers = {
                'x-rapidapi-key': "9a6ba754b5mshc3a4204662632f8p195c72jsn3c383b057633",
                'x-rapidapi-host': "air-quality.p.rapidapi.com"
                }
            # risk = [[x for x in range(240)] for y in range(240)]
            response = requests.request("GET", url, headers=headers, params=querystring)
            pretty_json = json.loads(response.text)
            dict1={"AQI":[],"time":[]}
            for i in range(0,48):
                time1 = pretty_json['data'][i]['timestamp_local']
                aqi=pretty_json['data'][i]['aqi']
                dict1['AQI'].append(aqi)
                dict1['time'].append(time1)
            
            df=pd.DataFrame(dict1)
            
            # for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):

            # for i in range(0,48):
            #     time1 = pretty_json1['data'][i]['timestamp_local']
            #     aqi=pretty_json1['data'][i]['aqi']
            #     city=pretty_json1['city_name']
            #     pm25=pretty_json1['data'][i]['pm25']
            #     o3=pretty_json1['data'][i]['o3']
            #     dict1['o3'].append(o3)
            #     dict1['AQI'].append(aqi)
            #     dict1['time'].append(time1)
            #     dict1['city'].append(city)
            #     dict1['pm2.5'].append(pm25)
            # for i in range(len(dict1['pm2.5'])):
            #     # print(dict1['risk'][i])
            #     if dict1['pm2.5'][i]>0 and dict1['pm2.5'][i]<50:
            #         dict1['risk'][i]='0'
            #     elif dict1['pm2.5'][i]>50 and dict1['pm2.5'][i]<100:
            #         dict1['risk'][i]='1'
            #     elif dict1['pm2.5'][i]>100 and dict1['pm2.5'][i]<200:
            #         dict1['risk'][i]='2'
            #     elif dict1['pm2.5'][i]>200 and dict1['pm2.5'][i]<300:
            #         dict1['risk'][i]='3'
            #     elif dict1['pm2.5'][i]>300 and dict1['pm2.5'][i]<400:
            #         dict1['risk'][i]='4'
            #     elif dict1['pm2.5'][i]>400 and dict1['pm2.5'][i]<500:
            #         dict1['risk'][i]='5'
            # df=pd.DataFrame(dict1)



    def create_plot():
        # def formatter(**kwargs):
        #     height = kwargs['AI']
        #     return "This bar is {:0.2f} units tall".format(height)
        # data = [
        #     go.Bar(
        #         x=dfnew['Date'], # assign x as the dataframe column 'x'
        #         y=dfnew['AQI'],
        #      )
        # ]
        # fig2 = px.scatter(df, x='pm2.5', y='risk', color='city', size='pm2.5', size_max=40, 
        #     hover_name='city' , log_x=True,animation_frame='time',
        #     animation_group='risk',range_x=[1, 500],range_y=[-1,6])
        # graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        fig = px.bar(df,
                    x='time',
                    y='AQI',
                    color='AQI',
                    barmode='stack')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
    bar = create_plot()
    return render_template('index.html',plot=bar, maxAqi = maxAqi, minAqi = minAqi, count = count, time = time, minStn = minStn, maxStn = maxStn)
    # return render_template('index.html',predic=model1)
# @app.route("/graphs.html")
# def maps():
#     dat = pd.read_excel('m-ward.xlsx')
#     risk = [[x for x in range(240)] for y in range(240)]

#     dict1={"AQI":[],"time":[],"city":[],"pm2.5":[],"risk":risk,"o3":[]}
#     def create():
#         for place,lat, lan in zip(dat['Place'],dat['Latitude'], dat['Longitude']):
#             querystring = {"lat":f"{lat}","lon":f"{lan}","hours":"72"}
#             url = "https://air-quality.p.rapidapi.com/forecast/airquality"
#             headers = {
#                 'x-rapidapi-key': "9a6ba754b5mshc3a4204662632f8p195c72jsn3c383b057633",
#                 'x-rapidapi-host': "air-quality.p.rapidapi.com"
#                 }

#             response = requests.request("GET", url, headers=headers, params=querystring)
        
#             pretty_json = json.loads(response.text)



#             for i in range(0,48):
#                 time1 = pretty_json['data'][i]['timestamp_local']
#                 aqi=pretty_json['data'][i]['aqi']
#                 city=pretty_json['city_name']
#                 pm25=pretty_json['data'][i]['pm25']
#                 o3=pretty_json['data'][i]['o3']
#                 dict1['o3'].append(o3)
#                 dict1['AQI'].append(aqi)
#                 dict1['time'].append(time1)
#                 dict1['city'].append(city)
#                 dict1['pm2.5'].append(pm25)
#             for i in range(len(dict1['pm2.5'])):
#                 # print(dict1['risk'][i])
#                 if dict1['pm2.5'][i]>0 and dict1['pm2.5'][i]<50:
#                     dict1['risk'][i]='0'
#                 elif dict1['pm2.5'][i]>50 and dict1['pm2.5'][i]<100:
#                     dict1['risk'][i]='1'
#                 elif dict1['pm2.5'][i]>100 and dict1['pm2.5'][i]<200:
#                     dict1['risk'][i]='2'
#                 elif dict1['pm2.5'][i]>200 and dict1['pm2.5'][i]<300:
#                     dict1['risk'][i]='3'
#                 elif dict1['pm2.5'][i]>300 and dict1['pm2.5'][i]<400:
#                     dict1['risk'][i]='4'
#                 elif dict1['pm2.5'][i]>400 and dict1['pm2.5'][i]<500:
#                     dict1['risk'][i]='5'
#         df=pd.DataFrame(dict1)

#         fig = px.scatter(df, x='pm2.5', y='risk', color='city', size='pm2.5', size_max=40, 
#                     hover_name='city' , log_x=True,animation_frame='time',
#                     animation_group='risk',range_x=[1, 500],range_y=[-1,6])
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#         return graphJSON
#     bar = create()
#     return render_template('graphs.html',plot=bar)

if __name__ == '__main__':
    app.run(debug=True)