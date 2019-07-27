from datetime import datetime

import firebase_admin, json
from firebase_admin import credentials
from firebase_admin import db

from firebase.database import DataBase

db = DataBase().rootReference()

def getCurrentSearch():
    """ Return last search status dict or None if there isn't. """
    return db.child("searchs/current").get()


def discardLast():
    """ Discards the last search storing its status """
    last = getCurrentSearch()
    if last:
        new_key_name = datetime.now().strftime("%y%m%d_%H%M%S")
        db.child("searchs/old/" + new_key_name).set(last)
        db.child("searchs/current").delete()


def setCurrentSearch(search_dict):
    db.child("searchs/current").set(search_dict)


def updateOnlyStatus(current_search):
    only_status = dict(current_search)
    only_status.pop("new_researchers")
    db.child("searchs/current").update(only_status)

def updateCurrentSearch(current_search):
    db.child("searchs/current").update(current_search)

def addNewAuthors(news):
    if news: db.child("searchs/current/new_researchers").update(news)

def getOrganizations():
    return db.child("organizations").get()

def getOrganizationCodes():
    return list(db.child("organizations").get(shallow=True).keys())