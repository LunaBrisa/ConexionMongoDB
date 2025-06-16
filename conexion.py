from pymongo import MongoClient, errors

def conectar_mongo():
    try:
        client = MongoClient(
            "mongodb+srv://myAtlasDBUser:AvYTTPKntGncmQqi@myatlasclusteredu.xwouxsq.mongodb.net/?retryWrites=true&w=majority",
            serverSelectionTimeoutMS=3000
        )
        client.server_info()
        print("✅ Conexión exitosa a MongoDB Atlas.")
        return client
    except errors.ServerSelectionTimeoutError as e:
        print("❌ Error de conexión:", e)
        return None
