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


class ViewData(models.Model):
    album_id = models.TextField(primary_key=True, blank=True, null=False)
    name = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    num_images = models.IntegerField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    date_modified = models.DateTimeField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    extra_1 = models.TextField(blank=True, null=True)
    extra_2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # Set managed = True
        # https://stackoverflow.com/a/35494384
        managed = True
        db_table = 'view_data'