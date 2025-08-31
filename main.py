from time import sleep as delay
from bs4 import BeautifulSoup
import http.client, urllib
import requests



url = "https://medeniyet.edu.tr/tr"



while True:
    req =  requests.get(url).content
    soup = BeautifulSoup(req, "lxml")

    first = soup.find_all("div", class_="media-body")

    conn = http.client.HTTPSConnection("api.pushover.net:443")


    a = 0

    try:
        file = open("son_duyuru.txt", "rt")
        x = file.read()
        file.close()
    except:
        x = ""
    finally:
        print(x)

    print("-----------------------------------------DUYURULAR-----------------------------------------")
    for i in first:
        a += 1
        if a >= 21 and a <= 24:
            duyuru = i.find("p")
            print(duyuru.text)
            if a == 21:
                    if x == duyuru.text:
                        print("---Zaten duyuru bu.")
                        with open("son_duyuru.txt", "w") as file:
                            file.write(x)
                    else:
                        x = duyuru.text
                        print("---Yeni Duyuru!!!")
                        with open("son_duyuru.txt", "w") as file:
                            file.write(x)
                        conn.request("POST", "/1/messages.json",
                                     urllib.parse.urlencode({
                                         "token":"aseio3vnkrsyv6i2szjgen2efddyba",
                                         "user":"uiqzb6qk2e3yf81pbn5z8dr55od5wf",
                                         "title":"Duyuru!!!",
                                         "message": x,
                                         "url":"",
                                         "priority":"0"
                                     }), {"Content-type":"application/x-www-form-urlencoded"})
                        conn.getresponse()




delay(60)



