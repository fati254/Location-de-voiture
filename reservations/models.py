from django.db import models
from cars.models import Car #pour faire relation avec car

from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.user} - {self.car}"