import sys
from imgurpython import ImgurClient


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


if __name__ == '__main__':
    # print(type(client))
    print(len(sys.argv))
    if len(sys.argv) < 3:
        print('Not enough arguments; please enter an action.')
        print('Options: \n'
              'add_album [album_id], '
              'remove_album [album_id]')
    else:
        print('Action:', sys.argv[1])
        client = get_client()
        if sys.argv[1] == 'add_album':
            album_id = sys.argv[2]
            album_image_links = get_album_image_links(client, album_id)
            print(album_image_links)