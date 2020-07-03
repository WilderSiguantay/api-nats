import asyncio
import os
import signal
import json
import pymongo
import redis
from nats.aio.client import Client as NATS
from pymongo import MongoClient

MONGODB_HOST = '34.69.77.226'
MONGODB_PORT = '27017'
MONGODB_TIMEOUT = 1000
MONGODB_DATABASE = 'Proyecto2MDB'
URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT +  "/"
r=redis(host='104.197.76.93',port=6379)
clave = 'Proyecto2RDB'


try:
    client = pymongo.MongoClient(URI_CONNECTION, serverSelectionTimeoutMS=MONGODB_TIMEOUT)
    client.server_info()
    print ("OK -- Connected to MongoDB at server %s" % (MONGODB_HOST))
except pymongo.errors.ServerSelectionTimeoutError as error:
    print ("Error with MongoDB connection: %s" % error)
except pymongo.errors.ConnectionFailure as error:
    print("Could not connect to MongoDB: %s" % error)

async def run(loop):
    nc = NATS()

    async def closed_cb():
        print("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    options = {
        # "servers": ["nats://127.0.0.1:4222"],
        "servers": ["nats://nats:4222"],
        "loop": loop,
        "closed_cb": closed_cb
    }

    await nc.connect(**options)
    print("Connected to NATS at {nc.connected_url.netloc}...")

    async def subscribe_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        try:
            destination = 'COVID'
            collection = client[MONGODB_DATABASE][destination]
            datos = json.loads(data) # <-- returned data is not string
            collection.insert(datos)
            print(datos)
            r.lpush(clave,datos)
            
            print("Data saved at %s collection in %s database: %s" % (destination, MONGODB_DATABASE, data))
        except Exception as error:
            print("Error saving data: %s" % str(error))
                #Guardar datos o documentos
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        


    # Basic subscription to receive all published messages
    # which are being sent to a single topic 'discover'
    await nc.subscribe("foo", cb=subscribe_handler)

    # Subscription on queue named 'workers' so that
    # one subscriber handles message a request at a time.
    #await nc.subscribe("foo.*", "workers", subscribe_handler)

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()