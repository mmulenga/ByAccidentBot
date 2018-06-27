import firebase_admin
import google.cloud.firestore_v1beta1
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

class Firebase():
  def __init__(self):
    cred = credentials.Certificate('firebase-credentials.json')
    default_app = firebase_admin.initialize_app(cred)

    self.db = firestore.client()

  def push(self, collection, key, value):
    while True:
      try:
        doc_ref = self.db.collection(collection).document()
        doc_ref.set({
          u'id': key,
          u'timestamp': value
        })
        break
      except Exception:
        print('Error writing to database. Trying again...')
        pass

  def pull(self, collection):
    delta = datetime.now() - timedelta(days=1)
    coll_ref = self.db.collection(collection)
    query = coll_ref.where(u'timestamp', u'>', delta)

    return query.get()
    
