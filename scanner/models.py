from django.db import models
from django.contrib.auth.models import User

class Scanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=500, unique=True)  # URL'yi benzersiz yaparak her kullanıcı için tek URL
    is_approved = models.BooleanField(default=False)  # Admin onayı
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.url}"
