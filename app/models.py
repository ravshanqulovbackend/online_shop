import uuid
from django.db import models
from decimal import Decimal

from django.core.validators import RegexValidator
from django.templatetags.static import static
from app.utils import product_image_path




# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    discount = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    stock = models.PositiveIntegerField(default=0)
    image = models.FileField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    @property
    def discounted_price(self):
        if self.discount and self.discount > 0:
            return self.price * (Decimal('1') - Decimal(self.discount) / Decimal('100'))
        return self.price
    
    @property
    def get_image_path(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://dummyimage.com/450x300/dee2e6/6c757d.jpg"

    def __str__(self):
        return self.name




class Comment(models.Model):
    
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3 
        FOUR = 4
        FIVIE = 5
    
    
    name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField()
    message = models.TextField()
    file = models.FileField(upload_to='comments/',null=True,blank=True)
    rating = models.IntegerField(choices=RatingChoices.choices,default = RatingChoices.ONE.value)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='comments',
                                null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.email} - {self.message}'

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=13, validators=[RegexValidator(r'^\+\d{12}$')])
    quantity = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        db_table = 'orders'
