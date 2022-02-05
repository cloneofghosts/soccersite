from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news', views.news, name='news'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('news/<int:page_id>', views.news_page, name='news_page'),
    path('league/<slug:league_slug>', views.league, name='league_page'),
    path('league/<slug:league_slug>/standings', views.standings, name='league_standings'),
    path('league/<slug:league_slug>/schedule', views.schedule, name='league_schedule'),
    path('league/<slug:league_slug>/statistics', views.statistics, name='league_statistics'),
]
