from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "brand", "price", "description", "is_featured", "thumbnail"]