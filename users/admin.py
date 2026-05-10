from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'cin',
        'phone',
        'license_status',
        'trust_score',
        'created_at'
    )

    search_fields = (
        'user__username',
        'cin'
    )

    list_filter = (
        'license_status',
        'trust_score',
    )