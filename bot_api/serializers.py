from .models import Comment
from rest_framework import serializers

class CommentSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Comment
    fields = ('reddit_id', 'timestamp')