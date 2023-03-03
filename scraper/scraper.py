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
        prizes = giveaway.find_all("span")
        #print(giveaway['data-author'])
        #print(prizes)

        if len(prizes) == 2:
            i = 1
        else:
            i = 0
        
        prize = prizes[i].text.strip()
        print(giveaway['data-author'] + " - " + prize)
    #    giver = giveaway.find("div", class_="structItem-title")
    #    print(giver.text)
