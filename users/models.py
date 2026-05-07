from django.contrib.auth.models import User 
from django.db import models

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    cin = models.CharField(
        max_length=20,
        unique=True
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    driver_license = models.ImageField(
        upload_to='licenses/'
    )

    trust_score = models.IntegerField(
        default=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username