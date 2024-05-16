from django import forms
from home.models import Technique, Style, Philosophy, SubjectMatter, Product, CartOrder, Artist

MEDIUM = (
    ("canvas", "Canvas"),
    ("paper", "Fine Art Paper"),
    ("wood_panel", "Wood Panel"),
    ("other", "Other")
)
SHIPPING = (
    ("free", "Free"),
    ("not included", "Not Included")
)

class addArtworkForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title of your artwork'}))
    image = forms.ImageField()
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Price of your artwork'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description | Story | Meaning of the artwork according to the artist.'}))
    specifications = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'A more detailed description of the tools used to paint the artwork.'}))
    width = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Width of your artwork in centimeters'}))
    height = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Height of your artwork in centimeters'}))
    depth = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Depth of your artwork in centimeters'}))

    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'price',
            'medium',
            'width',
            'height',
            'depth',
            'shipping',
            'technique',
            'style',
            'philosophy',
            'subject_matter',
            'description',
            'specifications',
            'signed_by_artist',
            'available',
        ]

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = CartOrder
        fields = ['product_status']
        widgets = {
            'product_status': forms.Select(attrs={'class': 'form-control'}),
        }

        

class CoverImageForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['profileArtworkImage']



class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['image']

    

class SocialMediaForm(forms.ModelForm):
    facebook = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'https://www.facebook.com/username'}))
    instagram = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'https://www.instagram.com/username/'}))

    class Meta:
        model = Artist
        fields = ['facebook', 'instagram']



class ArtistInfoForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'city', 'shortBio']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Artist Name'}),
            'city': forms.Select(),
            'shortBio': forms.TextInput(attrs={'placeholder': 'Short Bio'}),
        }


class BiographyForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['biography']

        widgets = {
            'biography': forms.Textarea(attrs={'placeholder': 'Biography', 'rows': 4}),
        }


class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['description']
        
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 4}),
        }


class OrientationForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['technique', 'style', 'philosophy', 'subject_matter']

        widgets = {
            'technique': forms.Select(),
            'style': forms.Select(),
            'philosophy': forms.Select(),
            'subject_matter': forms.Select(),
        }
