from pymongo import MongoClient, errors

def conectar_mongo():
    try:
        client = MongoClient(
            "mongodb+srv://myAtlasDBUser:AvYTTPKntGncmQqi@myatlasclusteredu.xwouxsq.mongodb.net/?retryWrites=true&w=majority",
            serverSelectionTimeoutMS=3000
        )
        client.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB Atlas.")
        return client
    except errors.PyMongoError:
        print(f"❌ Error al conectar a MongoDB")
        return None
    