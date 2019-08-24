from django.db import models
from django.template.defaultfilters import slugify
from tinymce import HTMLField
from django.contrib.auth.models import User

# Create your models here.
class League(models.Model):
    league_name = models.CharField(max_length=30)
    slug = models.SlugField(editable=False)
    def __str__(self):
        return self.league_name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.league_name)

        super(League, self).save(*args, **kwargs)

class Division(models.Model):
    division_name = models.CharField(max_length=30)
    division_logo = models.URLField(null=True, blank=True)
    division_leage = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.division_name

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    team_abbreviation = models.CharField(max_length=3)
    team_logo = models.URLField(null=True, blank=True)
    team_division = models.ForeignKey(Division, on_delete=models.DO_NOTHING)
    team_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.team_name

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    def __str__(self):
        return self.tag_name

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)
    posted = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    text = HTMLField('Content')
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        super(Article, self).save(*args, **kwargs)

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
    home_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='+')
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name='+')
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default=SCHEDULED,
    )
    playoff = models.BooleanField()
    referee = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(editable=False)

    def __str__(self):
        str = "%s %s %s" % (self.home_team, ' vs ', self.away_team)
        return str
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            slug_str = "%s %s %s" % (self.home_team, ' vs ', self.away_team)
            self.slug = slugify(slug_str)

        super(Schedule, self).save(*args, **kwargs)

class Statistic(models.Model):
    game = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    goals = models.PositiveSmallIntegerField()
    yellow_cards = models.PositiveSmallIntegerField()
    red_cards = models.PositiveSmallIntegerField()
    def __str__(self):
        self_str = "%s %s %s %s" % (self.game, ' - ', self.player, 'Statistic')
        return self_str
