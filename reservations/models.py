from django.db import models
from django.contrib.auth.models import User
from cars.models import Car


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reservations")
    date_debut = models.DateField()
    date_fin = models.DateField()
    is_validated = models.BooleanField(default=False)
    contract_generated = models.BooleanField(default=False) #contrat apres paiement

    
    def number_of_days(self):

        return (
            self.date_fin - self.date_debut
        ).days

    def total_price(self):

        return (
            self.number_of_days()
            * self.car.prix_par_jour
        )

    def __str__(self):
        return f"{self.user} - {self.car}"
    

from django.db import models
from reservations.models import Reservation

class Payment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('cancelled', 'Annulé'),
    ]

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.FloatField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reservation.id} - {self.status}"