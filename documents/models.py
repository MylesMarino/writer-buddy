from django.db import models
import secrets


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    settings = models.JSONField(default=dict, blank=True)
    share_token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.settings:
            self.settings = {
                'visible_words': 7,
                'disappearing_text_enabled': True
            }
        super().save(*args, **kwargs)
    
    def generate_share_token(self):
        self.share_token = secrets.token_urlsafe(32)
        self.save()
        return self.share_token
