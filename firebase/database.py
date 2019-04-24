import firebase_admin, json
from firebase_admin import credentials
from firebase_admin import db



class DataBase:
    def __init__(self, cred='./credentials.json', endpoint='INTRODUCE_ENDPOINT', ref='/'):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate(cred)
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://'+endpoint+'.firebaseio.com/'
        })

        self.db = db.reference(ref)
    

    def getAllResearchers(self):
        return self.db.child('researchers').get()

    def addResearcher(self, researcher):
        return self.db.child('researchers/'+researcher.crisid).set(researcher.to_dict())



