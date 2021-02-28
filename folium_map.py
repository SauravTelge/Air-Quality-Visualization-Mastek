import folium
import pandas as pd
import numpy as np
from folium import plugins
from folium.map import *
from folium.plugins import MeasureControl
from folium.plugins import MarkerCluster

from folium.map import Layer, LayerControl, FeatureGroup
from folium.plugins import MarkerCluster, FeatureGroupSubGroup, Fullscreen

import requests
data = pd.read_csv("23_01_data_test.csv")
data.head()
data_aqi = data.iloc[:, 1:4]


# print(data_aqi)


def colorEval(aqi):
    if aqi in range(0, 51):
        color = 'green'
    elif aqi in range(51, 101):
        color = 'yellow'
    elif aqi in range(101, 151):
        color = 'orange'
    elif aqi in range(151, 201):
        color = 'red'
    elif aqi in range(201, 301):
        color = 'purple'
    else:
        color = 'black'
    return color


def colorDecide(event):
    if event == 'AQI':
        color = 'red'
    elif event == 'Health':
        color = 'yellow'
    elif event == 'Literacy':
        color = 'green'
    return color


'''def popup_html(aqi, place, color):
  html = """ 
  <!DOCTYPE html>
  <html>
  <body>
  <div style='color:white; opacity: 0.8;background-color:{}'""".format(color)+""";>
  <p>AQI: {}""".format(aqi)+"""</p>
  </div>

  <div>
  <p>Place: {}""".format(place)+"""</p>
  </div>
  </body>
  </html>
  """

  return html'''

m1 = folium.Map(location=[19.0760, 72.8777], zoom_start=11.5)

events = ['AQI', 'Health', 'Literacy']

for event in events:

    cluster = folium.plugins.MarkerCluster(control=False).add_to(m1)

    subgroup = FeatureGroupSubGroup(cluster, name=event, control=True, show=True)

    for place, lat, lan, aqi in zip(data['Place'], data['Latitude'], data['Longitude'], data['AQI']):
        folium.CircleMarker(location=[lat, lan], popup="AQI : " + str(aqi),
                            tooltip='<strong>Click to view AQI of ' + str(place),
                            radius=25, color=colorDecide(event), fill_color=colorDecide(event),
                            line_color=colorDecide(event),
                            name=event,
                            overlay=True).add_to(subgroup)

    subgroup.add_to(m1)
folium.LayerControl(collapsed=False).add_to(m1)


