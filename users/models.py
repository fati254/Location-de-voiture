from django.contrib.auth.models import User 
from django.db import models


STATUS_CHOICES = [

    ('pending', 'En attente'),

    ('verified', 'Vérifié'),

    ('rejected', 'Refusé'),

]

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    cin = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(max_length=20)

    address = models.TextField()

    permis_recto = models.ImageField(
        upload_to='licenses/',
        null=True,
        blank=True
    )

    permis_verso = models.ImageField(
        upload_to='licenses/',
        null=True,
        blank=True
    )

    LICENSE_STATUS = [
        ('pending', 'En attente'),
        ('verified', 'Vérifié'),
        ('rejected', 'Refusé'),
    ]

    license_status = models.CharField(
        max_length=20,
        choices=LICENSE_STATUS,
        default='pending'
    )

    trust_score = models.IntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    