import os
import requests
from bs4 import BeautifulSoup

url = "https://medeniyet.edu.tr/tr"

req = requests.get(url).content
soup = BeautifulSoup(req, "lxml")

first = soup.find_all("h3", class_="title")

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

def sendMessage(message:str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=@{CHAT_ID}&text={message}"
    try:
        requests.post(url)
    except Exception as e:
        print("Telegram mesajı gönderilemedi:", e)

#Duyuru Link
def duyuruLink(duyuru, bolumDuyurusuMu):
    if bolumDuyurusuMu:
        mainURL = "https://muhendislikdogabilimleri.medeniyet.edu.tr/tr/duyurular/"
    else:
        mainURL = "https://medeniyet.edu.tr/tr/duyurular/"
    duyuru = duyuru.replace("İ","i")
    duyuru = duyuru.lower()
    duyuru = duyuru.replace("ı", "i")
    duyuru = duyuru.replace("ü", "u")
    duyuru = duyuru.replace("ö", "o")
    duyuru = duyuru.replace("ş", "s")
    duyuru = duyuru.replace("ğ", "g")
    duyuru = duyuru.replace("ç", "c")
    duyuru = duyuru.replace(" ", "-")
    duyuru = duyuru.replace("!", "")
    duyuru = duyuru.replace("(", "")
    duyuru = duyuru.replace(")", "")
    duyuru = duyuru.replace("/", "")
    while True:
        if duyuru[-1] == '-': duyuru = duyuru[:-1]
        else: break
    return mainURL+duyuru

#Duyuruyu Arama(imü)
for i in first:
    if i.text == "DUYURULAR":
        duyuru = i.find_next_sibling("div").find("p")
        if x != duyuru.text:
            with open(file_path, "w") as file:
                file.write(duyuru.text)
                link = duyuruLink(duyuru.text, False)

                sendMessage("------imü duyuru------\n" + duyuru.text + "\n" + link)

#Bölümün Duyurusu
url = "https://bm.medeniyet.edu.tr/tr"
request = requests.get(url).content
soup1 = BeautifulSoup(request, "lxml")
bul = soup1.find("div", class_="tab-container vertical vertical-tab tab-small-height")
p = bul.find("p")
with open("son_bolum_duyurusu.txt", "rt") as f:
    if f.read() != p.text:
        f.close()
        with open("son_bolum_duyurusu.txt", "wt") as f:
            f.write(p.text)
            f.close()

            link = duyuruLink(p.text, True)

            
            sendMessage("-----bilgisayar duyuru-----\n" + p.text + "\n" + link)
