import unittest
import time
from firebase import Firebase
from datetime import datetime, timezone

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
    for k, v in self.commentDictionary.items():
      self.fb.push('test_comments', k, v)

  def test_pull(self):
    response = dict()

    for data in self.fb.pull('test_comments'):
      response = data.to_dict()
    
    print(response)

    self.assertIn('e0j9iet', response)
    self.assertEqual(response['timestamp'], datetime(2018, 6, 27, 18, 0, tzinfo=timezone.utc))

    print(type(response['timestamp']) is datetime)
      


if __name__ == "__main__":
  unittest.main()