from rest_framework import serializers
from .models import message

class messageSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = message
        fields = ['author', 'content', 'timestamp']