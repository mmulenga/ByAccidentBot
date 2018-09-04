import unittest
import sys
from firebase import Firebase
from datetime import datetime, timezone
from unittest.mock import patch

class TestFirebase(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.fire = Firebase()

    self.patchFirestore = patch('firebase_admin.firestore', autospec=True)
    self.patchCredentials = patch('firebase_admin.credentials', autospec=True)

    self.mockFirestore = self.patchFirestore.start()
    self.mockCredentials = self.patchCredentials.start()

    self.store = self.mockFirestore
    self.credential = self.mockCredentials

    self.fire.cred = self.credential
    self.fire.db = self.store.client()

    self.commentDictionary = dict()
    self.commentDictionary['e0j9iet'] = datetime(2018, 6, 27, 18, 0, tzinfo=timezone.utc)

  def test_push(self):
    for k, v in self.commentDictionary.items():
      self.fire.push('test_comments', k, v)

  def test_pull(self):
    response = dict()

    for data in self.fire.pull('test_comments'):
      response = data.to_dict()

      
  @classmethod
  def tearDownClass(self):
    self.patchFirestore.stop()
    self.patchCredentials.stop()

if __name__ == "__main__":
  unittest.main()