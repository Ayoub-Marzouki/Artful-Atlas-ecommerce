from django import forms
from home.models import ProductReview, ArtistReview, UserReview, UserRating, Contact, NewsletterSubscriber, Profile, Offer
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
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Last name"}))
    bio = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Bio"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder" : "Phone number (You don't have to specify which region)"}))
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'image', 'bio', 'phone']


class OfferForm(forms.ModelForm):
    offer_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder':"Your custom price"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Tell the artist about your offer"}))
    class Meta:
        model = Offer
        fields = ['offer_price', 'message']
