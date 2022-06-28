import streamlit as st

from pathlib import Path
import pandas as pd
import numpy as np

import geopandas as gpd
import pyproj
import plotly.express as px

st.set_page_config(
    page_title="",
    page_icon="chart_with_upwards_trend",
#    layout="wide",
)

#################################################

dicNUTS = {
    'Bundesländer' : 'nuts1',
    'Regierungsbezirke' : 'nuts2',
    'Landkreise' : 'nuts3',
}

#################################################
@st.cache
def get_data(tmpEbene):
    tmpNUTS = gpd.read_file(str(Path.cwd()) + '\\' + tmpEbene + '.geojson')
    tmpNUTS = tmpNUTS.to_crs(pyproj.CRS.from_epsg(4326))
    tmpNUTS = tmpNUTS.set_index('NUTS_NAME')
    tmpNUTS['DummyTRW'] = np.random.randint(1, 10000, tmpNUTS.shape[0])

    return tmpNUTS

my_geo_nuts1 = get_data('nuts1')
my_geo_nuts2 = get_data('nuts2')
my_geo_nuts3 = get_data('nuts3')


##################################################
with st.sidebar:

    lst_nuts1 = st.multiselect(
                    "Auswahl Bundesländer",
                    my_geo_nuts1.index.unique(),
    )

    lst_nuts2 = st.multiselect(
                    "Auswahl Regierungsbezirke",
                    my_geo_nuts2.index.unique(),
    )

    lst_nuts3 = st.multiselect(
                    "Auswahl Landkreise",
                    my_geo_nuts3.index.unique(),
    )

    str_ebene = st.selectbox(
                    "Auswahl-Ebene",
                    dicNUTS.keys(),
    )

st.write(f"Ausgewählt: {dicNUTS[str_ebene]}")

##################################################

if dicNUTS[str_ebene] == 'nuts1':
    my_geo_data = my_geo_nuts1.copy()
    lst_region = lst_nuts1
elif dicNUTS[str_ebene] == 'nuts2':
    my_geo_data = my_geo_nuts2.copy()
    lst_region = lst_nuts2
elif dicNUTS[str_ebene] == 'nuts3':
    my_geo_data = my_geo_nuts3.copy()
    lst_region = lst_nuts3
else:
    my_geo_data = my_geo_nuts1.copy()
    lst_region = lst_nuts1


if len(lst_region) > 0:
    my_plot = my_geo_data[my_geo_data.index.isin(lst_region)].copy()
else:
    my_plot = my_geo_data.copy()

fig = px.choropleth(my_plot,
    #title=nuts_ebene,
    geojson=my_plot.geometry,
    locations=my_plot.index,
    color="DummyTRW",
    color_continuous_scale='twilight',
    #color_discrete_sequence=px.colors.qualitative.Dark2,
    projection='mercator',
    height=500,
    )

fig.update_geos(
    fitbounds="locations", 
    visible=False,
)

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    #paper_bgcolor='black',
            )

st.plotly_chart(fig)
