import unittest
import praw
import re
from byaccidentbot import ByAccidentBot

class TestByAccidentBot(unittest.TestCase):
  def setUp(self):
    self.bot = ByAccidentBot()

  def test_initCommentDict(self):
    self.assertEqual(self.bot.populateCommentDict('fakefile.txt'), None)
    self.assertEqual(len(self.bot.commentDictionary), 0)

    self.bot.populateCommentDict('testing/visitedComments.txt')
    self.assertEqual(len(self.bot.commentDictionary), 1)
    self.assertIn('test', self.bot.commentDictionary)

  def test_searchForPhrase(self):
    self.assertEqual()
  
  def test_replyToComment(self):
    self.assertEqual()
  
  def test_autoDeleteScoreCheck(self):
    self.assertEqual()
  
  if __name__ == "__main__":
    unittest.main()
    