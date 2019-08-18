from django.contrib import admin

from .models import League, Division, Team, Tags, Player, News, Schedule

# Change Admin List Display
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('division_name', 'division_leage')
    autocomplete_fields = ['division_leage']

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_abbreviation', 'team_division')
    list_filter = ['team_division']
    search_fields = ['team_name']

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_name', 'slug')
    search_fields = ['league_name']

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'number', 'team')
    list_filter = ['team']
    search_fields = ['first_name', 'last_name', 'team']
    autocomplete_fields = ['team']

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'posted', 'get_tags')
    list_filter = ['posted']
    search_fields = ['title']
    autocomplete_fields = ['tags']

    def get_tags(self, obj):
        return "\n".join([t.tag_name for t in obj.tags.all()])

    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['posted'], 'classes': ['collapseable']}),
        ('Tags',             {'fields': ['tags'], 'classes': ['collapseable']}),
        ('Post',             {'fields': ['text']}),
    ]

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('scheduled_time', 'home_team', 'home_score', 'away_team', 'away_score', 'status', 'playoff', 'slug')
    list_filter = ['scheduled_time', 'status', 'playoff']

    fieldsets = [
        ('Date information', {'fields': ['scheduled_time']}),
        ('Team information', {'fields': ['home_team', 'home_score', 'away_team', 'away_score'], 'classes': ['collapseable']}),
        ('Game Status',      {'fields': ['status', 'playoff']}),
    ]
    autocomplete_fields = ['home_team', 'away_team']

class TagsAdmin(admin.ModelAdmin):
    search_fields = ['tag_name']

# Register your models here.
admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Schedule, ScheduleAdmin)
