from bs4 import BeautifulSoup
import requests

import config
import mongodb

DEBUG = True
DEBUG_GIVEAWAYS = 2

login = "https://metacouncil.com/login/login/"
url = "https://metacouncil.com/giveaway/"
postURL = "https://metacouncil.com/posts/"

credentials = {
    'login': config.login,
    'password': config.password
}


def getWinners(postID):
    giveawayURL = postURL + postID
    postPage = requests.get(giveawayURL)
    postDoc = BeautifulSoup(postPage.text, "html.parser")
    givenGames = postDoc.body.find(
        "article", id="js-post-" + postID).find_all("li", class_="is-delivered")
    for givenGame in givenGames:
        list = givenGame.find_all("ul")
        # Retrieve winner
        game = list[0].find_all("li")[0]  # .find("a")
        winner = list[0].find_all("li")[1].find("a").text.strip()

        print(game.text.strip())


getWinners(str(332990))
