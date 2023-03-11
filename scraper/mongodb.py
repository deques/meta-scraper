import pymongo
from pymongo import MongoClient
import datetime
dbString = "mongodb://localhost:27017"
client = MongoClient(dbString)

db = client["MetaGiveaway"]


def combine():
    users = db["users"]
    winners = db["winners"]

    result = winners.find({})
    for user_in_winner in result:
        username = user_in_winner["name"]
        times = user_in_winner["giveaways"]

        count = users.count_documents({"name": username})
        if count == 0:
            users.insert_one({"name": username})
        else:
            users.update_one({"name": username}, {
                             "$set": {"won-games": times}})


def insertWinner(winner, game, giveawayDate):
    winners = db["users"]
    count = winners.count_documents({"name": winner})

    winner_games = db["winner-game"]
    winner_games.insert_one(
        {"name": winner, "game": game, "give_date": giveawayDate})

    if count == 0:
        winners.insert_one({"name": winner, "won_games": 1,
                           "giveaways": 0, "given_games": 0})
    else:
        # Find the user
        res = winners.find_one({"name": winner})
        times = res["won_games"]

        # Update
        winners.update_one(
            {"name": winner}, {"$set": {"won_games": (times + 1)}})


def insert(giver, number, giveawayID, giveawayDate):
    giveaways = db["meta-giveaway"]
    giveaways.insert_one(
        {"name": giver, "given_games": number, "giveawayID": giveawayID, "give_date": giveawayDate})


def insertUser(user, add):

    users = db["users"]
    count = users.count_documents({"name": user})

    # Add new entry
    if count == 0:
        count = users.insert_one(
            {"name": user, "given_games": int(add), "giveaways": 1})
    # Increase the number
    else:
        # Find the user
        res = users.find_one({"name": user})

        # Reset
        prizes = 0
        times = 0

        # Get the number
        if res["given_games"] != "":
            prizes = res["given_games"]

        if res["giveaways"] != "":
            times = res["giveaways"]

        # Update the entry
        numPrizes = users.update_one(
            {"name": user}, {"$inc": {"given_games": int(add), "giveaways": 1}})


def insertGame(game, platform):
    game = game.lower()
    games = db["games"]
    count = games.count_documents({"name": game, "platform": platform})

    if int(count) == 0:
        games.insert_one({"name": game, "platform": platform, "giveaways": 1})
    else:
        res = games.find_one({"name": game})

        times = 0

        if res["giveaways"] != "":
            times = res["giveaways"]

        # Update the entry
        # games.update_one({"name": game}, {"$inc": {times: 1}})
        games.update_one({"name": game}, {
                         "$set": {"giveaways": int(times) + 1}})


def process():
    giveaways = db["meta-giveaway"]
    entries = giveaways.find({})
    print("Processing")

    for entry in entries:
        user = entry["name"]
        prizes = entry["given_games"]
        insertUser(user, prizes)


def delete():
    print("Delete")
    db["meta-giveaway"].delete_many({})
    db["users"].delete_many({})
    db["games"].delete_many({})
    db["winner-game"].delete_many({})
