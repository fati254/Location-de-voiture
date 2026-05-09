from django.contrib import admin
from .models import Reservation, Payment


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'car',
        'date_debut',
        'date_fin',
        'is_validated'
    )

    list_filter = (
        'is_validated',
    )

    search_fields = (
        'user__username',
        'car__marque'
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'reservation',
        'amount',
        'status'
    )

    list_filter = (
        'status',
    )