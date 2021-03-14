import folium
import pandas as pd
import numpy as np
from folium import plugins
import branca
from folium.map import *
from folium.plugins import MeasureControl
from folium.plugins import MarkerCluster
from folium.map import Layer, LayerControl, FeatureGroup
from folium.plugins import MarkerCluster, FeatureGroupSubGroup, Fullscreen
import requests
import json

m = folium.Map(location=[19.047010705327335, 72.9126723062795], zoom_start=12.5)
data = pd.read_csv(r"m-ward-new1.csv")
data_aqi = data.iloc[:, 1:4]
d43 = pd.read_excel(r"400043(1).xlsx")
d71 = pd.read_excel(r"400071(1).xlsx")
d74 = pd.read_excel(r"400074(1).xlsx")
d88 = pd.read_excel(r"400088(1).xlsx")
d89 = pd.read_excel(r"400089(1).xlsx")
d94 = pd.read_excel(r"400094(1).xlsx")
locations_tuple = []
locations = [[], [], [], [], [], []]
locations_43 = []
locations_71 = []
locations_74 = []
locations_88 = []
locations_89 = []
locations_94 = []


# *************************************************************************************************************#

def popup_html_demographic(aqi, place, color, populationMale, populationFemale, literacy, sexRatio, childPopulation):
    html = """ 
  <!DOCTYPE html>
  <html>
  <body>
  <!--<div style='height: 50px;color:white; opacity: 0.8;background-color:{}'""".format(color) + """>
  <p style='padding-top: 10px;'>AQI: {}""".format(aqi) + """</p>
  </div>-->

  <div>
  <p><b>Place:</b> {}""".format(place) + """</p>
  </div>

  <div>
  <p><b>Population(Male):</b> {}""".format(populationMale) + """</p>
  </div>

  <div>
  <p><b>Population(Female):</b> {}""".format(populationFemale) + """</p>
  </div>

  <div>
  <p><b>Literacy Rate:</b> {}""".format(literacy) + """</p>
  </div>

  <div>
  <p><b>Sex Ratio:</b> {}""".format(sexRatio) + """</p>
  </div>

  <div>
  <p><b>Child population:</b> {}""".format(childPopulation) + """</p>
  </div>
  </body>
  </html>
  """

    return html


def popup_html_health(aqi, place, color, cardiac, allergic, copd):
    html = """ 
  <!DOCTYPE html>
  <html>
  <body>
  <!--<div style='height: 50px;color:white; opacity: 0.8;background-color:{}'""".format(color) + """>
  <p style='padding-top: 10px;'>AQI: {}""".format(aqi) + """</p>
  </div>-->

  <div>
  <p><b>Place:</b> {}""".format(place) + """</p>
  </div>

  <div>
  <p><b>Cardiac ailments:</b> {}""".format(cardiac) + """ per 10,000 people</p>
  </div>

  <div>
  <p><b>Allergic Rhintis:</b> {}""".format(allergic) + """ per 10,000 people</p>
  </div>

  <div>
  <p><b>COPD:</b> {}""".format(copd) + """ per 10,000 people</p>
  </div>

  </body>
  </html>
  """

    return html


def popup_html_aqi(aqi, place, color,so2, no2, pm10,co,o3,pm25):
    html = """ 
  <!DOCTYPE html>
  <html>
  <body>
  <div style='height: 50px;color:white; opacity: 0.8;background-color:{}'""".format(color) + """>
  <p style='padding-top: 10px;'>AQI: {}""".format(aqi) + """</p>

  </div>

  <div>
  <p><b>Place:</b> {}""".format(place) + """</p>
  </div>

  <div>
  <p><b>SO2 concentration:</b> {}""".format(so2) + """ ppm</p>
  </div>

  <div>
  <p><b>NO2 concentration:</b> {}""".format(no2) + """ ppm</p>
  </div>

  <div>
  <p><b>PM10 concentration:</b> {}""".format(pm10) + """ ppm</p>
  </div>
   <div>
  <p><b>CO concentration:</b> {}""".format(co) + """ ppm</p>
  </div>
   <div>
  <p><b>O3 concentration:</b> {}""".format(o3) + """ ppm</p>
  </div>
   <div>
  <p><b>PM2.5 concentration:</b> {}""".format(pm25) + """ ppm</p>
  </div>

  </body>
  </html>
  """

    return html


def colorEval(aqi):
    aqi=int(aqi)
    if aqi in range(0, 51):
        color = '#05F21A'
    elif aqi in range(51, 101):
        color = '#1C8D30'
    elif aqi in range(101, 151):
        color = '#56CD4D'
    elif aqi in range(151, 201):
        color = '#EAF016'
    elif aqi in range(201, 301):
        color = '#FE6A09'
    else:
        color = '#F50707'
    return color


# *************************************************************************************************************#

