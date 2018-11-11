from django.db import models

class Comment(models.Model):
  reddit_id = models.CharField(max_length=10)
  timestamp = models.DateTimeField()

  def __str__(self):
    return self.reddit_id