from django.shortcuts import render
from django.core.paginator import Paginator


def index(request):

    return render(request, 'soccersite/index.html')
	
def login(request):

    return render(request, 'soccersite/login.html')