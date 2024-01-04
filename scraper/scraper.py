from bs4 import BeautifulSoup
import requests

import config
import mongodb

DEBUG = True
DEBUG_GIVEAWAYS = 3

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

    #Check if giveaway has ended yet, abort if not ended
    active = postDoc.body.find("article", id="js-post-" + postID).find("div", class_="giveaway-bbCode--countdown")
    if active:
        print("Not ended yet")
        return []

    #Find all games in the giveaway and winners if any
    givenGames = postDoc.body.find(
        "article", id="js-post-" + postID).find_all("li", class_="giveaway-bbCode--prizeItem")
    games = []
    for givenGame in givenGames:
        list = givenGame.find_all("ul")

        # Retrieve game and winner
        num = len(list[0].find_all("li"))
        game = list[0].find_all("li")[0].text.strip()  # .find("a")
        if num > 2:
            winner = list[0].find_all("li")[1].find("a").text.strip()
        else:
            winner = "NONE"
        
        #games.append([game, winner])
        games.append({"game" : game, "winner" : winner})
        #games.append("{'game' : " + game + ", 'winner' : " + winner + "}")
        mongodb.insertWinner(winner, game, giveawayDate)

    return games

# Get games from giveaway
def scrapeGiveaway(id, giveawayDate):  
    givePage = s.get(url + str(id))
    giveDoc = BeautifulSoup(givePage.text, "html.parser")

    #Check first row to see if it's a code column or not
    firstRow = giveDoc.body.find("tr", class_="dataList-row")
    cell = firstRow.find_all("td")
    col = 1
    if cell[1].text.strip() == "Code":
        col = 2

    rows = giveDoc.body.find_all(
        "tr", class_="dataList-row")[1:]

    games = []
    for row in rows:
        cell = row.find_all("td")

        game = cell[0].text.strip()
        platform = cell[col].text.strip()
        mongodb.insertGame(game, platform)
        #games.append(game)

    # Check if giveaway is active
    #active = giveDoc.body.find(string="Enter Giveaway")
    #active = giveDoc.body.find("div", class_="giveaway-bbCode--countdown")
    #print(active)
    #if active:
    #    print("abort")
    #    return games
    # Get winners if the giveaway has ended
    #if not active:
    link = giveDoc.body.find(
        "div", class_="p-title-pageAction").find_all("a")
    # Get Post id
    postID = link[0]["href"].split("/")[2]
    games = getWinners(postID, giveawayDate)
    return games

#Get giveaway post
def getPost(giveaway):
    # Find link to the giveaway
    idLink = giveaway.find(
        "div", class_="structItem-title").find("a")

    # Get the ID from the link
    id = str(idLink).split("/")[2]
    giveawayDate = giveaway.find("time", class_="u-dt")["data-time"]

    #if id != "643":
    #    return

    print(id)
    games = scrapeGiveaway(id, giveawayDate)
    # Get the number of prizes
    prizes = giveaway.find_all("span")
    prizes = giveaway.find(
        "ul", class_="structItem-parts").find_all("li")[2].find("span")
    # print(giveaway['data-author'])

    prize = prizes.text.strip()
    giver = giveaway['data-author']

    numGames = prize.split(" ")[0]
    giveawayID = int(id)

    mongodb.insert(giver, numGames, giveawayID, giveawayDate, games)

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
            getPost(giveaway)

            if DEBUG == True:
                DEBUG_GIVEAWAYS -= 1
                if DEBUG_GIVEAWAYS == 0:
                    break
        i = i + 1

mongodb.process()
