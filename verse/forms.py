from django import forms
from .models import Verse, Tag
from django.contrib.flatpages.models import FlatPage
from django_markdown.widgets import MarkdownWidget
from djtokeninput import TokenField, TokenWidget


class ContactForm(forms.Form):
	full_name = forms.CharField()
	email = forms.EmailField()
	message = forms.CharField()

class VerseForm(forms.ModelForm):
	class Meta:
		model = Verse
		fields = ('title','text','tags')