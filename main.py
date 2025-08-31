import os
import requests
from bs4 import BeautifulSoup
import http.client, urllib

url = "https://medeniyet.edu.tr/tr"

req = requests.get(url).content
soup = BeautifulSoup(req, "lxml")

first = soup.find_all("div", class_="media-body")
conn = http.client.HTTPSConnection("api.pushover.net:443")

# Son duyuruyu tutacak dosya
file_path = "son_duyuru.txt"
if os.path.exists(file_path):
    with open(file_path, "rt", encoding="utf-8") as file:
        x = file.read()
else:
    x = ""

a = 0
for i in first:
    a += 1
    if 21 <= a <= 24:
        duyuru = i.find("p")
        if a == 21 and duyuru:
            if x != duyuru.text:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(duyuru.text)

                conn.request(
                    "POST",
                    "/1/messages.json",
                    urllib.parse.urlencode({
                        "token": os.getenv("PUSHOVER_TOKEN"),
                        "user": os.getenv("PUSHOVER_USER"),
                        "title": "Duyuru!!!",
                        "message": duyuru.text,
                        "url": "",
                        "priority": "0"
                    }),
                    {"Content-type": "application/x-www-form-urlencoded"}
                )
                conn.getresponse()
