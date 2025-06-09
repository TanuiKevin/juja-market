from django.contrib import admin
from .models import Category, Item,Review, Subcategory



admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Subcategory)