from django.contrib import admin

# Register your models here.
from django.contrib.auth.decorators import login_required
from .models import League, Division, Team, Tag, Player, Article, Schedule, Statistic

admin.site.login = login_required(admin.site.login)


# Inlines
class StatisticInline(admin.TabularInline):
    model = Statistic
    extra = 0
    autocomplete_fields = ["player"]


# Change Admin List Display
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("division_name", "division_leage")
    autocomplete_fields = ["division_leage"]


class TeamAdmin(admin.ModelAdmin):
    list_display = ("team_name", "team_abbreviation", "team_division")
    list_filter = ["team_division"]
    search_fields = ["team_name"]

    def get_queryset(self, request):
        qs = super(TeamAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team_owner=request.user)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ("league_name", "slug")
    search_fields = ["league_name"]


class PlayerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "number", "team")
    list_filter = ["team"]
    search_fields = ["first_name", "last_name", "team"]
    autocomplete_fields = ["team"]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "posted", "get_tags")
    list_filter = ["posted"]
    search_fields = ["title"]
    autocomplete_fields = ["tags"]

    def get_tags(self, obj):
        return "\n".join([t.tag_name for t in obj.tags.all()])

    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["posted"], "classes": ["collapseable"]}),
        ("Tags", {"fields": ["tags"], "classes": ["collapseable"]}),
        ("Post", {"fields": ["text"]}),
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "scheduled_time",
        "home_team",
        "home_score",
        "away_team",
        "away_score",
        "status",
        "playoff",
        "slug",
    )
    list_filter = ["scheduled_time", "status", "playoff"]

    fieldsets = [
        ("Date information", {"fields": ["scheduled_time", "league"]}),
        (
            "Team information",
            {
                "fields": [
                    "home_team",
                    "home_score",
                    "home_pk",
                    "away_team",
                    "away_score",
                    "away_pk",
                ],
                "classes": ["collapseable"],
            },
        ),
        ("Game Status", {"fields": ["referee", "status", "playoff"]}),
    ]
    inlines = [StatisticInline]
    autocomplete_fields = ["home_team", "away_team"]
    search_fields = ["home_team", "away_team"]

    def get_queryset(self, request):
        qs = super(ScheduleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(referee=request.user)


class TagAdmin(admin.ModelAdmin):
    search_fields = ["tag_name"]


class StatisticAdmin(admin.ModelAdmin):
    list_display = ("game", "player", "goals", "yellow_cards", "red_cards")
    list_filter = ["game", "player"]
    autocomplete_fields = ["player", "game"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Statistic, StatisticAdmin)
