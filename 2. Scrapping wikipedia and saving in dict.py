from bs4 import BeautifulSoup as bs
import requests

#creating function to get lists
#also replacing unwanted xa0 characters

def get_content_value(row_data):
    if row_data.find('li'):
        return[li.get_text(" ", strip = True).replace("\xa0"," ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ", strip = True).replace("\xa0"," ")

def get_info_box(url):
 
    #Load the webpage

    r = requests.get(url)

    #convert to beautifulsoup object
    soup = bs(r.content)
    info_box = soup.find(class_= "infobox vevent")
    info_rows = info_box.find_all("tr")


    #seperating header and rest of the table, creating a dictionary
    movie_info = {}
    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip = True)
        elif index ==1:
            continue
        else:
            content_key = row.find("th").get_text(" ", strip = True)
            content_value = get_content_value(row.find("td"))
            movie_info[content_key] = content_value
        
    return movie_info



#Load the webpage
r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
#convert to beautifulsoup object
soup = bs(r.content)
    
movies = soup.select(".wikitable.sortable i a")

base_path = "https://en.wikipedia.org/"

movie_info_list = []

for index, movie in enumerate(movies):
    if index==10:
        break
    try:
        relative_path = movie['href']
        title = movie['title']
        full_path = base_path + relative_path
        
        movie_info_list.append(get_info_box(full_path))
    
    except Exception as e:
        print(movie.get_text())
        print(e)


    
#function to save data
import json

def save_data(title,data):
    with open(title,'w', encoding='utf-8') as f:
        json.dump(data,f, ensure_ascii = False, indent = 2)

save_data("disney_data.json", movie_info_list)

#To load file
import json
def load_data(title):
    with open(title, encoding="utf-8") as f:
        return json.load(f)