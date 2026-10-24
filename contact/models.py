from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Subject')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Received At')
    is_read = models.BooleanField(default=False, verbose_name='Read')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} — {self.name}"
