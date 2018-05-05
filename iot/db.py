import iot
import flask
import pymongo
import datetime

DESCENDING = pymongo.DESCENDING
ASCENDING = pymongo.ASCENDING


def get():
    """Get database instance"""
    db = getattr(flask.g, '_database', None)
    if db is None:
        client = flask.g._mongoclient = pymongo.MongoClient(iot.app.config['MONGO_URI'])
        db = flask.g._database = client[iot.app.config['MONGO_DB']]
    return db


def num_collections():
    """Get number of collections in db defined in config"""
    return len(collection_names())


def collection_names():
    """Get names of all collections except settings collection"""
    return [n for n in get().collection_names() if n != 'settings']


def add_record(collection, data):
    """Add a document to a collection"""
    if 'timestamp' in data.keys():
        raise ValueError("Timestamp must not be specified.")
    data['timestamp'] = datetime.datetime.now()
    return get()[collection].insert_one(data)
