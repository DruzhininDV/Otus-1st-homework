from nltk import pos_tag


def make_flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4] """
    return sum([list(item) for item in _list], [])


def check_is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if check_is_verb(word)]
