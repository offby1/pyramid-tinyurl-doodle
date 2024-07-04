from app.models import ShortenedURL
from django.forms import ModelForm


class ShortenForm(ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ["original"]
