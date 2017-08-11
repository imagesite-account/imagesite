'''
When adding a new album ensure that album_id, name and init_message are correct
(or None if prefer not to use them)

When modifying an existing album ensure album_id exists and is correct, and fields that
should not be changed are None. To add/remove images from album, add/remove the images
from the imgur album then simply set the album_id to that album and set everything else
to None, then run python3 album.py modify.

See the instructions.pdf for more info.
'''

values_dict = {


    # Required fields:
    'album_id': 'NbU05', #ex. NbU05

    # Optional (important) fields:
    'name': 'haveaday',
    'init_message': # The 'initial picture' of the album people see when visiting homepage
        'http://i.imgur.com/JVhs653.jpg',


    # Optional (unimportant) fields (do not modify these unless you have good reason)
    'version': 0,
    'tags': (None,),
    'owner': None,
    'labels': (None,),
    
    # Auto-generated fields (do not modify these)
    'url': None, # Auto-generated
    'num_images': None, # Auto-generated
    'date_created': None, # Auto-generated
    'date_modified': None,
    'num_labels': None, # Auto-generated
    'images': (None,), # Auto-generated
}
