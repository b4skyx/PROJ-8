from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random
load_dotenv()

mongodbclient_token = os.getenv("DATABASE_CLIENT_URL")

if mongodbclient_token is None:
    try:
        with open('./mongodbclient.0', 'r', encoding='utf-8') as client_url:
            print("Using MongoDB cluster url provided in file")
            cluster = MongoClient(client_url.read())
    except FileNotFoundError:
        print("File not found [mongodbclient.0]")
        print("Neither environment variable nor client file exist")
        print("Abort")
        exit()
else:
    print("Using MongoDB cluster url provided in environment variable..")
    cluster = MongoClient(mongodbclient_token)

db = cluster["proj"]
client_account = db["client_account"]

def db_ping():
    return db.command('ping')

def create_client_account(email: str, password: str):
    account = client_account.find_one({"emailID": email, "password": password})
    if account:
        return account.get("clientID", False)
    else:
        client_id = int(random.uniform(1000000000000, 9999999999999))
        if client_account.find_one({"cliendID": client_id}):
            create_client_account(email=email, password=password)
        else:
            client_account.insert_one({"emailID": email, "password": password, "clientID": client_id})
            return client_id

def set_client_data(client_id, query):
    client_account.update_one({"clientID": client_id}, query)

def get_client_account(email: str, password: str):
    return client_account.find_one({"emailID": email, "password": password})
