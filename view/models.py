from random import shuffle

from django.db import models
from django.utils import timezone

# Create your models here.

# Model for view database, containing references to all albums:
# Album     | album_id  | TEXT       | PRIMARY KEY
# Album     | name      | TEXT
# Album     | URL       | URLField
# Album     | num images| INT
# Album     | tags      | TEXT
# Album     | date      | DateTimeField
# Album     | modified  | DateTimeField
# Album     | owner     | TEXT
# Album     | extra 1   | TEXT
# Album     | extra 2   | TEXT


# Concurrency:
# https://stackoverflow.com/questions/10325683/can-i-read-and-write-to-a-sqlite-database-concurrently-from-multiple-connections
class ViewData(models.Model):
    album_id = models.TextField(primary_key=True, blank=True, null=False)
    name = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)

    num_images = models.IntegerField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    date_modified = models.DateTimeField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    num_labels = models.IntegerField(blank=True, null=True)

    # rating_0 = models.IntegerField(blank=True, null=True)
    # rating_1 = models.IntegerField(blank=True, null=True)
    # rating_2 = models.IntegerField(blank=True, null=True)
    # rating_3 = models.IntegerField(blank=True, null=True)
    # rating_4 = models.IntegerField(blank=True, null=True)
    # rating_5 = models.IntegerField(blank=True, null=True)
    # rating_6 = models.IntegerField(blank=True, null=True)
    # rating_7 = models.IntegerField(blank=True, null=True)
    # rating_8 = models.IntegerField(blank=True, null=True)
    # rating_9 = models.IntegerField(blank=True, null=True)

    labels = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    init_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_image_list(self):
        # Randomize viewing order?
        image_list = self.images.split(',')
        shuffle(image_list)
        return image_list

    class Meta:
        # Set managed = True
        # https://stackoverflow.com/a/35494384
        managed = True
        db_table = 'view_data'
