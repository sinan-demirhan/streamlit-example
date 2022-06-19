import streamlit as st
import numpy as np
import pandas as pd
import json
import folium
from branca.element import Figure
from streamlit_folium import folium_static
#import pickle5 as pickle
import pickle
from folium import plugins
from folium.plugins import MeasureControl
from PIL import Image


my_algorithm = Image.open('modelling algorithm.png')


st.set_page_config(layout="wide")


@st.cache(allow_output_mutation=True)
def read_data(my_json):
    with open(my_json, 'rb') as handle:
        output_distances = pickle.load(handle)
    return output_distances


st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')
### SEASON RANGE ###
st.sidebar.markdown("**First select the station number you want to analyze:** 👇")




optimization_data = pd.read_csv("original_boston_data.csv")
optimal_data = read_data("optimal_stations.pickle")
my_working_city = st.sidebar.selectbox('Select the station number', list(optimal_data.keys())[:-1])
st.sidebar.text('')
agree = st.sidebar.checkbox('Show Model Algorithm')
st.sidebar.text('')
st.sidebar.text('')
st.sidebar.write("[MODELLING CODE](https://sinan-demirhan.github.io/ALL-PROJECTS/Projects/BOSTON%20OPTIMIZATION.html)")
st.sidebar.text('')
st.sidebar.text('')

my_csv = pd.read_csv("Boston Crimes Data 2017.csv").to_csv().encode('utf-8')

st.sidebar.download_button(
     label="Download Raw Data",
     data=my_csv,
     file_name='Boston Crimes Data 2017.csv',
     mime='text/csv',
 )


my_data_whs = pd.DataFrame(optimal_data[my_working_city])

potential_stations = pd.DataFrame(optimal_data['potential_stations'])


def plotting_main_map(optimization_data, my_data_whs):
    optimization_data = optimization_data.sample(2000).reset_index(drop=True)
    fig2 = Figure(width=840, height=500)        
    WHS_COORD = [optimization_data["Lat"][0],optimization_data["Long"][0]]
    map_nyc = folium.Map(location=WHS_COORD, zoom_start=12)


    for i in range(len(optimization_data)):

        folium.CircleMarker([optimization_data["Lat"][i],optimization_data["Long"][i]], 
                            radius=5,color=optimization_data["my_colours"][i], fill_color='#0080bb',
                            popup={'Incident Number':optimization_data["INCIDENT_NUMBER"][i]}).add_to(map_nyc)


    for j in range(len(my_data_whs)):
        folium.Marker([my_data_whs["Station_Lat"][j],my_data_whs["Station_Long"][j]], radius=5,
                      icon=folium.Icon(color='red', icon='info-sign'),
                      popup=
                     {"STATION": my_data_whs["Station_id"][j],
                             "LAT":my_data_whs["Station_Lat"][j],
                             "LON":my_data_whs["Station_Long"][j]}).add_to(map_nyc) 


    plugins.Fullscreen(position='topleft').add_to(map_nyc)
    map_nyc.add_child(MeasureControl())
    
    return map_nyc



if not agree:
    row_spacer1,row_1, row_spacer2 = st.columns((2, 6, 2))

    with row_1:
        st.text("")
        st.title('Optimal Station Modelling')
        st.text("Randomly Chosen {} potential station points.".format(len(potential_stations)))
        st.text("")
        folium_static(plotting_main_map(optimization_data, potential_stations))


    row2_spacer1,row2_1, row2_spacer2 = st.columns((2, 6, 2))

    with row2_1:
        st.text("Among these potential stations {} optimal stations were found".format(len(my_data_whs)))
        folium_static(plotting_main_map(optimization_data, my_data_whs))
        st.text("")
        st.text("")
else:
    st.image(my_algorithm, caption='The Algoritm',width = 1000)

    
    
    
    
    
    
    
