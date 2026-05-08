import csv

from django.core.management.base import BaseCommand

from cars.models import Car


class Command(BaseCommand):

    help = 'Importer les voitures CSV'


    def handle(self, *args, **kwargs):

        with open('cars_data.csv', newline='', encoding='utf-8') as file:

            reader = csv.DictReader(file)

            for row in reader:

                Car.objects.create(

                    marque=row['marque'],

                    modele=row['modele'],

                    prix_par_jour=float(row['prix_par_jour']),

                    nb_places=int(row['nb_places']),

                    transmission=row['transmission'],

                    carburant=row['carburant'],

                    categorie=row['categorie'],

                    image='cars/' + row['image']

                )

        self.stdout.write(
            self.style.SUCCESS(
                'Voitures importées avec succès'
            )
        )