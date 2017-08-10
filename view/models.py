from random import shuffle

from django.db import models
from django.utils import timezone
from django.apps import apps

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
    name = models.TextField(blank=True, null=True, default='')
    url = models.URLField(blank=True, null=True, default='')
    version = models.IntegerField(blank=True, null=True, default=0)

    num_images = models.IntegerField(blank=True, null=True, default=0)
    tags = models.TextField(blank=True, null=True, default='')
    date_created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    date_modified = models.DateTimeField(blank=True, null=True, default=timezone.now)
    owner = models.TextField(blank=True, null=True, default='')
    num_labels = models.IntegerField(blank=True, null=True, default=0)

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

    labels = models.TextField(blank=True, null=True, default='')
    images = models.TextField(blank=True, null=True, default='')
    init_message = models.TextField(blank=True, null=True, default='')

    _DATABASE = 'default'

    def __str__(self):
        return self.name if self.name else self.album_id

    def get_image_list(self, shuffle_list=True):
        image_list = self.images.split(',')
        # Randomize viewing order?
        if shuffle_list:
            shuffle(image_list)
        return image_list

    def get_labels(self):
        labels = self.labels
        if not labels or ',' not in labels:
            labels = [i for i in range(10)]
        else:
            labels = labels.split(',')

        return labels

    def get_basic_info(self):
        info = {
            'album_id': self.album_id,
            'name': self.name,
            'init_message': self.init_message,
        }

        return info

    def collect_data(self):
        album_ratings = []
        try:
            with conns['album_image_data'].cursor() as c:
                c.execute('''SELECT image_id, rating FROM {table_name}'''
                          .format(table_name=self.album_id))
                album_ratings = c.fetchall()
                print(album_ratings)
        except Exception as ex:
            print('''[View/models.py/ViewData/collect_data]
                  Error trying to collect data for model''', self.name, self.id)

        return album_ratings
    class Meta:
        # Set managed = True
        # https://stackoverflow.com/a/35494384
        managed = True
        db_table = 'view_data'


######################################################
from django.db import connections as conns

from master import check_sql, format_id


# Create or fetch a dynamic django model.
def create_or_get_model(album_id):
    album_id = format_id(album_id)
    table_name = album_id  # name of the table created by sql
    model_name = 'album_%s' % (album_id,)
    try:
        model = apps.get_registered_model('view', model_name)
        return model
    except LookupError:
        pass

    print('[View/models.py/create_or_get_model] no model exists for model %s, creating one:' % model_name)

    model = None
    try:
        # Unfortunately, have to use raw sql to create
        # db table - not much built in support for
        # dynamic modelling.
        #
        # Either the db table + model are both created,
        # Or only db table is created and model fails,
        # Or everything fails.
        album_id = check_sql(album_id)
        with conns['album_image_data'].cursor() as c:
            c.execute('''CREATE TABLE IF NOT EXISTS {table_name}
                        (rating INT, datetime TEXT, image_id TEXT, extra TEXT)
                        '''
                      .format(table_name=album_id))

        class Meta:
            managed = True
            db_table = table_name

        attrs = {
            'rating': models.CharField(max_length=200),
            'datetime': models.CharField(max_length=200),
            'image_id': models.CharField(max_length=200),
            'extra': models.CharField(max_length=200),
            '_DATABASE': 'album_image_data',
            '__module__': 'view.models',
            'Meta': Meta
        }
        model = type(str(model_name), (models.Model,), attrs)
    except Exception as ex:
        print('[View/models.py/create_or_get_model] Error:', ex)


    return model
