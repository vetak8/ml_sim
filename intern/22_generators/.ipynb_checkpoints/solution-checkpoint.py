import random

def username_generator(n, first_names=None, last_names=None):
    '''
    Generation usernames
    '''
    if not first_names:
        first_names = ['Andre', 'Puto', 'Biba']
    if not last_names:
        last_names = ['Madre', 'Boba', 'Quattro']
    for id in range(1, n + 1):
        yield {'id': id,
               'first_name': random.choice(first_names),
               'last_name': random.choice(last_names)}

def data_generator(n):
    '''
    Generation data
    '''
    y_list = list(range(101))
    for x in range(n):
        y = random.choice(y_list)
        yield (x, y)
