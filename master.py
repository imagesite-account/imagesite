

GLOBAL_CURRENT_HOST = 'http://127.0.0.1:8000'


IMAGE_ERR_CODES = {
    1: 'Unable to save rating to db. Please try resubmitting.'
}


acceptable_chars = '[]_-'
def is_acceptable_char(character):
    return character.isalnum() or character in acceptable_chars


def check_sql(table_name):

    for character in table_name:
        if not is_acceptable_char(character):
            raise ValueError('Invalid table name: contains character:', character)

    return ''.join(character for character in table_name if is_acceptable_char(character))


def format_id(item_id):
    item_id = item_id if '/' not in item_id else item_id.split('/')[-1]
    return item_id
