from django.shortcuts import render


def index(request):
    return render(request, "soccersite/index.html")


def login(request):
    return render(request, "soccersite/login.html")
