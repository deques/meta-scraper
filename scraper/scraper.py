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

# Delete old stuff
mongodb.delete()

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
            idLink = giveaway.find(
                "div", class_="structItem-title").find("a")
            x = str(idLink).split("/")
            prizes = giveaway.find_all("span")

            prizes = giveaway.find(
                "ul", class_="structItem-parts").find_all("li")[2].find("span")
            # print(giveaway['data-author'])
            print(prizes)

            prize = prizes.text.strip()
            mongodb.insert(giveaway['data-author'],
                           prize.split(" ")[0], int(x[2]))
        i = i + 1

mongodb.process()
