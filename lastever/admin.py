from django.contrib import admin


from .models import League, Division, Team

# Change Admin List Display
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('division_name', 'division_leage')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'team_abbreviation', 'team_division')
    list_filter = ['team_division']
    search_fields = ['team_name']

class LeagueAdmin(admin.ModelAdmin):
        list_display = ('league_name', 'slug')

# Register your models here.
admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Team, TeamAdmin)
