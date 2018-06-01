import praw
import re
import threading

def initCommentDict(dict):
  try:
    visitedCommentFile = open('visitedComments.txt', 'r')
  except OSError:
    print('File not found.')
    return

  for keyValue in visitedCommentFile:
    key,value = keyValue.split(' ')
    dict[key] = value

# Searches for instances of 'on accident' within the given comment.
# Pre:  phrase - A valid regex pattern.
#       comment - A valid reddit comment.
# Post: Returns true if a match is found, false otherwise.
def searchForPhrase(phrase, comment):
  if phrase.match(comment):
    return True
  else:
    return False

# Replies to the given comment with a pre-written message.
# Pre: comment - A valid reddit comment.
# Post: Replies to the comment with the appropriate reply template.
def replyToComment(comment):
  comment.reply('Just a friendly reminder that it\'s \"by accident\".')

# Automatically deletes any comment that gets downvoted below 0, checking
# every hour to see if the score has changed.
# Gives users a method to delete the comment if they dislike it.
def autoDeleteScoreCheck(user):
  threading.Timer(3600.0, autoDeleteScoreCheck, [user]).start()

  for comment in user.comments.new(limit=50):
    if comment.score < 0:
      comment.delete()

def main():
  commentDictionary = dict()
  reddit = praw.Reddit('byaccidentbot', user_agent='pi:com.example.bybottest:v0.0.1 by /u/thecrazybandicoot')
  phrase = re.compile(r'.*\bon accident\b.*', flags=re.I)
  commentStream = reddit.subreddit('byaccidentbot').stream.comments()
  botAccount = reddit.user.me()

  # Start score checker.
  autoDeleteScoreCheck(botAccount)

  for comment in commentStream:
    if searchForPhrase(phrase, comment.body):
      replyToComment(comment)
      print('ID: ' + comment.id + ' ' + comment.body)

if __name__ == "__main__":
    main()