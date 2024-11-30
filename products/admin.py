from django.contrib import admin

# Register your models here.
from .models import Category, File, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["parent", "title", "is_enable", "created_time"]
    list_filter = ["is_enable", "parent"]
    search_fields = ["title"]


class FileInlineAdmin(admin.StackedInline):
    model = File
    list_display = [
        "file",
        "file_type" "title",
        "is_enable",
    ]
    list_filter = ["is_enable", "parent"]
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "is_enable", "created_time"]
    list_filter = [
        "is_enable",
    ]
    search_fields = ["title"]
    inlines = [FileInlineAdmin]
    filter_horizontal = ["categories"]
