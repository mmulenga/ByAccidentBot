import unittest
import praw
import re
from byaccidentbot import ByAccidentBot

class TestByAccidentBot(unittest.TestCase):
  def setUp(self):
    self.bot = ByAccidentBot()

  # Tests the regular expression to see what types of matches it comes up with
  # Pre: file - A valid text file containing test phrases.
  # Post: Output of all phrases matching the regex pattern.
  ##  self.assertTrue()

  def test_initCommentDict(self):
    with self.assertRaises(OSError):
      self.bot.populateCommentDict('fakefile.txt')

    self.assertEqual(len(self.bot.commentDictionary), 0)
    self.bot.populateCommentDict('testing/visitedComments.txt')
    self.assertEqual(len(self.bot.commentDictionary), 1)
    self.assertIn('test', self.bot.commentDictionary)
  
  if __name__ == "__main__":
    unittest.main()
    