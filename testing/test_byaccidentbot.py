import unittest
import praw
from byaccidentbot import ByAccidentBot
from unittest.mock import patch

class TestByAccidentBot(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.bot = ByAccidentBot()

  def test_initCommentDict(self):
    self.assertEqual(len(self.bot.commentDictionary), 0)

    self.bot.populateCommentDict()
    self.assertGreater(len(self.bot.commentDictionary), 0)

  def test_searchForPhrase(self):
    self.assertTrue(self.bot.searchForPhrase('on accident'))
    self.assertFalse(self.bot.searchForPhrase('not a phrase'))
  
  #@patch('praw.models.Comment')
  #def test_replyToComment(self, MockComment):
  #  mockComment = MockComment(self.bot.reddit)
  #  self.assertTrue(self.bot.replyToComment(mockComment))
  
  if __name__ == "__main__":
    unittest.main()
    