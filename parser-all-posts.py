import requests
import json
import re
import pickle

boards_short = ['o', 'soc', 'media', 'r', 'int', 'po', 'news', 'hry', 'au', 'bi', 'biz', 'bo', 'c', 'cc', 'em', 'fa', 'fiz', 'fl', 'ftb', 'hh', 'hi', 'me', 'mg',
'mlp', 'mo', 'mov', 'mu', 'ne', 'psy', 're', 'sci', 'sf', 'sn', 'sp', 'spc', 'tv', 'un', 'w', 'wh', 'wm', 'wp', 'zog', 'de', 'di', 'diy', 'izd', 'mus', 'pa',
'p', 'wrk', 'trv', 'gd', 'hw', 'mobi', 'pr', 'ra', 's', 't', 'web', 'bg', 'cg', 'gsg', 'ruvn', 'tes', 'v', 'vg', 'wr', 'a', 'fd', 'ja', 'ma', 'vn']
boards_full = ['оэкаки', 'общение', 'анимация', 'просьбы', 'international', 'политика',
'новости', 'хрю', 'автомобили и транспорт', 'велосипеды', 'бизнес', 'книги', 'комиксы и мультфильмы', 'криптовалюты',
'другие страны и туризм', 'мода и стиль', 'физкультура', 'иностранные языки', 'футбол', 'hip-hop', 'история', 'медицина', 'магия',
'my little pony', 'мотоциклы', 'Фильмы', 'музыка', 'животные и природа', 'психология', 'религия', 'наука', 'научная фантастика', 'паранормальные явления',
'спорт', 'космос и астрономия', 'тв и кино', 'образование', 'оружие', 'warhammer', 'военная техника и оружие', 'обои и высокое разрешение', 'теории заговора', 'дизайн',
'столовая', 'хобби', 'графомания', 'музыканты', 'живопись', 'фото', 'РАБота и карьера', 'путешествия', 'gamedev', 'компьютерное железо', 'мобильные устройства и приложения',
'программирование', 'радиотехника', 'программы', 'техника', 'веб-мастера', 'настольные игры', 'консоли', 'grand strategy games', 'российские визуальные новеллы',
'the elder scrolls', 'video games', 'video games general', 'текстовые авторские рпг', 'аниме', 'фэндом', 'японская культура', 'манга', 'визуальные новеллы'
]

REGEXP = r'[а-яё]+|[a-z]+' # ru en
# REGEXP = r'[а-яё]+' # ru

def save(object, path):
    with open(path, 'wb') as f:
        pickle.dump(object, f)

def get_posts(num_th, board):
    resp = requests.get(f'https://2ch.hk/{board}/res/{num_th}.json')
    posts = []
    if resp.status_code != 200:
            print('failed')
            return
    js = json.loads(resp.text)
    for post in js['threads'][0]['posts']:
        text = re.findall(REGEXP, post['comment'].lower())
        posts.append(' '.join(text))
    return posts

def get_threads(board, board_full_name):
    resp = requests.get(f'https://2ch.hk/{board}/catalog.json')
    if resp.status_code != 200:
        print('query failed')
        return None
    js = json.loads(resp.text)
    res = {
        'board_short_name': board,
        'board_full_name': board_full_name,
        'messages': []
    }
    for th in js['threads']:
        res['messages'].append(' '.join(re.findall(REGEXP, th['comment'].lower())))
        posts = get_posts(th['num'], board)
        res['messages'] += posts
        #res['messages'].append(' '.join(re.findall(r'[а-яё]+', th['comment'].lower())))
    return res


def parse_all_boards(boards_short, boards_full):
    total_count = 0;
    for i in range(len(boards_short)):
        print(boards_full[i], end=' ')
        data = get_threads(boards_short[i], boards_full[i])
        print(len(data['messages']))
        total_count += len(data['messages'])
        save(data, f'data\\{boards_short[i]}.pickle')
    print('Total count: ', total_count)

parse_all_boards(boards_short, boards_full)