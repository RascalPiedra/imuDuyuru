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

# Telegram bilgileri
TOKEN = "8235702458:AAF2-W00mhcWkpMvL2NLz6wswsu1F5eZDGM"
CHAT_ID = "duyurularformee"

#Duyuruyu Arama
for i in first:
    if i.text == "DUYURULAR":
        duyuru = i.find_next_sibling("div").find("p")
        if x != duyuru.text:
            with open(file_path, "w") as file:
                file.write(duyuru.text)
        
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=@{CHAT_ID}&text={duyuru.text}"
                try:
                    r = requests.post(url)
                except Exception as e:
                    print("Telegram mesajı gönderilemedi:", e)
