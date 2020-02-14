from bs4 import BeautifulSoup
import requests
import urllib.request
from tqdm import tqdm
from dateutil import parser
from datetime import datetime
import os
from flask import request , Flask
import json

app = Flask(__name__)
@app.route("/fifa/", methods=['GET'])
def fifa ():
    league = "31"
    # for example use:
    # bundesliga 19
    # liga 53
    # serie A 31

    league_folder = "fifa-players-images"

    if not os.path.exists(league_folder):
        os.makedirs(league_folder)
        print("Folder created")
    else:
        print("Folder exists")


    print("Players scraping")
    links = []
    i = 0
    for page in tqdm(range(2)):
        html = requests.get("https://www.fifaindex.com/players/"+ str(page) +"/?league=" + league + "&order=desc").text
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.findAll(class_='link-player'):
            i += 1
            if i % 2 == 0:
                links.append(link.get('href'))


    print("Saving images...")
    i = 0
    images = []
    for link in tqdm(links):
        html = requests.get("https://www.fifaindex.com" + link).text
        soup = BeautifulSoup(html, 'html.parser')
        
        name = soup.h1.text.lower().replace(' fifa 19', "")
        name = name.replace(" ", "_")
        
        data_html = soup.findAll(class_="float-right")
        
        data_string = data_html[4].string
        data = parser.parse(data_string)
        data = data.strftime('%Y%m%d')
        image = soup.find(class_="player").get('data-srcset').split(",")[0][:-10] + ".png"
        images.append("https://www.fifaindex.com" + image)
        r = requests.get("https://www.fifaindex.com" + image, allow_redirects=False)
        open(league_folder +'/' + str(name) + '_' + data + '.png', 'wb').write(r.content)
        i += 1

    return "Done"
@app.route('/')
def index():
    return "add /fifa to url to get the players images folder in the same path"
if __name__ == "__main__":
    app.run(debug=True)
