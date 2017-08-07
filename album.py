import sys, os
from imgurpython import ImgurClient

from manage import DEFAULT_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
import django
django.setup()
from view.models import ViewData

from master import format_id

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
    # print(type(client))
    print(len(sys.argv))
    if len(sys.argv) < 3:
        client = get_client()
        '''
        Enter album info fields here!!

        Required fields: [album_id]
        Auto-generated fields: [url, album_image_links, version]
        Optional fields: [name, num_images, tags, ]
        '''
        #

        # Ex. http://imgur.com/a/FKsUu, https://imgur.com/a/FKsUu, FKsUu
        album_id = 'FKsUu'
        album_id = format_id(album_id)

        # Lazy exception handling
        if not album_id:
            raise ValueError('Invalid album id!')

        try:
            album_image_links = get_album_image_links(client, album_id)
            album_image_links_ = ','.join(album_image_links)
        except Exception as ex:
            print('Exception:', ex)
            raise ValueError('Probably invalid album id.')

        album_url = 'https://imgur.com/a/' + str(album_id)

        # Version: 1, 2, etc
        # Name: one word; "cats", "cars", "computers" etc
        # num_images: self-explanatory
        # tags: multiple word separated by comma: "colorful, boring, long" etc

        version = 1
        name = ''
        num_images = 0
        tags = ''

        album = ViewData.objects.create(album_id=album_id, url=album_url, images=album_image_links_,
                                        version=version, name=name, num_images=num_images, tags=tags)
        album.save()

    else:
        # print('Action:', sys.argv[1])
        client = get_client()
        if sys.argv[1] == 'add_album':
            # Viewdata.id
            album_id = sys.argv[2]
            album_id = format_id(album_id)

            # Viewdata.extra_1
            album_image_links = get_album_image_links(client, album_id)
            album_image_links_ = ','.join(album_image_links)

            # python manage.py migrate --run-syncdb to start
            # https://stackoverflow.com/a/37799885

            album_url = 'https://imgur.com/a/' + str(album_id)
            album = ViewData.objects.create(album_id=album_id, url=album_url, images=album_image_links_)
            album.save()

            print(album_image_links_)