from django.db import models


class Trope(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    rating = models.FloatField()
    shelf = models.CharField(max_length=20)
    tropes = models.ManyToManyField("Trope")

    notes = models.TextField(blank=True, null=True)
    progress = models.IntegerField(default=0)

    # Cover options
    cover_url = models.URLField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    # ✅ YOUR EXTRA FIELDS (add them back here)
    is_comfort = models.BooleanField(default=False)
    release_date = models.DateField(null=True, blank=True)
    is_released = models.BooleanField(default=True)
    favorite_scene = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
