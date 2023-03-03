from bs4 import BeautifulSoup
import requests

import config
import mongodb

login = "https://metacouncil.com/login/login/"
url = "https://metacouncil.com/giveaway/"
credentials = {
    'login': config.login,
    'password': config.password
}

with requests.session() as s:
    s.post(login, data=credentials)
    startPage = s.get(url)

    # Get the giveaway page
    doc = BeautifulSoup(startPage.text, "html.parser")

    # Get the number of pages
    numPages = doc.body.find_all("li", class_="pageNav-page")
    num = int(numPages[4].text.strip())
    i = 1

    # Loop through all the pages
    while i <= num:
        givePage = s.get(url + "?page=" + str(i))
        giveDoc = BeautifulSoup(givePage.text, "html.parser")

        giveaways = giveDoc.body.find_all("div", class_="structItem--giveaway")

        for giveaway in giveaways:
            prizes = giveaway.find_all("span")
            # print(giveaway['data-author'])
            # print(prizes)

            if len(prizes) == 2:
                index = 1
            else:
                index = 0

            prize = prizes[index].text.strip()
            mongodb.insert(giveaway['data-author'], prize.split(" ")[0])
#            print(giveaway['data-author'] + " - " + prize.split(" ")[0])
        i = i + 1
    #    giver = giveaway.find("div", class_="structItem-title")
    #    print(giver.text)
