from django.contrib import admin
from .models import Package, Subscription


# Register your models here.
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "sku", "description", "price")


admin.site.register(Subscription)
