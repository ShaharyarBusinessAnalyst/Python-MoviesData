import json
from bs4 import BeautifulSoup as bs
import requests

def load_data(title):
    with open(title, encoding="utf-8") as f:
        return json.load(f)


movie_info_list = load_data("disney_data.json")

#remove refrences( like [1], [2], etc.), removed by clean tags functions applied
#split long strings: fixed by stripped _strings and conditional header clause



def get_content_value(row_data):
    if row_data.find('li'):
        return[li.get_text(" ", strip = True).replace("\xa0"," ") for li in row_data.find_all("li")]
    elif row_data.find("br"):
        return[text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(" ", strip = True).replace("\xa0"," ")

def clean_tags(soup):
    for tag in soup.find_all(["sup","span"]):
        tag.decompose()
    
def get_info_box(url):
 
    #Load the webpage

    r = requests.get(url)

    #convert to beautifulsoup object
    soup = bs(r.content)
    info_box = soup.find(class_= "infobox vevent")
    info_rows = info_box.find_all("tr")
    
    clean_tags(soup)

    #seperating header and rest of the table, creating a dictionary
    movie_info = {}
    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip = True)
        elif index ==1:
            continue
        else:
            header = row.find('th')
            if header:
                content_key = row.find("th").get_text(" ", strip = True)
                content_value = get_content_value(row.find("td"))
                movie_info[content_key] = content_value

    return movie_info



#convert running time into integer: splitting string and taking first value if list
def minutes_to_integer(running_time):
    if running_time == "NA":
        return None
    
    if isinstance(running_time,list):
        return int(running_time[0].split(" ")[0])
    else:      #number is a string
        return int(running_time.split(" ")[0])
    
for movie in movie_info_list:
        movie['Running time (int)'] = minutes_to_integer(movie.get('Running time', "NA"))
    

#convert budget into float
import re

amounts = r"thousand|million|billion"
number = r"\d+(,\d{3})*\.*\d*"
word_re = rf"\${number}\s({amounts})"
value_re = rf"\${number}"

# case 1: money_conversion ($12.2 million) ----> 1220000
# case 2: money_conversion($789,000) ----> 789000

def word_to_value(word):
    value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    return value_dict[word]

def parse_word_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",",""))
    word = re.search(amounts,string).group()
    word_value = word_to_value(word)
    return value*word_value

def parse_value_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",",""))
    return value

def money_conversion(money):
    if money  == "NA":
        return None
    
    word_syntax = re.search(word_re,money)
    value_syntax = re.search(value_re,money)
    
    if word_syntax:
        return parse_word_syntax(word_syntax.group())
    elif value_syntax:
        return parse_value_syntax(value_syntax.group())
    else:
        return None

print(money_conversion("$790 million"))



#TASK 4 convert dates into Datetime

from datetime import datetime

dates = [movie.get('Release date', 'NA') for movie in movie_info_list]

def clean_date(date):
    return date.split("(")[0].strip()

def date_conversion(date):
    if isinstance(date, list):
        date = date[0]
        
    if date == "NA":
        return None
    
    date_str = clean_date(date)
    print(date_str)
    
    fmts = ["%B %d, %Y", "%d %B %Y"]
    for fmt in fmts:
        try:
            return datetime.strptime(date_str, fmt).isoformat()
        except:
            pass
    return None
 
   
for movie in movie_info_list:
    movie['Release date(datetime)'] = date_conversion(movie.get('Release date','NA'))

#function to save data
import json

def save_data(title,data):
    with open(title,'w', encoding='utf-8') as f:
        json.dump(data,f, ensure_ascii = False, indent = 2)
        
        
save_data("disney_data_cleaned_more.json", movie_info_list)