from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    default_image = models.URLField(null = True, max_length = 300)
    coordinate = models.CharField(max_length = 30)
    raw_data = models.TextField()
    source = models.CharField(max_length = 20)
    unique_id = models.CharField(max_length = 50, unique = True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    url = models.URLField(null = True)
    address = models.CharField(max_length = 100, null = True)
    super_category = models.CharField(max_length = 20)
    sub_category = models.CharField(max_length = 30)
    rating = models.FloatField(null = True)
    review = models.TextField()

    def __unicode__(self):
        return self.name


class Review(models.Model):
    venue_id = models.IntegerField()
    text = models.TextField()
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    uploaded = models.DateTimeField()

    def __unicode__(self):
        return self.first_name