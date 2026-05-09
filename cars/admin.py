from django.contrib import admin
from .models import Car, Review


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = (
        'marque',
        'modele',
        'prix_par_jour',
        'disponible',
        'categorie',
        'carburant'
    )

    list_filter = (
        'categorie',
        'disponible',
        'carburant'
    )

    search_fields = (
        'marque',
        'modele'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'car',
        'rating'
    )

    list_filter = (
        'rating',
    )

    search_fields = (
        'user__username',
        'car__marque'
    )

admin.site.site_header = "AutoLux Administration"
admin.site.site_title = "AutoLux Admin"
admin.site.index_title = "Dashboard AutoLux"