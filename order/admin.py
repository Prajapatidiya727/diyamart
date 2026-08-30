from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'status',
        'payment_method',
        'ordered_at',
    )

    list_filter = (
        'status',
        'payment_method',
        'ordered_at',
    )

    search_fields = (
        'user__username',
        'product__name',
    )

    readonly_fields = (
        'ordered_at',
    )

    ordering = (
        '-ordered_at',
    )