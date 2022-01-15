from django.db import models
from django.template.defaultfilters import slugify
from tinymce import HTMLField
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from datetime import datetime

# Create your models here.
class League(models.Model):
    league_name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='league_name', unique=True)
    def __str__(self):
        return self.league_name

class Division(models.Model):
    division_name = models.CharField(max_length=30)
    division_logo = models.URLField(null=True, blank=True)
    division_leage = models.ForeignKey(League, on_delete=models.CASCADE)
    def __str__(self):
        return self.division_name

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_abbreviation = models.CharField(max_length=3)
    team_logo = models.URLField(null=True, blank=True)
    team_division = models.ForeignKey(Division, on_delete=models.CASCADE)
    team_owner = models.ForeignKey(User, limit_choices_to={'groups__name__in': ["Team Owner", "Admin"]}, on_delete=models.CASCADE)
    def __str__(self):
        return self.team_name

    def save(self, *args, **kwargs):
        self.author = self.team_owner
        super(Team, self).save(*args, **kwargs)

class Player(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    def __str__(self):
        return self.tag_name

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    posted = models.DateTimeField(default=datetime.now)
    tags = models.ManyToManyField(Tag)
    text = HTMLField('Content')
    def __str__(self):
        return self.title

class Schedule(models.Model):
    # Options for Game Status
    SCHEDULED = 'SCH'
    FINAL = 'FIN'
    FINAL_EXTRA_TIME = 'FET'
    FINAL_PENALTYS = 'FPK'
    CANCELLED = 'CAN'
    RESCHEDULED = 'RES'
    STATUS_CHOICES = [
        (SCHEDULED, 'Scheduled'),
        (FINAL, 'Final'),
        (FINAL_EXTRA_TIME, 'Final/Extra Time'),
        (FINAL_PENALTYS, 'Final/Penalty Kicks'),
        (CANCELLED, 'Cancelled'),
        (RESCHEDULED, 'Rescheduled'),
    ]

    scheduled_time = models.DateTimeField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    home_pk = models.PositiveSmallIntegerField(null=True, blank=True)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_pk = models.PositiveSmallIntegerField(null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=SCHEDULED,
    )
    playoff = models.BooleanField()
    referee = models.ForeignKey(User, limit_choices_to={'groups__name__in': ["Referee", "Admin"]}, on_delete=models.CASCADE)


    def __str__(self):
        str = "%s %s %s" % (self.home_team, ' vs ', self.away_team)
        return str
    slug = AutoSlugField(populate_from='__str__', unique=True)

    def save(self, *args, **kwargs):
        self.author = self.referee
        super(Schedule, self).save(*args, **kwargs)


class Statistic(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.PositiveSmallIntegerField()
    yellow_cards = models.PositiveSmallIntegerField()
    red_cards = models.PositiveSmallIntegerField()
    def __str__(self):
        self_str = "%s %s %s %s" % (self.game, ' - ', self.player, 'Statistic')
        return self_str

# Database Views, adding them in as models so they can be used in the code
class Standings(models.Model):

    team = models.CharField(max_length=30)
    gp = models.PositiveSmallIntegerField()
    w = models.PositiveSmallIntegerField()
    d = models.PositiveSmallIntegerField()
    l = models.PositiveSmallIntegerField()
    pts = models.PositiveSmallIntegerField()
    gf = models.PositiveSmallIntegerField()
    ga = models.PositiveSmallIntegerField()
    gd = models.SmallIntegerField()
    division_id = models.PositiveSmallIntegerField()
    logo = models.URLField(null=True, blank=True)

    class Meta:
       managed = False
       db_table = "lastever_standings"

class Statistics(models.Model):

    team_name = models.CharField(max_length=30)
    player_name = models.CharField(max_length=30)
    gp = models.PositiveSmallIntegerField()
    goals = models.PositiveSmallIntegerField()
    yellowCards = models.PositiveSmallIntegerField()
    redCards = models.PositiveSmallIntegerField()
    player_id = models.PositiveSmallIntegerField()
    team_id = models.PositiveSmallIntegerField()
    league_id = models.PositiveSmallIntegerField()

    class Meta:
       managed = False
       db_table = "lastever_stats"
