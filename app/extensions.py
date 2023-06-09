# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from pymongo import MongoClient
# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
class MongoDBClient():
    '''This class is used to create an object with
    connection to a Mongo's Database'''
    def __init__(self, url, db_name) -> object:
        self.client = MongoClient(url)
        self.db = self.client[db_name]
    
    def create_collection(self, collection_name, schema=False):
        '''This method is used to create connection
        to and specific Mongo's database collection 
        if already exist, otherwise creates it'''
        try:
            self.db.create_collection(collection_name)
        except:
            pass
    
        if schema:
            self.db.command('collMod', collection_name, validator=schema)
            
        return self.db[collection_name]
    
    