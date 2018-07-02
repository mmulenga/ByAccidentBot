import praw
import prawcore.exceptions
import re
import threading
import time
from firebase import Firebase
from datetime import datetime, timedelta, timezone

class ByAccidentBot():
  def __init__(self):
    self.commentDictionary = dict()
    self.searchPhrase = re.compile(r'.*\bon accident\b.*', flags=re.I)
    self.reddit = praw.Reddit('byaccidentbot', user_agent='pi:com.bab.byaccidentbot:v1.0.0 by /u/thecrazybandicoot')
    self.account = self.reddit.user.me()
    self.fb = Firebase()

  # Populates the comment dictionary from the provided file.
  # Pre:  A successful connection with Firebase can be established.
  # Post: Success - The dictionary gets populated with comments.
  #       Failure - Error message is printed and method returns.
  def populateCommentDict(self):
    try:
      for item in self.fb.pull('comments'):
        response = item.to_dict()
        self.commentDictionary[response['id']] = response['timestamp']
    except OSError as e:
      print(e)
      print('File not found.')
      return

  # Searches for instances of 'on accident' within the given comment.
  # Pre:  comment - A valid reddit comment.
  # Post: Returns true if a match is found, false otherwise.
  def searchForPhrase(self, comment):
    if self.searchPhrase.match(comment):
      return True
    else:
      return False

  # Replies to the given comment with a pre-written message.
  # Pre:  comment - A valid reddit comment.
  # Post: Replies to the comment with the appropriate reply template.
  def replyToComment(self, comment):
    if comment.id in self.commentDictionary:
      return False
    else:
      ancestor = comment

      while not ancestor.is_root:
        ancestor = ancestor.parent()
        if ancestor.id in self.commentDictionary:
          return False

      try:
        now = datetime.now(timezone.utc)

        # Set the dictionary entry
        self.commentDictionary[comment.id] = now
        # Set the database entry
        self.fb.push('comments', comment.id, now)

        comment.reply('https://gfycat.com/gifs/detail/JointHiddenHummingbird  \nThis is a friendly reminder \
        that it\'s \"by accident\" and not \"on accident\".  \n***** \n^(Downvote to 0 to delete this comment.)')
        
        return True
      except prawcore.exceptions.PrawcoreException as e:
        print(e)
        print('Unable to reply to comment.')
        time.sleep(10)

        return False

  # Automatically deletes any comment that gets downvoted below 0, checking
  # every hour to see if the score has changed.
  # Gives users a method to delete the comment if they dislike it.
  # Pre:  There are valid comments associated with the account.
  # Post: All comments below at or below 0 are deleted.
  def autoDeleteScoreCheck(self):
    threading.Timer(3600.0, self.autoDeleteScoreCheck, []).start()

    for comment in self.account.comments.new(limit=50):
      try:
        if comment.score <= 0:
          comment.delete()
      except prawcore.exceptions.PrawcoreException as e:
        print('Unable to delete comment.')
        time.sleep(60)
  
def main():
  while True:
    try:
      # Initialize the bot.
      bot = None

      while bot == None:
        try:
          bot = ByAccidentBot()
        except prawcore.exceptions.PrawcoreException as e:
          print('Error creating bot instance.')
          time.sleep(60)

      bot.populateCommentDict()
      bot.autoDeleteScoreCheck()

      print('Running...')

      try:
        commentStream = bot.reddit.subreddit('all').stream.comments()
      except prawcore.exceptions.PrawcoreException as e:
        print(e)
        print('Error accessing comment stream.')
        time.sleep(60)

      for comment in commentStream:
        try:
          if bot.searchForPhrase(comment.body):
            bot.replyToComment(comment)
            print('ID: ' + comment.id + ' ' + comment.body)
        except prawcore.exceptions.PrawcoreException as e:
          print(e)
          print('Error connecting to server.')
          time.sleep(60)
    except Exception as e:
      bot.fb.delete()
      print(e)
      print('An error occurred. Restarting the bot...')
      time.sleep(60)
      pass

if __name__ == "__main__":
  main()