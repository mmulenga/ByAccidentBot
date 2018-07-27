import unittest
import praw
from byaccidentbot import ByAccidentBot
from unittest.mock import patch

class TestByAccidentBot(unittest.TestCase):
  # Need to create two mock objects (praw, firebase) 
  # and then patch them into the init method of ByAccidentBot class
  @classmethod
  def setUpClass(self):
    self.patchPraw = patch('praw.Reddit', autospec=True)
    self.patchFire = patch('firebase.Firebase', autospec=True)

    self.mockPraw = self.patchPraw.start()
    self.mockFire = self.patchFire.start()

    self.bot = ByAccidentBot()
    self.bot.reddit = self.mockPraw
    self.bot.fb = self.mockFire
    self.bot.fb.pull.return_value = dict()


  def test_populateCommentDict(self):
    self.assertEqual(len(self.bot.commentDictionary), 0)
    self.bot.populateCommentDict()
    self.mockFire.pull.assert_called()
  #  self.assertGreater(len(self.bot.commentDictionary), 0)

  #def test_searchForPhrase(self):
  #  self.assertTrue(self.bot.searchForPhrase('on accident'))
  #  self.assertFalse(self.bot.searchForPhrase('not a phrase'))
  
  #@patch('praw.models.Comment')
  #def test_replyToComment(self, MockComment):
  #  mockComment = MockComment(self.bot.reddit)
  #  self.assertTrue(self.bot.replyToComment(mockComment))

  @classmethod
  def tearDownClass(self):
    self.patchPraw.stop()
    self.patchFire.stop()
  
  if __name__ == "__main__":
    unittest.main()
    