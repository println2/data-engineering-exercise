import geopandas as gpd
from math import radians, cos, sin, asin, sqrt
# import matplotlib.pyplot as plt
import folium
import os
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

cur_dir_path = os.path.abspath(os.getcwd())
absolute_file_name = os.path.join(cur_dir_path,'location',"AD_0_StatisticSector.shp")
df = gpd.read_file(absolute_file_name)
df = df.to_crs({'init': 'epsg:4326'})
df['centroid'] = df.centroid
home_lat = 4.3953
home_lon = 50.4875
perimeter_distance = 5

for i in range(0, len(df)):
    df.loc[i,'distance'] = haversine(home_lat,home_lon,df.iloc[i].centroid.coords[0][0],df.iloc[i].centroid.coords[0][1])
df = df[df['distance'] < 2]
mapit = folium.Map( location=[48, -102], zoom_start=9 )
for i in range(0, len(df)):
    folium.Marker( location=[ df.iloc[i].centroid.coords[0][0], df.iloc[i].centroid.coords[0][1] ],fill_color='#43d9de', radius=8).add_to( mapit )
mapit.save('map.html')
# ax = df["geometry"].plot()
# df["centroid"].plot(ax=ax, color="black")
# plt.show()