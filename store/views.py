from django.shortcuts import render

from . import models

#create your views here
def genre_list(request):
    genres = models.Genre.objects.all()
    return render(request,'store/genre_list.html',{'genres':genres})