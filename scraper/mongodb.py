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
        count = users.insert_one({"name": user, "prizes": add, "times": 1})
    # Increase the number
    else:
        res = users.find_one({"name": user})

        # Reset
        prizes = 0
        times = 0

        if res["prizes"] != "":
            prizes = res["prizes"]

        if res["times"] != "":
            times = res["times"]

        numPrizes = users.update_one(
            {"name": user}, {"$set": {"prizes": (int(prizes) + int(add)), "times": (times + 1)}})


def process():
    entries = giveaways.find({})
    print("Test")

    for entry in entries:
        user = entry["name"]
        prizes = entry["prizes"]
        insertUser(user, prizes)


def delete():
    print("Delete")
    giveaways.delete_many({})
    db["users"].delete_many({})
