from django import forms

class quotationForm(forms.Form):
    email = forms.EmailField(label='Your email')
    name = forms.CharField(label='Your name')
    phone_number = forms.CharField(label="Your phone number")
