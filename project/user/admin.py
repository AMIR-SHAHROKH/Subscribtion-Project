from django.contrib import admin
from packages.models import Package
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass
