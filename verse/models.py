from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_markdown.models import MarkdownField


class Tag(models.Model):
	name = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return self.name

	@classmethod
	def search(cls, query):
		return cls.objects.filter(name__icontains=query)

class Verse(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=400)
	text = MarkdownField()
	date = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)
	tags = models.ManyToManyField(Tag)
	votes = models.IntegerField(default=0)
	

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "Verse"
		verbose_name_plural = "Verses"

class VoterList(models.Model):
	voter = models.ForeignKey('auth.User')
	voted = models.IntegerField(default=0)
	verse = models.ForeignKey(Verse)

	def __unicode__(self):
		return str(self.voter)