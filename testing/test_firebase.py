import unittest
import time
from firebase import Firebase

class TestFirebase(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.fb = Firebase()
    self.commentDictionary = dict()

    try:
      with open('testing/visitedComments.txt', 'r') as visitedFile:
        for line in visitedFile:
          key, value = line.split(' ')
          self.commentDictionary[key] = value
    except OSError:
      print('File not found.')
      return

  def test_push(self):
    for comment in self.commentDictionary.items():
      self.fb.push(comment)

  def test_pull(self):
    data = self.fb.pull()

    for item in data.each():
      print(item.val())

  @classmethod
  def tearDownClass(self):
    for comment in self.commentDictionary.items():
      self.fb.db.child('comments').child(comment[0]).remove()

if __name__ == "__main__":
  unittest.main()