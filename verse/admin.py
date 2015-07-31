from django.contrib import admin
from models import Verse, Tag, VoterList
from django_markdown.admin import MarkdownModelAdmin


class VerseAdmin(MarkdownModelAdmin):
	list_display = ("title","date")

admin.site.register(Verse, VerseAdmin)
admin.site.register(Tag)
admin.site.register(VoterList)	
