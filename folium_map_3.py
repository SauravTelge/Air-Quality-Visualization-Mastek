import folium
import pandas as pd
import numpy as np
from folium import plugins
from folium.map import *
from folium.plugins import MeasureControl
from folium.plugins import MarkerCluster
import requests
import branca
from folium.map import Layer, LayerControl, FeatureGroup
from folium.plugins import MarkerCluster, FeatureGroupSubGroup, Fullscreen
import json
import requests
import xlrd

m = folium.Map(location=[19.047010705327335, 72.9126723062795], zoom_start=12.5)
data = pd.read_csv(r"E:\MS learn\m-ward-new.csv")
data_aqi = data.iloc[:, 1:4]
d43 = pd.read_csv(r"E:\MS learn\400043-new.csv")
d71 = pd.read_csv(r"E:\MS learn\400071-new.csv")
d74 = pd.read_csv(r"E:\MS learn\400074-new.csv")
d88 = pd.read_csv(r"E:\MS learn\400088-new.csv")
d89 = pd.read_csv(r"E:\MS learn\400089-new.csv")

locations_tuple = []
locations = [[], [], [], [], [], []]
locations_43 = []
locations_71 = []
locations_74 = []
locations_88 = []
locations_89 = []


# *************************************************************************************************************#

def popup_html(aqi2, place, populationMale, populationFemale, literacy, sexRatio, childPopulation):

    color = colorEval(aqi2)
    html = """ 
  <!DOCTYPE html>
  <html>
  <body>
  <div style='height: 50px;color:white; opacity: 0.8;background-color:{};'""".format(color) + """>
  <p style='padding-top: 10px;'>AQI: {}""".format(aqi2) + """</p>
  </div>

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


def colorEval(aqi2):
    if aqi2 in range(0, 51):
        color = '#05F21A'
    elif aqi2 in range(51, 101):
        color = '#1C8D30'
    elif aqi2 in range(101, 151):
        color = '#56CD4D'
    elif aqi2 in range(151, 201):
        color = '#EAF016'
    elif aqi2 in range(201, 301):
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

for latitude, longitude in zip(d88['Latitude'], d88['longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_88.append(tuple(locations_tuple))
    locations_tuple = []

for latitude, longitude in zip(d89['Latitude'], d89['Longitude']):
    locations_tuple.append(latitude)
    locations_tuple.append(longitude)
    locations_89.append(tuple(locations_tuple))
    locations_tuple = []

folium.Polygon(locations_43, popup=None, color='red', weight=2, opacity=0.8, fill_color='red').add_to(m)
folium.Polygon(locations_71, popup=None, color='purple', weight=2, opacity=0.8, fill_color='purple').add_to(m)
folium.Polygon(locations_74, popup=None, color='green', weight=2, opacity=0.8, fill_color='green').add_to(m)
folium.Polygon(locations_88, popup=None, color='yellow', weight=2, opacity=0.8, fill_color='yellow').add_to(m)
folium.Polygon(locations_89, popup=None, color='black', weight=2, opacity=0.8, fill_color='black').add_to(m)


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

for event in events:

    cluster = folium.plugins.MarkerCluster(control=False).add_to(m)

    subgroup = FeatureGroupSubGroup(cluster, name=event, control=True, show=True)

    for place, lat, lan, aqi, health, populationMale, populationFemale, literacy, sexRatio, childPopulation in zip(
            data['Place'], data['Latitude'], data['Longitude'], data['AQI'], data['Health'], data['Population-Male'],
            data['Population-Female'],
            data['Litracy Rate'], data['Sex Ratio'], data['Child Population']):
        response = requests.get(
            f"https://api.waqi.info/search/?token=ec81c94493eacdee259a68cd8ceef4754afcae04&keyword={place},mumbai")
        res = response.json()
        aqi3 = res['data'][0]['aqi']
        
        aqi2 = int(aqi3) 
        if event == 'AQI':
            folium.Circle(location=[lat, lan], popup="AQI : " + str(aqi2),
                          tooltip='<strong>Click to view AQI of ' + str(place),
                          radius=500, color=colorDecide(event), fill_color=colorDecide(event),
                          line_color=colorDecide(event),
                          name=event,
                          overlay=True).add_to(subgroup)

        if event == 'Health':
            folium.CircleMarker(location=[lat, lan], popup="Health : " + str(health),
                                tooltip='<strong>Click to view Health of ' + str(place),
                                radius=25, color=colorDecide(event), fill_color=colorDecide(event),
                                line_color=colorDecide(event),
                                name=event,
                                overlay=True).add_to(subgroup)
        if event == 'Demography':
            # color = colorEval(aqi2)
            html = popup_html(aqi2, place, populationMale, populationFemale, literacy, sexRatio, childPopulation)
            iframe = branca.element.IFrame(html=html, width=400, height=280)
            popup = folium.Popup(iframe, parse_html=True)
            folium.Marker(location=[lat, lan], popup=popup, tooltip='<strong>Click to view demography of ' + str(place),
                          icon=folium.Icon(color=colorDecide(event), icon_color='white', icon='cloud')
                          ).add_to(subgroup)

    subgroup.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)
m.save(outfile="name1.html")
# *************************************************************************************************************#pip
