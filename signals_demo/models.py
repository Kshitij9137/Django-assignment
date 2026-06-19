from django.db import models


class UserProfile(models.Model):
    """Simple model used to trigger signals in our demos."""
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'signals_demo'
