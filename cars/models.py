from django.db import models
from django.contrib.auth.models import User

from datetime import date
# Create your models here.
class Car(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    prix_par_jour = models.FloatField()
    nb_places = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=50)
    carburant = models.CharField(max_length=50, default="Essence")
    categorie = models.CharField(max_length=50, default="SUV")
    disponible = models.BooleanField(default=True) 

    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    def __str__(self):
        return f"{self.marque} {self.modele}"


class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    comment = models.TextField()

    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.car}"


class Notification(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title