for latitude, longitude in zip(d43['Latitude'], d43['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_43.append(tuple(locations_tuple))
    locations_tuple = []

for latitude, longitude in zip(d71['Latitude'], d71['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_71.append(tuple(locations_tuple))
    locations_tuple = []

for latitude, longitude in zip(d74['Latitude'], d74['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_74.append(tuple(locations_tuple))
    locations_tuple = []

for latitude, longitude in zip(d88['Latitude'], d88['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_88.append(tuple(locations_tuple))
    locations_tuple = []

for latitude, longitude in zip(d89['Latitude'], d89['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_89.append(tuple(locations_tuple))
    locations_tuple = []

for latitude, longitude in zip(d94['Latitude'], d94['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_94.append(tuple(locations_tuple))
    locations_tuple = []

diction = {"locations_43": 3, "locations_71": 0, "locations_74": 2, "locations_88": 1, "locations_89": 4,
           "locations_94": 5}


def findcolor(loc):
    loc=int(loc)
    col = colorEval(loc)
    return col





# ****************************************************************************************************************8
def colorDecide(event):
    if event == 'AQI':
        color = 'red'
    elif event == 'Health':
        color = '#1AFAFF'
    elif event == 'Demography':
        color = 'green'
    return color


events = ['AQI', 'Health', 'Demography']
dic={}
for event in events:

    cluster = folium.plugins.MarkerCluster(control=False).add_to(m)

    subgroup = FeatureGroupSubGroup(cluster, name=event, control=True, show=True)

    for place, lat, lan,  health, populationMale, populationFemale, literacy, sexRatio, childPopulation,  cardiac, allergic, copd,lat1,lon1 in zip(
            data['Place'], data['Latitude'], data['Longitude'],  data['Health'], data['Population-Male'],
            data['Population-Female'],
            data['Litracy Rate'], data['Sex Ratio'], data['Child Population'],
            data['Cardiac Ailments'], data['Allergic Rhintis'], data['COPD'],data['lat'],data['lon']):
        
        url = "https://air-quality.p.rapidapi.com/forecast/airquality"

        querystring = {"lat":f"{lat1}","lon":f"{lon1}","hours":"72"}

        headers = {
            'x-rapidapi-key': "29b6513e48msh01b781d2f47959ap1dc775jsn99ae781400d8",
            'x-rapidapi-host': "air-quality.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        pretty_json = json.loads(response.text)
        aqi=pretty_json['data'][0]['aqi']
        so2=pretty_json['data'][0]['so2']
        no2=pretty_json['data'][0]['no2']
        pm10=pretty_json['data'][0]['pm10']
        o3=pretty_json['data'][0]['o3']
        co=pretty_json['data'][0]['co']
        pm25=pretty_json['data'][0]['pm25']
        dic[place]=aqi
        print(dic)
        if event == 'AQI':
            color = colorEval(aqi)
            html = popup_html_aqi(aqi, place, color, so2, no2, pm10,co,o3,pm25)
            iframe = branca.element.IFrame(html=html, width=400, height=280)
            popup = folium.Popup(iframe, parse_html=True)
            folium.Circle(location=[lat, lan], popup=popup, tooltip='<strong>Click to view AQI of ' + str(place),
                          radius=500, color=colorDecide(event), fill_color=colorDecide(event),
                          line_color=colorDecide(event),
                          name=event,
                          overlay=True).add_to(subgroup)

        if event == 'Health':
            color = colorEval(aqi)
            html = popup_html_health(aqi, place, color, cardiac, allergic, copd)
            iframe = branca.element.IFrame(html=html, width=300, height=150)
            popup = folium.Popup(iframe, parse_html=True)
            folium.CircleMarker(location=[lat, lan], popup=popup,
                                tooltip='<strong>Click to view Health of ' + str(place),
                                radius=25, color=colorDecide(event), fill_color=colorDecide(event),
                                line_color=colorDecide(event),
                                name=event,
                                overlay=True).add_to(subgroup)

        if event == 'Demography':
            color = colorEval(aqi)
            html = popup_html_demographic(aqi, place, color, populationMale, populationFemale, literacy, sexRatio,
                                          childPopulation)
            iframe = branca.element.IFrame(html=html, width=400, height=250)
            popup = folium.Popup(iframe, parse_html=True)
            folium.Marker(location=[lat, lan], popup=popup, tooltip='<strong>Click to view demography of ' + str(place),
                          icon=folium.Icon(color=colorDecide(event), icon_color='white', icon='cloud')
                          ).add_to(subgroup)

    subgroup.add_to(m)
folium.Polygon(locations_43, popup=None, color=findcolor(dic['Shivaji Nagar']), weight=4, opacity=0.8,
               fill_color=findcolor(dic['Shivaji Nagar'])).add_to(m)
folium.Polygon(locations_71, popup=None, color=findcolor(dic['Chembur']), weight=4, opacity=0.8,
               fill_color=findcolor(dic['Chembur'])).add_to(m)
folium.Polygon(locations_74, popup=None, color=findcolor(dic['Mahul']), weight=4, opacity=0.8,
               fill_color=findcolor(dic['Mahul'])).add_to(m)
folium.Polygon(locations_88, popup=None, color=findcolor(dic['Govandi']), weight=4, opacity=0.8,
               fill_color=findcolor(dic['Govandi'])).add_to(m)
folium.Polygon(locations_89, popup=None, color=findcolor(dic['Tilak Nagar']), weight=4, opacity=0.8,
               fill_color=findcolor(dic['Tilak Nagar'])).add_to(m)
folium.Polygon(locations_94, popup=None, color=findcolor(dic['Anushakti']), weight=4, opacity=0.8,
               fill_color=findcolor(dic['Anushakti'])).add_to(m)
folium.LayerControl(collapsed=False).add_to(m)
m.save(outfile="templates/name1.html")
