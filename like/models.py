from django.db import models
from user.models import User
from content.models import Feed

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} likes Feed {self.feed.id}"
