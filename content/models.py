from django.db import models
from user.models import User

class Feed(models.Model):
    content=models.TextField()
    image=models.TextField()
    image = models.TextField()
    user=models.ForeignKey(User, on_delete = models.CASCADE, related_name='feeds') #유저 테이블에서 유저 외부참조
    like_count=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True )

    def __str__(self):
        return f"{self.user.email} - {self.content[:30]}"