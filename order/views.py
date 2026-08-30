from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Order


@login_required
def my_orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .select_related("product")
        .order_by("-ordered_at")
    )

    return render(
        request,
        "order/my_orders.html",
        {
            "orders": orders,
        }
    )


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    if order.status == "Pending":

        order.status = "Cancelled"
        order.save()


    return redirect("my_orders")


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status == "Pending":

        order.status = "Cancelled"
        order.save()

    return redirect("my_orders")