import praw
import re
import threading

# Tests the regular expression to see what types of matches it comes up with
# can be commented out for prod.
# Pre: file - A valid text file containing test phrases.
# Post: Output of all phrases matching the regex pattern.
def test(filename):
  testFile = open(filename, "r")
  print('Opened test file...')

  for line in testFile:
    if searchForPhrase(line):
      print(line)

  testFile.close()
  print('Closed test file...')

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
  reddit = praw.Reddit('byaccidentbot', user_agent='pi:com.example.bybottest:v0.0.1 by /u/thecrazybandicoot')
  phrase = re.compile(r'.*\bon accident\b.*', flags=re.I)
  subredditSubmissions = reddit.subreddit('space').hot(limit=20)
  botAccount = reddit.user.me()

  # Start score checker.
  autoDeleteScoreCheck(botAccount)

  # Uncomment for testing.
  # test('regtesttext.txt')

  for submission in subredditSubmissions:
    print('------ ' + submission.title + ' ------')

    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():
      if searchForPhrase(phrase, comment.body):
        replyToComment(comment)
        #print('ID: ' + comment.id + ' ' + comment.body)

if __name__ == "__main__":
    main()