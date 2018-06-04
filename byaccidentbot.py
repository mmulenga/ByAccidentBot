import praw
import re
import threading

class ByAccidentBot():
  def __init__(self):
    self.commentDictionary = dict()
    self.reddit = praw.Reddit('byaccidentbot', user_agent='pi:com.example.bybottest:v0.0.1 by /u/thecrazybandicoot')
    self.searchPhrase = re.compile(r'.*\bon accident\b.*', flags=re.I)
    self.account = self.reddit.user.me()

  def populateCommentDict(self, filename):
    try:
      visitedCommentFile = open(filename, 'r')
    except OSError:
      print('File not found.')
      return

    for keyValue in visitedCommentFile:
      key,value = keyValue.split(' ')
      self.commentDictionary[key] = value
    
    visitedCommentFile.close()

  # Searches for instances of 'on accident' within the given comment.
  # Pre:  phrase - A valid regex pattern.
  #       comment - A valid reddit comment.
  # Post: Returns true if a match is found, false otherwise.
  def searchForPhrase(self, comment):
    if self.searchPhrase.match(comment):
      return True
    else:
      return False

  # Replies to the given comment with a pre-written message.
  # Pre: comment - A valid reddit comment.
  # Post: Replies to the comment with the appropriate reply template.
  def replyToComment(self, comment):
    try:
      comment.reply('Just a friendly reminder that it\'s \"by accident\".')
      return True
    except praw.exceptions.ClientException:
      print('Unable to reply to comment.')
      return False

  # Automatically deletes any comment that gets downvoted below 0, checking
  # every hour to see if the score has changed.
  # Gives users a method to delete the comment if they dislike it.
  def autoDeleteScoreCheck(self):
    threading.Timer(3600.0, self.autoDeleteScoreCheck, [self.account]).start()

    for comment in self.account.comments.new(limit=50):
      if comment.score < 0:
        comment.delete()

def main():
  bot = ByAccidentBot()
  commentStream = bot.reddit.subreddit('byaccidentbot').stream.comments()

  # Start score checker.
  bot.autoDeleteScoreCheck()

  for comment in commentStream:
    if bot.searchForPhrase(comment.body):
      bot.replyToComment(comment)
      print('ID: ' + comment.id + ' ' + comment.body)

if __name__ == "__main__":
  main()