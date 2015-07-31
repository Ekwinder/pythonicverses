import datetime
from haystack import indexes
from .models import Verse


class VerseIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True, model_attr='text')
	author = indexes.CharField(model_attr='author')
	title_auto = indexes.EdgeNgramField(model_attr='title')


	def get_model(self):
		return Verse

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		print '~~~~'
		return self.get_model().objects.all()