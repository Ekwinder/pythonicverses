from django.conf import settings
import simplejson as json
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Verse, Tag, VoterList
from .forms import ContactForm, VerseForm
from django.utils import timezone
from .serializers import TagSerializer
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from haystack.query import SearchQuerySet

def verse_list(request,q=None):
	request.POST.get('q',None)
	if q != None:
		query = q
		return render(request, 'search.html', {'query':query})
	else:
		verses = Verse.objects.all().order_by('-date')
		return render(request, 'home.html',{'verses':verses})

def new(request):
	form = VerseForm(request.POST or None)
	if form.is_valid():
		verse = form.save(commit=False)
		#verse.text = request.POST.get('test',None)
		verse.author = request.user
		verse.date = timezone.now()
		verse.save()
		return redirect('verse_detail',pk=verse.pk)
	else:
		form = VerseForm()
	return render(request, 'new.html', {'form': form})

def verse_detail(request, pk):
	if request.user.is_authenticated():	
		verse = get_object_or_404(Verse,pk=pk)
		value = None
		try:
			q = VoterList.objects.get(Q(voter=request.user),Q(verse=verse))
			value = q
			print q
		except VoterList.DoesNotExist:
			pass
		return render(request, 'verse_detail.html',{'verse':verse,'q':value	}) 
	else:
		verse = get_object_or_404(Verse,pk=pk)
		value = None
		return render(request, 'verse_detail.html',{'verse':verse,'q':value	}) 

def about(request):
	return render(request, 'about.html',{})

def tags(request, name):
	verses = Verse.objects.filter(tags__name=name)
	return render(request, 'tags.html',{'verses':verses})

def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get('email')
		form_message = form.cleaned_data.get('message')
		form_full_name = form.cleaned_data.get('full_name')

		subject = 'Pythonic contact form'
		from_email = settings.EMAIL_HOST_USER
		contact_message="%s: %s via %s"%(form_full_name,form_message, form_email)
		send_mail(subject, contact_message, from_email,[from_email], fail_silently=False)
		if request.POST:
			form = None
	context={
	"form":form
	}
	return render(request,"contact.html",context)


@login_required
def profile(request):
	user = request.user
	verses = Verse.objects.filter(author = user)
	context = {'user':user, 'verses':verses}
	return render(request, 'profile.html',context)

def oprofile(request, username):
	user = User.objects.filter(username = username)
	verses = Verse.objects.filter(author = user)
	context = {'user':user, 'verses':verses}
	return render(request,'profile.html',context)

@login_required
def upvote(request):
	context = {}
	if request.method == 'GET':
		verse_id = request.GET.get('verse_id')
	votes = 0
	if verse_id:
		verse = Verse.objects.get(id=int(verse_id))
		if verse:
			try:
				q = VoterList.objects.get(Q(voter=request.user),Q(verse=verse))
				q.voted = 1
				q.save()
			except VoterList.DoesNotExist:
				u = VoterList(voter = request.user, voted = 1, verse = verse)
				u.save()
				pass
			votes = verse.votes + 1
		verse.votes = votes
		verse.save()


	return HttpResponse(votes)

@login_required	
def downvote(request):
	context = {}
	if request.method == 'GET':
		verse_id = request.GET.get('verse_id')
	else:
		votes = 0
	if verse_id:
		verse = Verse.objects.get(id=int(verse_id))
		if verse:
			try:
				q = VoterList.objects.get(Q(voter=request.user),Q(verse=verse))
				q.voted = 2-3
				q.save()
			except VoterList.DoesNotExist:
				u = VoterList(voter = request.user, voted = 2-3, verse = verse)
				u.save()
				pass
			votes = verse.votes - 1
		verse.votes = votes
		verse.save()

	return HttpResponse(votes)

@login_required	
def revote(request):
	context = {}
	if request.method == 'GET':
		verse_id = request.GET.get('verse_id')
	else:
		votes = 0
	was = 0
	if verse_id:
		verse = Verse.objects.get(id=int(verse_id))
		if verse:
			try:
				q = VoterList.objects.get(Q(voter=request.user),Q(verse=verse))
				was = q.voted
				q.voted = 0
				q.save()
			except VoterList.DoesNotExist:
				u = VoterList(voter = request.user, voted = True, verse = verse)
				u.save()
				pass
			if was > 0:
				votes = verse.votes - 1
			else:
				votes = verse.votes + 1	
		verse.votes = votes
		verse.save()
	return HttpResponse(votes)

class TagSearch(generics.ListAPIView):
	model = Tag
	serializer_class = TagSerializer

	def get_queryset(self):
		"""
		Optionally restricts the returned purchases to a given user,
		by filtering against a `name` query parameter in the URL.
		"""
		queryset = Tag.objects.all()
		name = self.kwargs['q']
		qlist =  name[2:]
		if qlist is not None:
			queryset = queryset.filter(name__icontains=qlist)

		return queryset
