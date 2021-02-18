"""
The following functions are used in the process of data collection, filtering, transforming, and organizing the data into CSV files.
"""
#importing basic packages
import requests
import json
import pandas as pd
import os

#helper functions
#RESTAURANT DATA

def yelp_business_call(url, headers, url_params):
    """
    This function is setting up a singular url call
    """
    
    response = requests.get(url, headers=headers, params=url_params)
    
    return response.json()['businesses']

def parse_business_data(businesses, term):
    """
    This function is extracting the desired categories from the
    data recieved via the url call
    """
    #sorting for restaurants that have a price key
    has_price_key = list(filter(lambda business: 'price' in business.keys(), businesses))
    
    #sorting for restaurants that have the term we are looking for
    has_type = list(filter(lambda business: business['categories'][0]['title'] == term, has_price_key))
   
    #returning a list of terms with desired information
    return list(map(lambda business:(business['id'] ,business['name'] ,business['categories'][0]['title']
                                     ,business['coordinates']['latitude'], business['coordinates']['longitude'] 
                                     ,business['rating'] ,business['review_count'],business['price'] 
                                     ,business['location']['zip_code'],'delivery' in business['transactions']), has_type))

def df_business_save(parsed_results):
    """
    This function is creating a new DataFrame(on the first loop), 
    then adding to it the original as the loop goes on to combine 
    all the data collected into a single DataFrame
    """
    #This is checking to see if our DataFrame already exists
    path = os.path.exists('Restaurant.csv')
    
    if path == False:
        #This is making a new DataFrame on the first loop ONLY if the CSV doesn't exist
        parsed_results = pd.DataFrame(parsed_results, columns = ['Business Id','Business Name', 'Type', 'Latitude', 'Longitude', 'Ratings', 'Review_Counts', 'Price', 'Zipcode', 'Delivery'])

        parsed_results.to_csv('Restaurant.csv', index = False)

        #This is making a new DataFrame and concating it to 
        #the previous one created
    else:
        parsed_results = pd.DataFrame(parsed_results, columns = ['Business Id','Business Name', 'Type', 'Latitude', 'Longitude', 'Ratings', 'Review_Counts', 'Price', 'Zipcode', 'Delivery'])
        
        df = pd.read_csv('Restaurant.csv')
        
        df.append(parsed_results).to_csv('Restaurant.csv', index = False)




#REVIEW DATA
def yelp_review_call(url, headers):
    """
    This function is setting up a url call for the review data, and
    will be looped through so that it completes multiple url calls
    for the various restaurants and their reviews
    """
    
    response = requests.get(url, headers=headers)
    
    return response.json()['reviews']

def parse_review_data(review_list, url):
    """
    This function takes the review data recieved from the url calls 
    and extracts the desired data for analysis
    """
    #We are also including the business id used to collect the data in this list
    #This is indicated by the url.split('/')[-2]
    return list(map(lambda review: (url.split('/')[-2], review['user']['name'], review['rating'],
                                   review['text'], review['time_created'][:-9]),
                                   review_list))

def df_review_save(parsed_results, i):
    """
    This function creates a new DataFrame (on the first loop), and then
    adds to it as the loops increase to create a singular DataFrame of
    review data
    """
    #This creates a DataFrame on first iteration of loop.
    if i==0:

        parsed_results = pd.DataFrame(parsed_results, columns = ['Business Id', 'Reviewer Name', 'Rating', 'Text', 'Time Created'])
        
        parsed_results.to_csv('Review.csv', index = False)
        
    #This creates a new DataFrame and adds it onto the previous
    #one created.
    else:
        parsed_results = pd.DataFrame(parsed_results, columns = ['Business Id', 'Reviewer Name', 'Rating', 'Text', 'Time Created'])
    
        df = pd.read_csv('Review.csv')
    
        df.append(parsed_results).to_csv('Review.csv', index = False)
        


