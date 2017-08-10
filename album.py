import sys, os
import csv

from imgurpython import ImgurClient

from manage import DEFAULT_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)
import django
django.setup()
from view.models import ViewData, create_or_get_model

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
    if len(sys.argv) < 2:
        print('''Not enough arguments: options are "add", "modify" or "collect".
              See documentation for what each do.''')
        quit()
    
    client = get_client()

    def add_album():
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

        num_images = len(album_image_links)
        num_labels = len(labels)

        album = ViewData.objects.create(album_id=album_id, name=name, version=version,
                                        tags=tags, labels=labels, owner=owner,
                                        init_message=init_message, url=url, images=album_image_links_,
                                        num_images=num_images, num_labels=num_labels)
        album.save()

        print('Success in adding', album_id)

    def modify_album():
        album_id = format_id(vd['album_id'])
        album_exists = ViewData.objects.filter(album_id=album_id).exists() \
                       if isinstance(album_id, str) else False
        
        if not album_exists:
            print('''Album %s does not exist; please use "add"
                  function if you want to add it.''' % album_id)
            print('Exiting...')
            quit()

        a = ViewData.objects.get(album_id=album_id)
        a.name = vd['name'] if isinstance(vd['name'], str) else a.name
        a.init_message = vd['init_message'] if isinstance(vd['init_message'], str) \
            else a.init_message

        success_updating_images = False
        try:
            album_image_links = get_album_image_links(client, album_id)
            album_image_links_ = ','.join(album_image_links)
            success_updating_images = True
        except Exception as ex:
            print('Exception trying to get images from album:', ex)
            raise ValueError('Probably invalid album id.')

        a.images = album_image_links_
        num_images = len(album_image_links)
        a.num_images = num_images
        
        save_list = []
        if isinstance(vd['name'], str):
            save_list.append('name')
        if isinstance(vd['init_message'], str):
            save_list.append('init_message')
        if success_updating_images:
            save_list.extend(['images', 'num_images'])

        print('[album.py] save_list:', save_list)
        a.save()

        print('Successfully saved changes to', album_id)

    def collect_data(album_id, savepath='data/'):
        album_id=format_id(album_id)
        album_exists = ViewData.objects.filter(album_id=album_id).exists() \
                       if isinstance(album_id, str) else False
        
        if not album_exists:
            print('Album %s does not exist; please add it first.' % album_id)
            print('Exiting...')
            quit()
##        A = create_or_get_model(album_id)
##        if A is None:
##            print('[album.py] Error occured trying to create or get model for album_id:', album_id)
##            quit()
##        all_ratings = A.objects.filter(rating=7)
##        # print(rating)
##        
##        for rating in all_ratings:
##            print(rating)
        
        a = ViewData.objects.get(album_id=album_id)
        album_ratings = a.collect_data()
        image_dict = {format_id(image): {i: 0 for i in range(1,11)} \
                      for image in a.get_image_list(shuffle_list=False)}
        
        for image, rating in album_ratings:
            image = format_id(image)
            try:
                rating = int(rating)
            except ValueError as ve:
                print(''' [album.py]
                      Error trying to convert rating in album
                      %s for image %s: rating %s''' % (album_id, image, rating))
                continue
            
            if image in image_dict:
                image_dict[image][rating] += 1
            else:
                print(''' [album.py]
                      Warning: Unknown image in %s: %s''' % (album_id, image))

        with open('data/%s_data.csv' % (album_id,), 'w', newline='') as csvfile:
            album_writer = csv.writer(csvfile, delimiter=',')
            album_writer.writerow(
                ['image_id',] + ['r_%d' % rating for rating in range(1, 11)] + \
                    ['r_total',]
            )
            for image, rating_dict in image_dict.items():
                album_writer.writerow(
                    [image,] + [number for rating, number in rating_dict.items()] + \
                        [sum([number for rating, number in rating_dict.items()]),]
                )
                print(image)
                for rating, number in rating_dict.items():
                    print(rating, number)

        print('Successfully collected data for %s' % album_id)
            
    if sys.argv[1] == 'add':
        add_album()
    elif sys.argv[1] == 'update':
        modify_album()
    elif sys.argv[1] == 'collect':
        if len(sys.argv) < 3:
            print('''[album.py]
                  Not arguments enough for "collect": must provide album_id.''')
            quit()
        collect_data(sys.argv[2])
    
