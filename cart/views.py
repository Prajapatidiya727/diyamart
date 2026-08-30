from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cart
from products.models import Product
from order.models import Order


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = cart.items.get_or_create(
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.select_related("product")

    total = sum(
        item.subtotal
        for item in items
    )

    return render(
        request,
        "cart/cart.html",
        {
            "items": items,
            "total": total
        }
    )


@login_required
def remove_from_cart(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    item = get_object_or_404(
        cart.items,
        product_id=product_id
    )

    item.delete()

    return redirect("cart")


@login_required
def increase_quantity(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    item = get_object_or_404(
        cart.items,
        product_id=product_id
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect("cart")


@login_required
def decrease_quantity(request, product_id):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    item = get_object_or_404(
        cart.items,
        product_id=product_id
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")


@login_required
def checkout(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.select_related("product")

    if not items.exists():
        return redirect("cart")

    total = sum(
        item.subtotal
        for item in items
    )

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")

        if payment_method == "COD":

            for item in items:

                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    full_name=full_name,
                    phone=phone,
                    address=address,
                    city=city,
                    pincode=pincode,
                    payment_method="COD",
                    quantity=item.quantity
                )

            items.delete()

            return render(
                request,
                "order/success.html",
                {
                    "total": total
                }
            )

        request.session["checkout_data"] = {
            "full_name": full_name,
            "phone": phone,
            "address": address,
            "city": city,
            "pincode": pincode,
            "payment_method": payment_method
        }

        return render(
            request,
            "cart/payment.html",
            {
                "total": total,
                "payment_method": payment_method
            }
        )

    return render(
        request,
        "cart/checkout.html",
        {
            "cart_items": items,
            "total": total
        }
    )


@login_required
def demo_payment(request):

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    items = cart.items.select_related("product")

    if not items.exists():
        return redirect("cart")

    checkout_data = request.session.get("checkout_data")

    if not checkout_data:
        return redirect("checkout")

    total = sum(
        item.subtotal
        for item in items
    )

    if request.method == "POST":

        for item in items:

            Order.objects.create(
                user=request.user,
                product=item.product,
                full_name=checkout_data["full_name"],
                phone=checkout_data["phone"],
                address=checkout_data["address"],
                city=checkout_data["city"],
                pincode=checkout_data["pincode"],
                payment_method=checkout_data["payment_method"],
                quantity=item.quantity
            )

        items.delete()

        request.session.pop("checkout_data", None)

        return render(
            request,
            "order/success.html",
            {
                "total": total
            }
        )

    return render(
        request,
        "cart/payment.html",
        {
            "total": total,
            "payment_method": checkout_data["payment_method"]
        }
    )