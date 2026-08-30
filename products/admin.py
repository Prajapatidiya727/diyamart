from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "image_preview",
        "name",
        "category",
        "price",
        "stock",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "category",
    )

    ordering = (
        "-id",
    )

    list_per_page = 10


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius:8px;">',
                obj.image.url
            )

        return "No Image"


    image_preview.short_description = "Preview"