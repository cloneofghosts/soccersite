from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class League(models.Model):
    league_name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.league_name
    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
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
    def __str__(self):
        return self.team_name
