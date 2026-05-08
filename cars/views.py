
from .models import Car , Review  
from django.views.generic import ListView 
from django.shortcuts import render , get_object_or_404
from reservations.models import Reservation
from datetime import datetime

import json
import re
import spacy 
nlp = spacy.load("fr_core_news_sm")
FAMILY_WORDS = [
    "famille",
    "familiale",
    "enfants",
    "voyage",
    "amis",
    "groupe"
]

ECONOMY_WORDS = [
    "pas cher",
    "economique",
    "économique",
    "budget",
    "petit prix"
]

LUXURY_WORDS = [
    "luxe",
    "vip",
    "premium",
    "confort"
]

SUV_WORDS = [
    "suv",
    "4x4",
    "grand"
]


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


#filtre
class CarListView(ListView):
     model = Car  ##modele utilise 
     template_name = 'cars/cars_list.html'
     context_object_name = 'cars'


#pour home qu'il herite de base
def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars' : cars})

def contact(request):
    return render(request, 'contactez.html')

def propos(request):
    return render(request, 'apropos.html')

def avis(request):
      reviews = Review.objects.all()

      if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            user=request.user,
            rating=rating,
            comment=comment
        )

      return render(request, 'avis.html', {'reviews': reviews})


def cars_list(request):
    print("GET DATA =", request.GET)

    cars = Car.objects.all()

    budget = request.GET.get('budget')
    places = request.GET.get('places')
    marque = request.GET.get('marque')
    categorie = request.GET.get('categorie')
    disponible = request.GET.get('disponible')
    ville = request.GET.get('ville')

    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    if budget:
        cars = cars.filter(prix_par_jour__lte=budget)

    if places:
        cars = cars.filter(nb_places__gte=places)

    if marque:
        cars = cars.filter(marque__icontains=marque)

    if categorie:
        cars = cars.filter(categorie__icontains=categorie)

    if ville:
        cars = cars.filter(ville__icontains=ville)

    if disponible == "on":
        cars = cars.filter(disponible=True)

    if date_debut and date_fin:
        try:
            date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()
            date_fin = datetime.strptime(date_fin, "%Y-%m-%d").date()

            cars = cars.exclude(
                reservations__date_debut__lte=date_fin,
                reservations__date_fin__gte=date_debut
            )

        except:
            print("Erreur format date")

    return render(request, 'cars/cars_list.html', {'cars': cars})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_chat_search(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body)

            message = data.get('message', '').lower()

            print("MESSAGE USER =", message)

            doc = nlp(message)

            cars = Car.objects.all()

            scored_cars = []

            for car in cars:

                score = 0

                print(
                    car.marque,
                    car.modele,
                    car.categorie,
                    car.transmission
                )

                # =========================
                # FAMILY DETECTION
                # =========================

                if any(word in message for word in FAMILY_WORDS):

                    if car.nb_places and car.nb_places >= 5:
                        score += 5

                    if car.categorie.strip().lower() == "suv":
                        score += 5

                # =========================
                # ECONOMY DETECTION
                # =========================

                if any(word in message for word in ECONOMY_WORDS):

                    if car.prix_par_jour <= 500:
                        score += 5

                # =========================
                # LUXURY DETECTION
                # =========================

                if any(word in message for word in LUXURY_WORDS):

                    if car.prix_par_jour >= 1000:
                        score += 5

                # =========================
                # SUV DETECTION
                # =========================

                if any(word in message for word in SUV_WORDS):

                    if car.categorie.strip().lower() == "suv":
                        score += 5

                # =========================
                # AUTOMATIQUE
                # =========================

                if "automatique" in message:

                    if (
                        car.transmission
                        and
                        car.transmission.strip().lower() == "automatique"
                    ):
                        score += 5

                # =========================
                # DIESEL
                # =========================

                if "diesel" in message:

                    if (
                        car.carburant
                        and
                        car.carburant.strip().lower() == "diesel"
                    ):
                        score += 5

                # =========================
                # NOMBRE DE PLACES
                # =========================

                for token in doc:

                    if token.like_num:

                        try:

                            number = int(token.text)

                            if (
                                car.nb_places
                                and
                                car.nb_places >= number
                            ):
                                score += 3

                        except:
                            pass

                print("SCORE =", score)

                # =========================
                # AJOUT SI SCORE > 0
                # =========================

                if score > 0:

                    scored_cars.append({

                        'car': car,

                        'score': score

                    })

            # =========================
            # TRI PAR SCORE
            # =========================

            scored_cars.sort(
                key=lambda x: x['score'],
                reverse=True
            )

            result = []

            for item in scored_cars[:5]:

                car = item['car']

                result.append({

                    'id': car.id,

                    'name': f"{car.marque} {car.modele}",

                    'price': car.prix_par_jour,

                    'image': car.image.url if car.image else '',

                    'score': item['score']

                })

            print("RESULT =", result)

            return JsonResponse({

                'cars': result

            })

        except Exception as e:

            print("ERREUR IA =", e)

            return JsonResponse({

                'cars': [],

                'error': str(e)

            })

    return JsonResponse({

        'cars': []

    })