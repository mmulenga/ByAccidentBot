import praw
import prawcore.exceptions
import re
import threading
import time
from datetime import datetime, timedelta

class ByAccidentBot():
  def __init__(self):
    self.commentDictionary = dict()
    self.searchPhrase = re.compile(r'.*\bon accident\b.*', flags=re.I)
    self.reddit = praw.Reddit('byaccidentbot', user_agent='pi:com.bab.byaccidentbot:v1.0.0 by /u/thecrazybandicoot')
    self.account = self.reddit.user.me()

  # Populates the comment dictionary from the provided file.
  # Pre:  filename - A file name of a valid txt file.
  # Post: Success - The dictionary gets populated with comments.
  #       Failure - Error message is printed and method returns.
  def populateCommentDict(self, filename):
    try:
      with open(filename, 'r') as visitedFile:
        for line in visitedFile:
          key, value = line.split(' ')
          self.commentDictionary[key] = value
    except OSError:
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
        comment.reply('https://gfycat.com/gifs/detail/JointHiddenHummingbird  \nThis is a friendly reminder \
        that it\'s \"by accident\" and not \"on accident\".  \n***** \n^(Downvote to 0 to delete this comment.)')
        
        self.commentDictionary[comment.id] = datetime.strftime(datetime.now(), '%d/%m/%y::%H:%M:%S')

        try:
          with open('visited.txt', 'a') as visitedFile:
            visitedFile.write(comment.id + ' ' + self.commentDictionary.get(comment.id) + '\n')
        except OSError:
          print('File not found.')
          return False

        return True
      except prawcore.exceptions.PrawcoreException:
        print('Unable to reply to comment.')
        time.sleep(60)
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
      except prawcore.exceptions.PrawcoreException:
        print('Unable to delete comment.')
        time.sleep(60)
  
  # Clear all comments within the 'visited' file that are older than a day old.
  # Pre: 'visited' is a valid text file.
  # Post: All comments older than a day are deleted.
  def autoClearVisitedComments(self):
    threading.Timer(86400.0, self.autoClearVisitedComments, []).start()
    visitedDictionary = dict()

    try:
      with open('visited.txt', 'r') as visitedFile:
        for line in visitedFile:
          comment, time = line.split(' ')
          dt = datetime.strptime(time.strip(), '%d/%m/%y::%H:%M:%S')
          
          if datetime.now() - dt < timedelta(days=1) :
            visitedDictionary[comment] = time.strip()
    except OSError:
      print('File not found.')
      return

    try:
      with open('visited.txt', 'w') as visitedFile:
        for key, value in visitedDictionary.items():
          visitedFile.write(key + ' ' + value + '\n')
    except OSError:
      print('Error writing to file.')

def main():
  # Initialize the bot.
  bot = ByAccidentBot()

  bot.populateCommentDict('visited.txt')
  #bot.autoClearVisitedComments()
  bot.autoDeleteScoreCheck()

  print('Running...')

  commentStream = bot.reddit.subreddit('all').stream.comments()

  for comment in commentStream:
    try:
      if bot.searchForPhrase(comment.body):
        bot.replyToComment(comment)
        print('ID: ' + comment.id + ' ' + comment.body)
      except prawcore.exceptions.PrawcoreException:
        time.sleep(60)

if __name__ == "__main__":
  main()