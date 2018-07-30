import firebase_admin
import google.cloud.firestore_v1beta1
from firebase_admin import firestore, credentials
from datetime import datetime, timedelta

class Firebase():
  def __init__(self):
    self.cred = credentials.Certificate('firebase-credentials.json')
    self.default_app = firebase_admin.initialize_app(self.cred)
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
      except Exception as e:
        print(e)
        print('Error writing to database. Trying again...')
        pass

  def pull(self, collection):
    while True:
      try:
        delta = datetime.now() - timedelta(days=1)
        coll_ref = self.db.collection(collection)
        query = coll_ref.where(u'timestamp', u'>', delta)
        break
      except Exception as e:
        print(e)
        print('Error reading from database. Trying again...')
        pass

    return query.get()

  def pullAll(self, collection):
    while True:
      try:
        coll_ref = self.db.collection(collection)
        query = coll_ref.order_by(u'timestamp', direction=firestore.Query.ASCENDING)
        break
      except Exception as e:
        print(e)
        print('Error reading from database. Trying again...')
        
    return query.get()

  def delete(self):
    firebase_admin.delete_app(self.default_app)
    
