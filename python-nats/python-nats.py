# [begin subscribe_json]
# coding=utf-8
import asyncio
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
from pymongo import MongoClient
#from redis import Redis
#from bson import json_util

#Conexion a bases de datos
MONGO_URI = 'mongodb://34.69.77.226:27017' #servidor donde esta la db
client=MongoClient("MONGO_URI")



async def run(loop):
    nc = NATS()

    await nc.connect(servers=["nats://nats:4222"], loop=loop)

    async def message_handler(msg):
        data = json.loads(msg.data.decode())
        insertar(data)

    sid = await nc.subscribe("foo", cb=message_handler)
    await nc.flush()

    #await nc.auto_unsubscribe(sid, 2)
    #await nc.publish("updates", json.dumps({"symbol": "GOOG", "price": 1200 }).encode())
    #await asyncio.sleep(1, loop=loop)
    await nc.close()
# [end subscribe_json]

def insertar(datos):
    db = client['teststore'] #base de datos, si no existe la crea
    collection = db['products'] #coleccion de la base de datos
    #Guardar datos o documentos
    collection.insert_one(datos)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()