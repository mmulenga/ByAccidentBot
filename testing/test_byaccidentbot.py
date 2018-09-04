import unittest
import threading
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

  def test_searchForPhrase(self):
    self.assertFalse(self.bot.searchForPhrase('on'))
    self.assertFalse(self.bot.searchForPhrase('53djon accident15'))
    self.assertFalse(self.bot.searchForPhrase('not a phrase'))

    self.assertTrue(self.bot.searchForPhrase('on accident'))
    self.assertTrue(self.bot.searchForPhrase('It was on accident'))
    self.assertTrue(self.bot.searchForPhrase('On aCcident'))
  
  def test_replyToComment(self):
    class FakeComment():
      id = ''
      parent_var = None
      is_root = False
      reply_var = ''

      def __init__(self, x):
        self.id = x

      def reply(self, r):
        self.reply_var = r

      def parent(self):
        return self.parent_var

    fakeParent = FakeComment('test5678')
    fakeParent.is_root = True
    comment = FakeComment('test1234')
    comment.parent_var = fakeParent

    self.bot.commentDictionary['test1234'] = '12:34'
    self.bot.replyToComment(comment)
    del self.bot.commentDictionary['test1234']

    self.bot.commentDictionary['test5678'] = '12:34'
    self.bot.replyToComment(comment)
    del self.bot.commentDictionary['test5678']

    self.bot.replyToComment(comment)
    self.assertNotEqual(comment.reply_var, '')
    self.assertEqual(fakeParent.reply_var, '')
    self.mockFire.push.assert_called()

  @patch('praw.models.Redditor', autospec=True)
  def test_autoDeleteScoreCheck(self, mockAccount):
    self.bot.account = mockAccount
    self.bot.autoDeleteScoreCheck()
    self.bot.account.comments.new.assert_called()

  @classmethod
  def tearDownClass(self):
    self.patchPraw.stop()
    self.patchFire.stop()

    # Stop the timer thread created in autoDeleteScoreCheck.
    threading.enumerate()[1].cancel()
  
  if __name__ == "__main__":
    unittest.main()
    