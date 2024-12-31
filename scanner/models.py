from django.db import models
from django.contrib.auth.models import User

class Scanner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scanned_urls")
    url = models.URLField(max_length=500, unique=True)  # URL'yi benzersiz yaparak her kullanıcı için tek URL
    is_approved = models.BooleanField(default=False)  # Admin onayı
    results = models.JSONField(null=True, blank=True)  # Tarama sonuçlarını saklamak için JSONField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['user']),
            models.Index(fields=['is_approved']),  # Onaylanmış URL'lerin hızlı sorgulanması için
        ]
        ordering = ['-created_at']  # Varsayılan sıralama: En son eklenen ilk sırada gösteriyo

    def __str__(self):
        return f"{self.user.username} - {self.url}"

    def approval_status(self):
        return "Onaylandı" if self.is_approved else "Onay Bekliyor"

    approval_status.short_description = "Onay Durumu"
