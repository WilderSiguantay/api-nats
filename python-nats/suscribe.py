import asyncio
import os
import signal
from nats.aio.client import Client as NATS
from pymongo import MongoClient
MONGO_URI = 'mongodb://34.69.77.226:27017' #servidor donde esta la db

client = MongoClient(MONGO_URI) #nos devuelve un objeto llamado cliente, el cursor o la conexion


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
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        db = client['teststore'] #base de datos, si no existe la crea
        collection = db['products'] #coleccion de la base de datos
        #Guardar datos o documentos
        collection.insert_one( {"Nombre":"Ramon Entro","Departamento":"Huehuetenango","Edad":"","Forma de contagio":"Comunitario","Estado":"Activo"})


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