from django import forms
from .models import Category, Item, Review
from moviepy.editor import VideoFileClip
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewItemForm, self).__init__(*args, **kwargs)

        if 'category' in self.fields:
            self.fields['category'].queryset = Category.objects.all()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
            except (ValueError, TypeError):
                pass

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if isinstance(video, InMemoryUploadedFile):
                temp_video_file = tempfile.NamedTemporaryFile(delete=False)
                for chunk in video.chunks():
                    temp_video_file.write(chunk)
                temp_video_file.close()
                video_path = temp_video_file.name
            else:
                video_path = video.temporary_file_path()

            clip = VideoFileClip(video_path)
            if clip.duration > 60:
                raise ValidationError('Video is longer than 60 seconds.')
        return video

    class Meta:
        model = Item
        fields = ('category', 'condition', 'name', 'description', 'price', 'whatsapp_number', 'location', 'image', 'image1', 'image2', 'image3', 'image4', 'video')
        widgets = {
            'category': forms.Select(attrs={'class': INPUT_CLASSES, 'placeholder': 'Select a category'}),
            'condition': forms.Select(attrs={'class': INPUT_CLASSES, 'placeholder': 'Select condition'}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter item name'}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your location'}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter item price'}),
            'whatsapp_number': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your WhatsApp number (Recomended)'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter a detailed description of the item'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload main image'}),
            'image1': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'image2': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'image3': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'image4': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'video': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload a video (optional, max 30 sec)'}),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'image1', 'image2', 'image3', 'image4', 'is_sold', 'whatsapp_number', 'condition')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Item name'}),
            'condition': forms.Select(attrs={'class': INPUT_CLASSES, 'placeholder': 'Select condition'}),
            'price': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter item price'}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter seller location'}),
            'whatsapp_number': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter your WhatsApp number (optional)'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'placeholder': 'Enter a detailed description'}),
            'image': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload main image'}),
            'image1': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'image2': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'image3': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
            'image4': forms.FileInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Upload additional image (optional)'}),
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices from 1 to 5

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-control'}))

    class Meta:
        model = Review
        fields = ['rating', 'review_desp']
        widgets = {
            'review_desp': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter review description'}),
        }
