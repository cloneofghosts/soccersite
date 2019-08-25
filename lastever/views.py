from django.shortcuts import render

from .models import Article

def index(request):
    article = Article.objects.order_by('-posted').all()
    context = {'articles': article}
    return render(request, 'lastever/home.html', context)
