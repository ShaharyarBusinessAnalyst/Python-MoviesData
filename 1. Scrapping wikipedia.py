from bs4 import BeautifulSoup as bs
import requests

#Load the webpage
r = requests.get("https://en.wikipedia.org/wiki/toy_Story_3")

#convert to beautifulsoup object
soup = bs(r.content)

#prettify just indents the result
contents = soup.prettify()
print(contents)

info_box = soup.find(class_="infobox vevent")
#print(info_box.prettify())

info_rows = info_box.find_all("tr")

for row in info_rows:
    print(row.prettify())

#creating function to get lists
#also replacing unwanted xa0 characters

def get_content_value(row_data):
    if row.find('li'):
        return[li.get_text(" ", strip = True).replace("\xa0"," ") for li in row_data.find_all("li")]
    else:
        return row_data.get_text(" ", strip = True).replace("\xa0"," ")


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
        
movie_info