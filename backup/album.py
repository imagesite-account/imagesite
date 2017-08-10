import sys, os
from functools import reduce

from imgurpython import ImgurClient

from manage import DEFAULT_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
import django
django.setup()
from view.models import ViewData

from master import format_id
from set_album_values import values_dict as vd

EMPTY_ALBUM_KEY = '__empty_album__'


# http://imgur.com/a/NbU05, http://imgur.com/a/fdPFE, http://imgur.com/a/S7Ixt

def get_client():
    imgur_key_file = 'keys-imgur.txt'
    with open(imgur_key_file) as f:
        tokens = f.readlines()
        client_id = tokens[0].split(':')[1].strip()
        client_secret = tokens[1].split(':')[1].strip()
        # print(client_id, client_secret)
        # print(tokens)

    return ImgurClient(client_id, client_secret)


def get_album_image_links(client, album_id):
    album_images = client.get_album_images(album_id)
    album_image_links = [image.link for image in album_images]
    # for image in album_images:
    #     print(image.link)

    return album_image_links


# test album: http://imgur.com/a/VBrKp
if __name__ == '__main__':
    client = get_client()
    print('Number of arguments:', len(sys.argv))
    album_id = format_id(vd['album_id'])
    album_exists = ViewData.objects.filter(album_id=album_id).exists() \
                   if isinstance(album_id, str) else False
    
    if album_exists:
        print('Album already exists; please use "update" function if you want to update it.')
        print('Exiting...')
        quit()

    name = vd['name'] if isinstance(vd['name'], str) else album_id
    version = vd['version'] if isinstance(vd['version'], int) else 0

    tags = ''
    if isinstance(vd['tags'], (list, tuple)):
        if all([isinstance(t, str) for t in tags]):
            tags = ','.join(tags)

    labels = ''
    if isinstance(vd['labels'], (list, tuple)):
        if all([isinstance(l, str) for l in labels]):
            labels = ','.join(labels)

    owner = vd['owner'] if isinstance(vd['owner'], str) else ''
    init_message = vd['init_message'] if isinstance(vd['init_message'], str) \
        else 'http://i.imgur.com/IaXTuHx.png'
            
    
    url = 'https://imgur.com/a/%s' % str(album_id)

    try:
        album_image_links = get_album_image_links(client, album_id)
        album_image_links_ = ','.join(album_image_links)
    except Exception as ex:
        print('Exception trying to get images from album:', ex)
        raise ValueError('Probably invalid album id.')

    num_images = len(album_image_links_)
    num_labels = len(labels)

    album = ViewData.objects.create(album_id=album_id, name=name, version=version,
                                    tags=tags, labels=labels, owner=owner,
                                    init_message=init_message, url=url, images=album_image_links_,
                                    num_images=num_images, num_labels=num_labels)
    album.save()

    print('Success in adding', album_id)
    
