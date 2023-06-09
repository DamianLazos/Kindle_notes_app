# ******************************PYTHON LIBRARIES******************************
import os
# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************
from extensions import MongoDBClient
# ****************************************************************************
client = MongoDBClient(os.getenv("MONGO_URL"), "Kindle")
dbBooks = client.create_collection('booksCollection')
dbNotes = client.create_collection('notesCollection')
