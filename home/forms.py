from django import forms
from home.models import ProductReview, ArtistReview, UserReview, UserRating
from cities_light.models import Country, City

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write a review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']


class ArtistReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write a review"}))

    class Meta:
        model = ArtistReview
        fields = ['review', 'rating']

class UserReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write a testimonial"}))

    class Meta:
        model = UserReview
        fields = ['review']

class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['rating']


class CheckoutForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select a country")
    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Select a city")

