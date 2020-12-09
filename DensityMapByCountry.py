import pandas as pd
import reverse_geocoder as rg
import numpy as np
import json
import plotly.express as px
from shapely.geometry import shape
import shapely.prepared as shapelyprep
import shapely.vectorized as shapelyvect
from area import area

startMth = 1
endMth = 1
year = 2019

# read in json data (countries), *countries_updated contains same polys as world-countries, but with iso_a2 info
country_json = pd.read_json('countries_updated.json')

# create iso,area (km2) df (add monthly lightning counts later)
df = pd.DataFrame({'iso_a2': [], 'iso_a3': [], 'name': [], 'area_sqkm': []})
df.iso_a2 = [i['properties']['iso_a2'] for i in country_json.features]
df.iso_a3 = [i['properties']['iso_a3'] for i in country_json.features]
df.name = [i['properties']['name'] for i in country_json.features]
df.area_sqkm = [area(i['geometry'])/1000000 for i in country_json.features]  # m2 to km2

# load dissolved countries json (for clipping to land-only)
dissolvedCountry_json = pd.read_json('DissolvedCountries.geojson')
poly_countries = shape(dissolvedCountry_json['features'][0]['geometry'])
land_only_poly = shapelyprep.prep(poly_countries)

# load lightning data, get counts by country
for mth in range(startMth, endMth + 1):
    print('Loading month %s' % str(mth))

    tempDF = pd.read_csv('gld%s%s.zip' % (str(year), '{:02d}'.format(mth)), delim_whitespace=True,
                         header=None, usecols=[2, 3], names=['lat', 'lon'], dtype=float)

    # find indices of land (non-ocean) lightning strokes
    lonlatIdc = np.where(shapelyvect.contains(land_only_poly, tempDF.lon, tempDF.lat))

    tempDF = tempDF.iloc[lonlatIdc]

    # add country code, based on lat/lon
    geoInfo = rg.search(list(zip(tempDF.lat, tempDF.lon)))
    tempDF['iso_a2'] = ([list(i.values())[-1] for i in geoInfo])

    # get counts of lightning by country
    countryCounts_df = pd.DataFrame(tempDF.groupby('iso_a2').size())
    countryCounts_df = countryCounts_df[1:].reset_index()
    countryCounts_df.columns = ['iso_a2', 'counts_%s' % '{:02d}'.format(mth)]

    # add lightning counts to iso,area df
    df = df.join(countryCounts_df.set_index('iso_a2'), on='iso_a2')

# sum monthly counts and calculate density
df['density'] = ''
count_cols = [col for col in df.columns if 'counts' in col]
df.density = df[count_cols].sum(axis=1) / df.area_sqkm
df.to_csv('gldCountryCounts%s_%s-%s.csv' % (str(year), '{:02d}'.format(startMth), '{:02d}'.format(endMth)))

# open json file (countries) for plotting
with open('world-countries.json') as response:
    countries = json.load(response)

# open previously geocoded info
df = pd.read_csv('gldCountryCounts%s_%s-%s.csv' % (str(year), '{:02d}'.format(startMth), '{:02d}'.format(endMth)),
                 sep=',')
df.loc[df.density < 2] = df.loc[df.density < 2].round(1)
df.loc[df.density >= 2] = df.loc[df.density >= 2].round(0)

# plot
fig = px.choropleth(df, geojson=countries, locations='iso_a3', color='density', featureidkey='id',
                    locationmode='geojson-id',
                    color_continuous_scale='matter',
                    range_color=(1, 100),  # max(df.density)),
                    labels={'density': 'Average density<br>strokes / km<sup>2</sup> '},
                    hover_name='name', hover_data={'iso_a3': False})

fig.update_geos(visible=True, showcountries=False, lakecolor='rgba(0,0,0,0)')

fig.update_layout(margin={"r": 0, "t": 15, "l": 0, "b": 0})
fig.update_layout(coloraxis_colorbar=dict(
    title='<b>Average density<br>strokes / km<sup>2</sup><b>',
    tickvals=[0, 20, 40, 60, 80, 100],
    ticktext=['0', '20', '40', '60', '80', '>100'],
))
config = dict({'scrollZoom': True, 'responsive': True,
               'displaylogo': False, 'modeBarButtonsToRemove': ['toImage', 'select2d', 'lasso2d']})

fig.show(config=config)
# fig.write_html('CountryDensity_%s_%s-%s.html' % (str(year), '{:02d}'.format(startMth), '{:02d}'.format(endMth)),
#               auto_open=True, include_plotlyjs='cdn', config=config)
