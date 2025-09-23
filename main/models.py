import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top'),
        ('shorts', 'Shorts'),
        ('jacket', 'Jacket'),
        ('shoes', 'Shoes'),
        ('socks', 'Socks'),
        ('gloves', 'Gloves'),
        ('ball', 'Ball'),
        ('lainnya', 'Lainnya'),
    ]

    BRAND_CHOICES = [
        ('nike', 'Nike'),
        ('adidas', 'Adidas'),
        ('puma', 'Puma'),
        ('lainnya', 'Lainnya'),
    ]

    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lainnya')
    is_featured = models.BooleanField(default=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, default='lainnya')
    product_views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name
    
    @property
    def is_trending(self):
        return self.product_views > 20
        
    def increment_views(self):
        self.product_views += 1
        self.save()