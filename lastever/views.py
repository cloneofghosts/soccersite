from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Article, League, Tag, Division, Standings, Schedule

def index(request):
    article = Article.objects.order_by('-posted')[:3]

    context = {'articles': article}
    return render(request, 'lastever/home.html', context)

def news(request):
    articles = Article.objects.order_by('-posted').all()
    paginator = Paginator(articles, 10)

    page = request.GET.get('page')
    article = paginator.get_page(page)

    context = {'articles': article}
    return render(request, 'lastever/news.html', context)

def news_page(request, page_id):
    articles = Article.objects.order_by('-posted').all()
    paginator = Paginator(articles, 10)

    article = paginator.get_page(page_id)

    context = {'articles': article}
    return render(request, 'lastever/news.html', context)

def league(request, league_slug):
    league = League.objects.get(slug=league_slug)
    tag = Tag.objects.filter(tag_name=league.league_name).first()
    article = Article.objects.filter(tags=tag).order_by('-posted')[:10]

    context = {'articles': article}
    return render(request, 'lastever/home.html', context)

def standings(request, league_slug):
    league = League.objects.get(slug=league_slug)
    division = Division.objects.filter(division_leage=league.id)
    standings = Standings.objects.filter(division_id__in=division)

    context = {'standings': standings, 'division': division}
    return render(request, 'lastever/standings.html', context)

def schedule(request, league_slug):
    league = League.objects.get(slug=league_slug)
    schedule = Schedule.objects.filter(league=league.id)
    results = schedule.filter(status__icontains='F').order_by('-scheduled_time')
    schedule = schedule.exclude(status__icontains='F').order_by('-scheduled_time')

    context = {'schedule': schedule, 'results': results}
    return render(request, 'lastever/schedule.html', context)

def statistics(request, league_slug):
    league = League.objects.get(slug=league_slug)
    division = Division.objects.filter(division_leage=league.id)
    standings = Standings.objects.filter(division_id__in=division)

    context = {'standings': standings, 'division': division}
    return render(request, 'lastever/standings.html', context)
