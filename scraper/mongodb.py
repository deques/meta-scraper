import pymongo
from pymongo import MongoClient
import datetime
dbString = "mongodb://localhost:27017"
client = MongoClient(dbString)

db = client["MetaGiveaway"]
giveaways = db["meta-giveaway"]


def insert(giver, number, giveawayID):
    giveaways.insert_one(
        {"name": giver, "prizes": number, "giveawayID": giveawayID})


def insertUser(user, add):
    if add == "":
        add = 0
    else:
        add = (add)

    users = db["users"]
    count = users.count_documents({"name": user})

    # Add new entry
    if count == 0:
        count = users.insert_one(
            {"name": user, "prizes": int(add), "times": 1})
    # Increase the number
    else:
        # Find the user
        res = users.find_one({"name": user})

        # Reset
        prizes = 0
        times = 0

        # Get the number
        if res["prizes"] != "":
            prizes = res["prizes"]

        if res["times"] != "":
            times = res["times"]

        # Update the entry
        numPrizes = users.update_one(
            {"name": user}, {"$set": {"prizes": int(int(prizes) + int(add)), "times": (times + 1)}})


def insertGame(game, platform):
    game = game.lower()
    games = db["games"]
    count = games.count_documents({"name": game, "platform": platform})

    if int(count) == 0:
        games.insert_one({"name": game, "platform": platform, "times": 1})
    else:
        res = games.find_one({"name": game})

        times = 0

        if res["times"] != "":
            times = res["times"]

        # Update the entry
        # games.update_one({"name": game}, {"$inc": {times: 1}})
        games.update_one({"name": game}, {"$set": {"times": int(times) + 1}})


def process():
    entries = giveaways.find({})
    print("Processing")

    for entry in entries:
        user = entry["name"]
        prizes = entry["prizes"]
        insertUser(user, prizes)


def delete():
    print("Delete")
    giveaways.delete_many({})
    db["users"].delete_many({})
    db["games"].delete_many({})
