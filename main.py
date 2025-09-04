import os
import requests
from bs4 import BeautifulSoup
import http.client, urllib

url = "https://medeniyet.edu.tr/tr"

req = requests.get(url).content
soup = BeautifulSoup(req, "lxml")

first = soup.find_all("h3", class_="title")
conn = http.client.HTTPSConnection("api.pushover.net:443")

# Son duyuruyu tutacak dosya
file_path = "son_duyuru.txt"    
if os.path.exists(file_path):
    with open(file_path, "rt") as file:
        x = file.read()
else:
    x = ""

for i in first:
    if i.text == "DUYURULAR":
        duyuru = i.find_next_sibling("div").find("p")
        if x != duyuru.text:
            with open(file_path, "w") as file:
                file.write(duyuru.text)

                conn.request(
                    "POST",
                    "/1/messages.json",
                    urllib.parse.urlencode({
                        "token": "aseio3vnkrsyv6i2szjgen2efddyba",
                        "user": "uiqzb6qk2e3yf81pbn5z8dr55od5wf",
                        "title": "Duyuru!!!",
                        "message": duyuru.text,
                    }),
                    {"Content-type": "application/x-www-form-urlencoded"}
                )
                resp = conn.getresponse()



