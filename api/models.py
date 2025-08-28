from django.db import models
from django.contrib.auth.models import User

class Paragraph(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paragraphs')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class WordFrequency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    frequency = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'word']),
        ]