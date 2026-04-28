from django.db import models

# Create your models here.
class Car(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    prix_par_jour = models.FloatField()
    nb_places = models.IntegerField(null=True, blank=True)
    transmission = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    def __str__(self):
        return f"{self.marque} {self.modele}"
    

class Review(models.Model):
    
    comment = models.TextField()
    rating = models.IntegerField()


