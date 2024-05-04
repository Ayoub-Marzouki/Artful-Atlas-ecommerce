from django import forms
from home.models import ProductReview, ArtistReview, UserReview, UserRating, Contact, NewsletterSubscriber, Profile
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

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'phone', 'subject', 'message']

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Full name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Phone number"}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']
