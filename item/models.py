from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from moviepy.editor import VideoFileClip


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Subcategories'
    
    def __str__(self):
        return self.name
    
def validate_video_length(value):
    video = VideoFileClip(value.path)
    if video.duration > 60:  # duration is in seconds
        raise ValidationError('Video is longer than 60 seconds.') 


class Item(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('USED', 'Second Hand/Used'),
    ]

    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES, default='NEW')
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    image1 = models.ImageField(upload_to='item_images', blank=True, null=True)
    image2 = models.ImageField(upload_to='item_images', blank=True, null=True)
    image3 = models.ImageField(upload_to='item_images', blank=True, null=True)
    image4 = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='item_video', blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rating = models.IntegerField()
    review_desp = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.name