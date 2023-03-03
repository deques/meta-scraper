import pymongo
from pymongo import MongoClient
import datetime
dbString = "mongodb://localhost:27017"
client = MongoClient(dbString)

db = client["MetaGiveaway"]
giveaways = db["meta-giveaway"]


def insert(giver, number):
    giveaways.insert_one({"name": giver, "prizes": number})


def insertUser(user, add):
    if add == "":
        add = 0
    users = db["users"]
    count = users.count_documents({"name": user})
    # print(user)
    if count == 0:
        count = users.insert_one({"name": user, "prizes": add})
    else:
        res = users.find_one({"name": user})

        num = 0
        if res["prizes"] != "":
            num = res["prizes"]
        numPrizes = users.update_one(
            {"name": user}, {"$set": {"prizes": (int(num) + int(add))}})


def process():
    entries = giveaways.find({})

    for entry in entries:
        user = entry["name"]
        prizes = entry["prizes"]
        insertUser(user, prizes)


# giveaways.delete_many({})

db["users"].delete_many({})
process()
