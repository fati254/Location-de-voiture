
from .models import Car , Review  
from django.views.generic import ListView 
from django.shortcuts import render , get_object_or_404

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

    if budget:
        cars = cars.filter(prix_par_jour__lte=budget)

    if places:
        cars = cars.filter(nb_places__gte=places)

    if marque:
        cars = cars.filter(marque__icontains=marque)

    if categorie:
        cars = cars.filter(categorie__icontains=categorie)

    if disponible == "on":
        cars = cars.filter(disponible=True)

    return render(request, 'cars/cars_list.html', {'cars': cars})