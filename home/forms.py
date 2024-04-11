from django import forms
from home.models import ProductReview, ArtistReview

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
