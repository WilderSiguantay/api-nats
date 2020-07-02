from pymongo import MongoClient

MONGO_URI = 'mongodb://34.69.77.226:27017' #servidor donde está la db

client = MongoClient(MONGO_URI) #nos devuelve un objeto llamado cliente, el cursor o la conexion
db = client['teststore'] #base de datos, si no existe la crea
collection = db['products'] #coleccion de la base de datos
#Guardar datos o documentos
collection.insert_one( {"Nombre":"Ramon Puertas","Departamento":"Huehuetenango","Edad":"","Forma de contagio":"Comunitario","Estado":"Activo"})

