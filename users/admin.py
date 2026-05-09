from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'cin',
        'phone',
        'trust_score',
        'created_at'
    )

    search_fields = (
        'user__username',
        'cin'
    )

    list_filter = (
        'trust_score',
    )