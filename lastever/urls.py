from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news', views.news, name='news'),
    path('news/<int:page_id>', views.news_page, name='news_page'),
    path('league/<slug:league_slug>', views.league, name='league_page'),
    path('league/<slug:league_slug>/standings', views.standings, name='league_standings'),
]
