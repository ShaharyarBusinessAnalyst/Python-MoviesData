import json

movie_info_list = load_data("disney_data_cleaned_more.json")

# http://www.omdbapi.com/?apikey=[yourkey]&

import requests 
import os
import urllib

def get_omdb_info(title):
    base_url = "http://www.omdbapi.com/"
    parameters = {"apikey": os.environ['OMDB_API_KEY'], 't': title}
    params_encoded = urllib.parse.urlencode(parameters)
    full_url = base_url + "?" + params_encoded
    
    response = requests.get(full_url)
    
    # Print the response text for troubleshooting
    print(response.text)
    
    return response.json()

get_omdb_info('into the woods')

for movie in movie_info_list:
    title = movie['title']
    omdb_info = get_omdb_info(title)
    movie['imdb'] = omdb_info.get('imdbRating',None)
    movie['metascore'] = omdb_info.get('Metascore', None)

movie_info_copy = [movie.copy() for movie in movie_info_list]


#converting datetime string into datetime object
from datetime import datetime
for movie in movie_info_copy:
    current_date_str = movie['Release date(datetime)']
    
    if current_date_str and current_date_str != 'NA':
        current_date = datetime.strptime(current_date_str, "%Y-%m-%dT%H:%M:%S")
        movie['Release date(datetime)'] = current_date.strftime("%B %d, %Y")
    else:
        movie['Release date (datetime)'] = None

save_data("disney_final.json", movie_info_copy)


#saving into csv
import pandas as pd
df = pd.DataFrame(movie_info_list)

df.to_csv("disney_movie_data_final.csv")