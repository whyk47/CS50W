from django import forms
from .models import Category

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=128, label="Title")
    starting_bid = forms.DecimalField(decimal_places=2, max_digits=10, label="Starting Bid ($)")
    img_url = forms.CharField(max_length=2048, label="Image URL", required=False)
    desc = forms.CharField(max_length=1024, label="Description")
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label="Categories", required=False)