from bs4 import BeautifulSoup
import requests

import config
import mongodb

DEBUG = False
DEBUG_GIVEAWAYS = 10

login = "https://metacouncil.com/login/login/"
url = "https://metacouncil.com/giveaway/"
postURL = "https://metacouncil.com/posts/"

credentials = {
    'login': config.login,
    'password': config.password
}


def getWinners(postID, giveawayDate):
    giveawayURL = postURL + postID
    postPage = requests.get(giveawayURL)
    postDoc = BeautifulSoup(postPage.text, "html.parser")
    givenGames = postDoc.body.find(
        "article", id="js-post-" + postID).find_all("li", class_="is-delivered")
    for givenGame in givenGames:
        list = givenGame.find_all("ul")
        # Retrieve winner
        game = list[0].find_all("li")[0].text.strip()  # .find("a")
        winner = list[0].find_all("li")[1].find("a").text.strip()

        mongodb.insertWinner(winner, game, giveawayDate)


def scrapeGiveaway(id, giveawayDate):  # Get games from giveaway
    givePage = s.get(url + str(id))
    giveDoc = BeautifulSoup(givePage.text, "html.parser")
    rows = giveDoc.body.find_all(
        "tr", class_="dataList-row")[1:]

    for row in rows:
        cell = row.find_all("td")

        game = cell[0].text.strip()
        platform = cell[1].text.strip()
        mongodb.insertGame(game, platform)

    # Check if giveaway is active
    active = giveDoc.body.find(string="Enter Giveaway")

    # Get winners if the giveaway has ended
    if not active:
        link = giveDoc.body.find(
            "div", class_="p-title-pageAction").find_all("a")
        # Get Post id
        postID = link[0]["href"].split("/")[2]
        getWinners(postID, giveawayDate)


# Delete old stuff
mongodb.delete()

# Login
with requests.session() as s:
    s.post(login, data=credentials)
    startPage = s.get(url)

    # Get the giveaway page
    doc = BeautifulSoup(startPage.text, "html.parser")

    # Get the number of pages
    num = doc.body.find_all("li", class_="pageNav-page")
    numPages = int(num[4].text.strip())
    i = 1

    if DEBUG == True:
        numPages = 1  # Debugging, only check first page

    # Loop through all the pages
    while i <= numPages:
        givePage = s.get(url + "?page=" + str(i))
        giveDoc = BeautifulSoup(givePage.text, "html.parser")

        giveaways = giveDoc.body.find_all("div", class_="structItem--giveaway")

        for giveaway in giveaways:
            # Find link to the giveaway
            idLink = giveaway.find(
                "div", class_="structItem-title").find("a")

            # Get the ID from the link
            id = str(idLink).split("/")[2]
            giveawayDate = giveaway.find("time", class_="u-dt")["data-time"]

            print(id)
            scrapeGiveaway(id, giveawayDate)

            # Get the number of prizes
            prizes = giveaway.find_all("span")
            prizes = giveaway.find(
                "ul", class_="structItem-parts").find_all("li")[2].find("span")
            # print(giveaway['data-author'])

            prize = prizes.text.strip()
            giver = giveaway['data-author']
            numGames = prize.split(" ")[0]
            giveawayID = int(id)

            mongodb.insert(giver, numGames, giveawayID, giveawayDate)

            if DEBUG == True:
                DEBUG_GIVEAWAYS -= 1
                if DEBUG_GIVEAWAYS == 0:
                    break
        i = i + 1

mongodb.process()
