from django.db import models
from decimal import Decimal
import uuid
from django.core.validators import RegexValidator
from django.templatetags.static import static
from app.utils import product_image_path


uz_phone_validator = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami +998XXXXXXXXX ko'rinishida bo'lishi kerak (masalan +998901234567).",
)



class Category(models.Model):
    title = models.CharField(max_length=255,unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Categories'
    


class Product(models.Model):
    name = models.CharField()
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=14,decimal_places=2) # 2000
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=product_image_path,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    discount = models.PositiveIntegerField(default=0) # 30
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def discounted_price(self):
        if self.discount:
            return self.price * (Decimal('1') - self.discount / Decimal('100'))

        return self.price
    
    @property
    def get_image_path(self):
        if self.image:
            return self.image.url
        
        return static("app/images/not_found_image.jpg")
        
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
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               related_name='replies',
                               null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.email} - {self.message}'
    
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13, validators=[uz_phone_validator])
    quantity = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                related_name='orders',
                                null=True,
                                blank=True
                                )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} - {self.phone}'
    
    class Meta:
        db_table = 'orders'