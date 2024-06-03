from django.db import models
from django_extensions.db.models import TitleDescriptionModel, ActivatorModel
from django.utils.translation import gettext_lazy as _


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
