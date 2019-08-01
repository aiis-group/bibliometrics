import os

import firebase_admin, json
from firebase_admin import credentials
from firebase_admin import db

class DataBase:
    __instance = None     # Singleton pattern.

    def __new__(cls):
        if DataBase.__instance is None:
            DataBase.__instance = object.__new__(cls)
        return DataBase.__instance

    def __init__(self, cred='./credentials.json',
                       endpoint='bibliometrics-86d67', ref='/'):

        if hasattr(self, 'db'):
            # If __new__ returns an instance of DataBase (new or not)
            # __init__ is called. This prevents multiple inits.
            return

        #  s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])

        # Fetch the service account key JSON file contents

        cred = credentials.Certificate(
            cred if os.path.exists(cred)
            else json.loads(os.environ["firebase_api_key"])
        )
            
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://'+endpoint+'.firebaseio.com/'
        })

        self.db = db.reference(ref)
        self.researchers = None

    def rootReference(self):
        return self.db
    
    def updateResearcher(self, researcher):
        return self.db.child('researchers/'+researcher.crisid).update(researcher.to_dict())
    
    def getResearcher(self, crisID):
        return self.db.child('researchers/'+crisID).get()

    def getAllScholarIds(self):
        return db.reference("scholarIds").get()


    # Legacy.
    def getAllResearchers(self):
        if self.researchers is None:
            self.researchers = self.db.child('researchers').get()

        return self.researchers

    def addResearcher(self, researcher):
        return self.db.child('researchers/'+researcher.crisid).set(researcher.to_dict())

    def updateScholarIds(self, newIDs):
        return self.db.child('scholarIds').update(newIDs)

    def updateResearchers(self, newRes):
        return self.db.child('researchers').update(newRes)

