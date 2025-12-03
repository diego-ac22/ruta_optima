from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["ruta_optima_db"]
rutas_col = db["rutas"]
