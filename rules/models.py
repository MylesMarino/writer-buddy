from django.db import models


class Rule(models.Model):
    RULE_TYPES = [
        ('preset', 'Preset'),
        ('custom', 'Custom'),
        ('ai', 'AI-Assisted'),
    ]

    name = models.CharField(max_length=255)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    pattern = models.TextField(blank=True, help_text='For custom rules: regex pattern or word/phrase to flag')
    is_active = models.BooleanField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)
