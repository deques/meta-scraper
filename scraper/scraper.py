from bs4 import BeautifulSoup
import requests

import config

login = "https://metacouncil.com/login/login/"
url = "https://metacouncil.com/giveaway/"
credentials = {
    'login': config.login,
    'password': config.password
}

with requests.session() as s:
    s.post(login, data=credentials)
    result = s.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    giveaways = doc.body.find_all("div", class_="structItem--giveaway")

    for giveaway in giveaways:
        print(giveaway['data-author'])
    #    giver = giveaway.find("div", class_="structItem-title")
    #    print(giver.text)

""" 

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
giveaways = doc.body.find_all("div")

print(giveaways)

with open("index.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")

tag = doc.find_all("p")
print(tag[0])
"""
