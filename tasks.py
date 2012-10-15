from celery import Celery

from mongoengine import Document, StringField, DateTimeField, connect

import os
import datetime
import requests


class Entry(Document):
    name = StringField()
    zip = StringField()
    timestamp = DateTimeField()

celery = Celery('tasks', broker='amqp://guest@localhost//')
connect("mempyflaskcelery")

@celery.task
def lookup(entry_id):
    entry = Entry.objects(id=entry_id)[0]
    url = "http://ws.geonames.org/postalCodeLookupJSON?postalcode=%s&country=US" % entry.zip
    data = requests.get(url).json
    the_name = data['postalcodes'][0]['placeName']

    entry.name = the_name
    entry.save()