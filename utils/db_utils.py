import re

from firebase.database import DataBase

""" Utility scripts for database manipulation and maintenance """

def update_scholar_ids_from_researchers_collection():
    """ This function inspects all researchers in the researchers collection,
    looking for those who have scholar profile, adding their reference to the
    scholar_ids collection if it is not added yet """
    db = DataBase()

    res = db.getAllResearchers()
   # scholar_ids = db.getAllScholarIds()

    new_ids = {}

    print(len(res))
    for k,v in res.items():
        if "scholarID" in v:
            id = re.match("(.*)&(.*)", v['scholarID'])
            if id is None:
                print("Error en scholarID de " + k)
            else:
                new_ids[id.group(1)] = k
                print(new_ids[id.group(1)])

    db.updateScholarIds(new_ids)