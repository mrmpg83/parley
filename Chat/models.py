from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class message(models.Model):
    room_name = models.CharField(max_length=255, db_index=True, default='general')
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    @staticmethod
    def last_message(room_name, limit=10):
        # پیام‌های آخر یک چت خاص
        return reversed(
            message.objects.filter(room_name=room_name).order_by('-timestamp')[:limit]
        )

    def __str__(self):
        return f"{self.author.username} - {self.room_name}"