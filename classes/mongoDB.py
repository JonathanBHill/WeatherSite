from pymongo.errors import ConnectionFailure

import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# uri = settings.MONGO_URI

# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


class DatabaseAdmin:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        try:
            self.client.admin.command('ismaster')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
        except ConnectionFailure as e:
            print(e)

    def list_databases(self):
        return self.client.list_database_names()

    def create_database(self, db_name: str):
        self.client[db_name].create_collection('temp_collection')
        self.client[db_name].drop_collection('temp_collection')
        print(f"Database {db_name} created.")

    def delete_database(self, db_name: str):
        self.client.drop_database(db_name)
        print(f"Database {db_name} deleted.")


class CollectionAdmin:
    def __init__(self, db_name):
        self.client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        self.database = self.client[db_name]
        try:
            self.client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
        except ConnectionFailure as e:
            print(e)

    def list_collections(self):
        return self.database.list_collection_names()

    def create_collection(self, collection: str):
        self.database.create_collection(collection)
        print(f"Collection {collection} created in database {self.database.name}.")

    def delete_collection(self, collection: str):
        self.database[collection].drop()
        print(f"Collection {collection} deleted from database {self.database.name}.")


class UserAdmin:
    def __init__(self, db_name):
        self.client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        self.database = self.client[db_name]
        try:
            self.client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
        except ConnectionFailure as e:
            print(e)

    def create_user(self, username: str, password: str, roles: list[dict]):
        self.database.command('createUser', username, pwd=password, roles=roles)
        print(f"User {username} created.")

    def delete_user(self, username: str):
        self.database.command('dropUser', username)
        print(f"User {username} deleted.")


class MongoManager:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI, server_api=ServerApi('1'))
        self.db = self.client.weather
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)


    def insert_one(self, collection: str, data: dict):
        self.db[collection].insert_one(data)

    def insert_many(self, collection: str, data: list[dict]):
        self.db[collection].insert_many(data)

    def find_one(self, collection: str, query: dict):
        return self.db[collection].find_one(query)

    def find_many(self, collection: str, query: dict):
        return self.db[collection].find(query)

    def update_one(self, collection: str, query: dict, data: dict):
        self.db[collection].update_one(query, {'$set': data})

    def update_many(self, collection: str, query: dict, data: dict):
        self.db[collection].update_many(query, {'$set': data})

    def delete_one(self, collection: str, query: dict):
        self.db[collection].delete_one(query)

    def delete_many(self, collection: str, query: dict):
        self.db[collection].delete_many(query)




    def close(self):
        self.client.close()


def main():
    mm = MongoManager()
    print(mm.list_collections())
    mm.close()


if __name__ == "__main__":
    main()
