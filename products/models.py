from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    owner_name = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', default='default.jpg')  # For the product image (avatar)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Use DecimalField for prices
    info = models.TextField(default="")
    connect = models.CharField(max_length=1000, default="")
    owner_email = models.EmailField(max_length=100, blank=True, null=True, default="")


    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / len(reviews)
        else:
            return 0

    @property
    def avg_rating(self):
        return round(self.average_rating(), 2)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', default='default.jpg')  # For additional product images

    def __str__(self):
        return f"Image for {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)  # Allow null and set a default value
    date_ordered = models.DateTimeField(auto_now_add=True)
    # You can add any other fields you need for orders


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # You may want to add a property for the total price of this order item
    @property
    def item_total(self):
        return self.product.price * self.quantity

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"