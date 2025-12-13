from django import forms
from .models import About, SocialLink


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ("about_header", "about_content")


class socialForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ("social_name", "social_icon", "social_link")
