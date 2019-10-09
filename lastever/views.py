from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Article

def index(request):
    article = Article.objects.order_by('-posted')[:10]

    context = {'articles': article}
    return render(request, 'lastever/home.html', context)

def news(request):
    articles = Article.objects.order_by('-posted').all()
    paginator = Paginator(articles, 3)

    page = request.GET.get('page')
    article = paginator.get_page(page)

    context = {'articles': article}
    return render(request, 'lastever/news.html', context)

def news_page(request, page_id):
    articles = Article.objects.order_by('-posted').all()
    paginator = Paginator(articles, 3)

    article = paginator.get_page(page_id)

    context = {'articles': article}
    return render(request, 'lastever/news.html', context)
