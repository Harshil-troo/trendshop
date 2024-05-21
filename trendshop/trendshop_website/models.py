from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel, ActivatorModel
from django.utils.translation import gettext_lazy as _


class Category(TitleDescriptionModel):
    """Model for Categories Details,Fields:name(title), and description"""

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class SubCategory(TimeStampedModel):
    """Model for SubCategory,Fields: name, category(F.K.)"""
    name = models.CharField(max_length=50)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_subcategories', null=True,
                                     blank=True)

    class Meta:
        verbose_name_plural = 'Sub-Categories'

    def __str__(self):
        return f"Name : {self.name}, Category : {self.category}"


class Products(ActivatorModel, TitleDescriptionModel):
    """Model for Products Fields: name,sub_category(F.K.),description, price, stock, image, status"""
    """STATUS is not required as we are using the activator_model"""

    AVAILABLE = 1
    OUT_OF_STOCK = 0

    categories = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=50)
    image = models.ImageField(upload_to='product_images/', default="product_images/default-product-image.jpg")

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"Name : {self.title}, Price : {self.price}"


