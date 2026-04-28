
from .models import Car , Review  
from django.views.generic import ListView 
from django.shortcuts import render , get_object_or_404

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
     cars = Car.objects.all()

     # 🔍 FILTRES
     budget = request.GET.get('budget')
     places = request.GET.get('places')

     if budget:
        cars = cars.filter(prix_par_jour__lte=budget)

     if places:
        cars = cars.filter(nb_places__gte=places)

        return render(request, 'cars/cars_list.html', {'cars': cars})

def car_detail(request, id):
    car = get_object_or_404(Car, id=id)

     # 🔥 RECOMMANDATION SIMPLE
    recommended = Car.objects.filter(categorie=car.categorie).exclude(id=car.id)[:3]

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'recommended': recommended
     })