import os
import pika
import requests
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
print(f"Connecting to rabbitmq({rabbitMQHost})")

rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()
rabbitMQChannel.queue_declare(queue='toFirebaseSave')

cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spotifyplaylistgenerator-48abb-default-rtdb.firebaseio.com/'
})

print(' [*] Waiting for sentiment analysis requests. To exit press CTRL+C')

def callback(ch, method, properties, body):
    jsonRest = pickle.loads(body)
    ref = db.reference('/')
    user_ref = ref.child(jsonRest['user'])
    playlistName = None
    if user_ref.get() == None:
        playlistName = "playlist1"
        ref.set({
            jsonRest['user'] : {
                playlistName : jsonRest['playlist']
            }
        })
    else:
        numPlaylists = len(list(user_ref.get().keys()))
        playlistName = "playlist" + str(numPlaylists + 1)
        user_ref.update({
            playlistName : jsonRest['playlist']
        })

    print(" [x] {}:{}".format(method.routing_key, jsonRest['callback']))
    if "callback" in jsonRest:
        url = jsonRest["callback"]["url"]
        data = jsonRest["callback"]["data"]
        try:
            r = requests.post(url, data=data)
        except requests.exceptions.ConnectionError:
            print("Connection refused")

rabbitMQChannel.basic_consume(queue='toFirebaseSave', on_message_callback=callback, auto_ack=True)
rabbitMQChannel.start_consuming()