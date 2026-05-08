import csv

from cars.models import Car

with open('cars_data.csv', newline='', encoding='utf-8') as file:

    reader = csv.DictReader(file)

    for row in reader:

        Car.objects.create(

            marque=row['marque'],
            modele=row['modele'],
            prix_par_jour=row['prix_par_jour'],
            transmission=row['transmission'],
            carburant=row['carburant'],
            image='cars/' + row['image']

        )

print("Voitures ajoutées avec succès")