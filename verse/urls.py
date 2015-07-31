from django.conf.urls import include, url
import haystack
from . import views

urlpatterns = [
    url(r'^$', views.verse_list),
    url(r'^about/', views.about),
    url(r'^new/$', views.new, name='new'),
    url(r'^contact/', views.contact),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^oprofile/(?P<username>.+)/$', views.oprofile, name='oprofile'),
    url(r'^tags/(?P<name>.+)/$', views.tags),
    url(r'^verse/(?P<pk>[0-9]+)/$', views.verse_detail, name='verse_detail'),
    url(r'^upvote/$', views.upvote, name='upvote'),
    url(r'^downvote/$', views.downvote, name='downvote'),
    url(r'^revote/$', views.revote, name='revote'),
    url(r'^search/(?P<q>.+)$',views.TagSearch.as_view(),name='tag_search'),
    url(r'^search/', include('haystack.urls')),
]   