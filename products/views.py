from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderProduct, ProductReview
from .forms import YourOrderForm, ReviewForm  # Import your order form
from django.contrib import messages

def products_view(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_details.html', {'product': product})

def search_products(request):
    query = request.GET.get('query')

    if query:
        # Perform a case-insensitive search on both name and location
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(info__icontains=query)
    else:
        products = Product.objects.all()

    context = {
        'products': products
    }

    return render(request, 'search_products.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Check if the user already has an open order or create a new one
    user = request.user
    open_order, created = Order.objects.get_or_create(user=user)

    # Check if the product is already in the user's cart, and update the quantity if necessary
    order_product, created = OrderProduct.objects.get_or_create(order=open_order, product=product)
    if not created:
        order_product.quantity += 1
        order_product.save()

    # Calculate and update the total_price for the order based on order products
    open_order.total_price = sum(op.item_total for op in open_order.orderproduct_set.all())
    open_order.save()

    return redirect('cart')


@login_required
def view_cart(request):
    user = request.user
    open_order = Order.objects.filter(user=user).first()
    context = {
        'open_order': open_order,
    }
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, order_product_id):
    order_product = get_object_or_404(OrderProduct, pk=order_product_id)

    if order_product.order.user == request.user:
        order_product.delete()

    return redirect('cart')

@login_required
def checkout(request):
    user = request.user
    open_order = Order.objects.filter(user=user).first()

    if request.method == 'POST':
        form = YourOrderForm(request.POST)
        if form.is_valid():
            # Process the order and payment here
            open_order.is_ordered = True
            open_order.save()
            return render(request, 'order_confirmation.html', {'order': open_order})

    else:
        form = YourOrderForm()

    context = {
        'open_order': open_order,
        'form': form,
    }

    return render(request, 'checkout.html', context)

@login_required
def update_cart(request, order_product_id):
    order_product = get_object_or_404(OrderProduct, pk=order_product_id)

    if request.user == order_product.order.user:
        if request.method == 'POST':
            if 'update' in request.POST:
                # Update the quantity based on user input
                new_quantity = request.POST.get('quantity', None)
                if new_quantity is not None:
                    new_quantity = int(new_quantity)
                    if new_quantity >= 1:
                        order_product.quantity = new_quantity
                        order_product.save()
                    else:
                        # Handle invalid input (e.g., negative or zero quantity)
                        # You can add error handling logic here
                        pass

            elif 'increase' in request.POST:
                order_product.quantity += 1
                order_product.save()
            elif 'decrease' in request.POST:
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
            elif 'remove' in request.POST:
                order_product.delete()

            # Calculate and update the total_price for the order based on order products
            open_order = order_product.order
            open_order.total_price = sum(op.item_total for op in open_order.orderproduct_set.all())
            open_order.save()

    return redirect('cart')



@login_required
def write_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.user = request.user  # Assuming user is logged in
            review.save()
            return redirect('product_details', product_id=product_id)  # Redirect to the turf details page

    else:
        form = ReviewForm()

    return render(request, 'write_review_products.html', {'form': form})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    # Check if the user is the owner of the review
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Review updated successfully.')
                return redirect('product_details', product_id=review.product_id)
        else:
            form = ReviewForm(instance=review)
        return render(request, 'edit_review_products.html', {'form': form, 'review': review})
    else:
        messages.error(request, 'You do not have permission to edit this review.')
        return redirect('product_details', product_id=review.product_id)

@login_required
def confirm_delete_review(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    # Check if the user is the owner of the review
    if request.user == review.user:
        if request.method == 'POST':
            # Redirect to the deletion view if the user confirms the delete action
            return redirect('delete_review_products', review_id=review_id)
        return render(request, 'confirm_delete_review_products.html', {'review': review})
    else:
        messages.error(request, 'You do not have permission to delete this review.')
        return redirect('product_details', product_id=review.product_id)

@login_required
def delete_review(request, review_id):
    # Get the review object
    review = get_object_or_404(ProductReview, pk=review_id)

    # Check if the user has permission to delete the review
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Review deleted successfully')  # Set a success message
    else:
        messages.error(request, 'You do not have permission to delete this review')  # Set an error message

    return redirect('product_details', product_id=review.product_id)
