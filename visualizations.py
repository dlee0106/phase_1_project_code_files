"""
The following code was used to craft the visualizations for this project.
"""

#importing the necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline

#importing the data
restaurant = pd.read_csv('Restaurant.csv')

""""""""""""""""
RESTAURANT BY RATING BAR GRAPH
""""""""""""""""

by_rating = restaurant.groupby(['Ratings', 'Type'])['Business Id'].count().unstack()


labels = by_rating['Chinese'].index

x = np.arange(len(labels))
width=.35 

fig, ax = plt.subplots()
chinese = ax.bar(x - width/2, by_rating['Chinese'].values, width, label = 'Chinese')
italian = ax.bar(x + width/2, by_rating['Italian'].values, width, label = 'Italian', color = 'red')
ax.set_ylabel('Number of Restaurants')
ax.set_title('Restaurants by Rating')
ax.set_xticks(list(range(6)))
ax.set_xticklabels(labels)
ax.legend()

plt.show()

""""""""""""""""
RESTAURANT BY PRICE BAR GRAPH
""""""""""""""""

by_price = restaurant.groupby(['Price', 'Type'])['Business Id'].count().unstack()

labels = ["$","\$\$",'\$\$\$','\$\$\$\$']

x = np.arange(len(labels))
width=.35 

fig, ax = plt.subplots()
chinese = ax.bar(x - width/2, by_price['Chinese'].values, width, label = 'Chinese')
italian = ax.bar(x + width/2, by_price['Italian'].values, width, label = 'Italian', color = 'red')
ax.set_ylabel('Number of Restaurants')
ax.set_title('Restaurants by Price')
ax.set_xticks(list(range(4)))
ax.set_xticklabels(labels)
ax.legend()

plt.show()

------------

""""""""""""""""
DELIVERY BOX PLOTS
""""""""""""""""

#splitting the data into separate categories for easy manipulation
chinese_restaurants = restaurant[restaurant['Type'] == 'Chinese']

fig, ax = plt.subplots()
ax.boxplot([chinese_restaurants[chinese_restaurants['Delivery']==True]['Ratings'], chinese_restaurants[chinese_restaurants['Delivery']==False]['Ratings']])
ax.set_xticklabels(['Delivery', 'No Delivery'])
ax.set_ylabel('Rating')
ax.set_title('Chinese Restaurants Delivery Type')
plt.show()

#splitting the data into separate categories for easy manipulation
italian_restaurants = restaurant[restaurant['Type'] == 'Italian']

fig, ax = plt.subplots()
ax.boxplot([italian_restaurants[italian_restaurants['Delivery']==True]['Ratings'], italian_restaurants[italian_restaurants['Delivery']==False]['Ratings']])
ax.set_xticklabels(['Delivery', 'No Delivery'])
ax.set_ylabel('Rating')
ax.set_title('Italian Restaurants Delivery Type')
plt.show()

""""""""""""""""
RESTAURANT MAPS BY TYPE
""""""""""""""""

#Italian

import folium

#creating a list of values the add the map
restaurant_list =  [list(x) for x in zip(italian_restaurants['Latitude'].values,
                                         italian_restaurants['Longitude'].values,
                                         italian_restaurants['Business Name'].values,
                                         italian_restaurants['Type'].values)] 

nyc_map = folium.Map(location=[40.7589, -73.9851], zoom_start = 14)

def markers(iterables, nyc_map):
    """
    This function creates markers with popup labels and adds them to the map
    of NYC for a visual reference of restaurant locations
    """
    #making map markers and popups for each restaurant
    markers = list(map(lambda iterable: folium.Marker(location = iterable[:2],
                                                      popup = f'{iterable[2]}: {iterable[3]}'), iterables))
    for marker in markers:
        marker.add_to(nyc_map)
    
    return nyc_map

Italian_Restaurant_Map = markers(restaurant_list, nyc_map)

Italian_Restaurant_Map

#Chinese

import folium

#creating a list of values the add the map
restaurant_list =  [list(x) for x in zip(chinese_restaurants['Latitude'].values,
                                         chinese_restaurants['Longitude'].values,
                                         chinese_restaurants['Business Name'].values,
                                         chinese_restaurants['Type'].values)] 

nyc_map = folium.Map(location=[40.7589, -73.9851], zoom_start = 14)

def markers(iterables, nyc_map):
    """
    This function creates markers with popup labels and adds them to the map
    of NYC for a visual reference of restaurant locations
    """
    #making map markers and popups for each restaurant
    markers = list(map(lambda iterable: folium.Marker(location = iterable[:2],
                                                      popup = f'{iterable[2]}: {iterable[3]}'), iterables))
    for marker in markers:
        marker.add_to(nyc_map)
    
    return nyc_map

Chinese_Restaurant_Map = markers(restaurant_list, nyc_map)

Chinese_Restaurant_Map


