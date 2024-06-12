from django.db import models
from django_extensions.db.models import TitleDescriptionModel, ActivatorModel,TimeStampedModel
from django.utils.translation import gettext_lazy as _
from user.models import User, UserAddress


# Create your models here.
class Category(TitleDescriptionModel):
    """Model for Categories Details,Fields:name(title), and description"""
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    image = models.ImageField(upload_to='uploaded_image/', default="product_images/default-product-image.jpg")

    class Meta:
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.title


class Product(ActivatorModel, TitleDescriptionModel):
    """Model for Products Fields: name,sub_category(F.K.),description, price, stock, image, status"""
    """STATUS is not required as we are using the activator_model"""

    AVAILABLE = 1
    OUT_OF_STOCK = 0

    categories = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=50)
    image = models.ImageField(upload_to='uploaded_image/', default="product_images/default-product-image.jpg")


    def __str__(self):
        return self.title



class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mycart')
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart: {self.id} User: {self.user}"

    @property
    def cart_total(self):
        total = 0
        for item in self.carts.all():
            total += item.sub_total()
        return total

    @property
    def total_items(self):
        return self.carts.count()

    @property
    def total_tax(self):
        result = round(self.cart_total) * 18/100
        return result

    @property
    def delivery_charges(self):
        if self.cart_total >= 5000:
            return 0
        return 99

    @property
    def order_total(self):
        bill = round(self.cart_total) + round(self.total_tax) + round(self.delivery_charges)
        return bill


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='users')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='carts')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='selected_items')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"ID: {self.id}, Product_item: {self.item}, Quantity: {self.quantity}"

    def sub_total(self):
        return self.quantity * self.item.price

    def item_quantity(self):
        return self.quantity


class Order(TimeStampedModel):
    STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
        ('Deleted', 'Deleted'),
        ('Cancelled', 'Cancelled')
    )

    order = models.CharField(max_length=10, null=True, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='cart')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myorders')
    total_amount = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    delivery_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True,
                                         related_name='myaddress')

    class Meta:
        ordering = ['id']

    def save(self, **kwargs):
        self.total_amount = self.cart.order_total
        return super(Order, self).save(**kwargs)

    def __str__(self):
        return str(self.order)






