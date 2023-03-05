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


def scrapeGiveaway(id):  # Get games from giveaway
    givePage = s.get(url + str(id))
    giveDoc = BeautifulSoup(givePage.text, "html.parser")
    rows = giveDoc.body.find_all(
        "tr", class_="dataList-row")[1:]

    for row in rows:
        cell = row.find("td")

        game = cell.text.strip()
        mongodb.insertGame(game)


# Delete old stuff
mongodb.delete()

# Login
with requests.session() as s:
    s.post(login, data=credentials)
    startPage = s.get(url)

    # Get the giveaway page
    doc = BeautifulSoup(startPage.text, "html.parser")

    # Get the number of pages
    numPages = doc.body.find_all("li", class_="pageNav-page")
    num = int(numPages[4].text.strip())
    i = 1

    # num = 1  # temp variable, remove
    # Loop through all the pages
    while i <= num:
        givePage = s.get(url + "?page=" + str(i))
        giveDoc = BeautifulSoup(givePage.text, "html.parser")

        giveaways = giveDoc.body.find_all("div", class_="structItem--giveaway")

        for giveaway in giveaways:
            # Find link to the giveaway
            idLink = giveaway.find(
                "div", class_="structItem-title").find("a")

            # Get the ID from the link
            id = str(idLink).split("/")[2]
            print(id)
            scrapeGiveaway(id)

            # Get the number of prizes
            prizes = giveaway.find_all("span")
            prizes = giveaway.find(
                "ul", class_="structItem-parts").find_all("li")[2].find("span")
            # print(giveaway['data-author'])

            prize = prizes.text.strip()
            mongodb.insert(giveaway['data-author'],
                           prize.split(" ")[0], int(id))
        i = i + 1

mongodb.process()
