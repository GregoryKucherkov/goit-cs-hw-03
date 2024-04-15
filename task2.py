from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
import argparse 

config = dotenv_values(".env")


uri = f"mongodb+srv://{config['USER_MDB']}:{config['PASSWORD_MDB']}@goitlearn.t6x1yrg.mongodb.net/?retryWrites=true&w=majority&appName=goitlearn"

# Initialize MongoClient
client = MongoClient(uri, server_api=ServerApi("1"))

# Select database
#db = client.cats
#access to database we created earlier
db = client.test  


parser = argparse.ArgumentParser(description="Add a new cat")

parser.add_argument("--action", help="[create,read, update, delete]")
parser.add_argument("--id", help="[ID of the cat]")
parser.add_argument("--name", help="[Name of the cat]")
parser.add_argument("--age", help="[Age of the cat]")
parser.add_argument("--features", help="[Features of the cat]", nargs="+")

args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]

# read a cat
def read():
    try:
        return list(db.cats.find())
    except Exception as e:
        print("Error retrieving cats:", e)

#create a cat
def create(name, age, features):
    try:
        return db.cats.insert_one({
            "name": name,
            "age": age,
            "features": features
        })
    except Exception as e:
        print("Error creating a cat:", e)

#update a cat
def update(pk, name, age, features):
    try:
        return db.cats.update_one({"_id": ObjectId(pk)}, {"$set": {"name": name, "age": age, "features": features}})
    except Exception as e:
        print("Error updating a cat:", e)

#delete a cat
def delete(pk):
    try:
        return db.cats.delete_one({"_id": ObjectId(pk)})
    except Exception as e:
        print("Error deleting a cat:", e)


if __name__ == "__main__":
    if not action:
        print("Action is required. Please provide --action [create, read, update, delete]")
        exit(1)

    if action == "create":
        if not name or not age or not features:
            print("To create a cat, provide --name, --age, and --features")
            exit(1)
        r = create(name, age, features)
        print(f"New cat created with ID: {r.inserted_id}")

    elif action == "read":
        cats = read()
        if cats:
            for cat in cats:
                print(cat)
        else:
            print("No cats found.")

    elif action == "update":
        if not pk or (not name and not age and not features):
            print("To update a cat, provide --id and at least one of --name, --age, or --features")
            exit(1)
        r = update(pk, name, age, features)
        print(f"Updated {r.modified_count} cat(s).")

    elif action == "delete":
        if not pk:
            print("To delete a cat, provide --id")
            exit(1)
        r = delete(pk)
        print(f"Deleted {r.deleted_count} cat(s).")

    else:
        print("Invalid action. Please provide one of [create, read, update, delete]")
