from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from dotenv import dotenv_values
import argparse 

config = dotenv_values(".env")

uri = f"mongodb+srv://{config['USER_MDB']}:{config['PASSWORD_MDB']}@goitlearn.t6x1yrg.mongodb.net/?retryWrites=true&w=majority&appName=goitlearn"

# Initialize MongoClient
client = MongoClient(uri, server_api=ServerApi("1"))

# Select database
# db = client.cats
# access to database we created earlier
db = client.test  

parser = argparse.ArgumentParser(description="Manage cats")

parser.add_argument("--action", help="[create, read, update, delete, delete_all]")
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

# Create a cat
def create(name, age, features):
    try:
        return db.cats.insert_one({
            "name": name,
            "age": age,
            "features": features
        })
    except Exception as e:
        print("Error creating a cat:", e)

# Read a cat
def read(name=None):
    try:
        if name:
            cats = list(db.cats.find({"name": name}))
            return cats
        else:
            return list(db.cats.find())
    except Exception as e:
        print("Error retrieving cats:", e)



def update(name, age=None, features=None):
    try:
        update_data = {}
        if age is not None:
            update_data["age"] = age
        if features is not None:
            update_data["features"] = features

        if update_data:
            return db.cats.update_one({"name": name}, {"$set": update_data})
        else:
            print("No update parameters provided.")
    except Exception as e:
        print("Error updating a cat:", e)



# Delete a cat by name
def delete(name):
    try:
        return db.cats.delete_one({"name": name})
    except Exception as e:
        print("Error deleting a cat:", e)

# Delete all cats
def delete_all():
    try:
        return db.cats.delete_many({})
    except Exception as e:
        print("Error deleting cats:", e)

        

if __name__ == "__main__":
    if not action:
        print("Action is required. Please type in: py task2.py --action [read, create, update, delete]")
        exit(1)

    if action == "create":
        if not name or not age or not features:
            print("To create a cat, type in: py task2.py --action <actiom> --name <Name> --age <age> --features <features>")
            exit(1)
        r = create(name, age, features)
        print(f"New cat created with ID: {r.inserted_id}")

    elif action == "read":
        if name:
            cat = read(name)
            if cat:
                print(cat)
            else:
                print('No such cat')
        else:
            cats = read()
            if cats:
                for cat in cats:
                    print(cat)
            else:
                print("No cats found.")


    elif action == "update":
        if not name or (not age and not features):
            print("To update a cat use:py task2.py --action update --name <name> and at least one --age <age> --features <'features'>")
            exit(1)
        r = update(name, age, features)
        print(f"Updated {r.modified_count} cat(s).")


    elif action == "delete":
        if not name:
            print("To delete a cat, use: --action --delete --name <name>")
            exit(1)
        r = delete(name)
        print(f"Deleted {r.deleted_count} cat(s).")

    elif action == "delete_all":
        confirmation = input("Are you sure you want to delete all cats? (yes/no): ")
        if confirmation.lower() == "yes":
            r = delete_all()
            print(f"Deleted {r.deleted_count} cat(s).")
        else:
            print("Delete all operation aborted.")

    else:
        print("Invalid action. Please provide one of: [create, read, update_age, update_features, delete, delete_all]")

