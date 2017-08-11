# Optional fields (they are only used as labels, no other meaningful purpose)
owner = 'name'
contact = 'your.email@domain.com'

# Delete an entry by adding it to filter_list
# Do not remove empty string (first entry) from filter list!
init = ''
filter_list = [init, 'S7Ixt',]


##try:
##    with open('filter_list.txt', 'r') as f:
##        album_list = [album.strip() for album in f.readlines()]
##        filter_list.extend(album_list)
##except Exception as ex:
##    print(['[userdata.py]: Error trying to parse filter file filter_list.py'])
    
