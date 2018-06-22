import pyrebase

class Firebase():
  def __init__(self):
    self.config = {
      'apiKey': 'AIzaSyAQSB_SGUlHEeEVCY2YSLmjk7vystNOOsI',
      'authDomain': 'byaccidentbot.firebaseapp.com',
      'databaseURL': 'https://byaccidentbot.firebaseio.com',
      'projectId': 'byaccidentbot',
      'storageBucket': 'byaccidentbot.appspot.com',
      'serviceAccount': 'firebase-credentials.json'
    }

    self.firebase = pyrebase.initialize_app(self.config)
    self.db = self.firebase.database()

  def push(self, data):
    comments = self.db.child('comments').child(data[0]).set(data)

  def pull(self):
    return self.db.child('comments').get()

  def stream(self, handler):
    return self.db.child('comments').stream(handler)

  def streamHandler(self, message):
    print(message["event"])
    print(message["path"])
    print(message["data"])
