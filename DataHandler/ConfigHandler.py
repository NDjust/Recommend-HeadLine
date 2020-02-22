import json

ATTR_LIST = [
    'db_host',
    'db_user',
    'db_passwd',
    'db_port',
    'title_table',
    'title_column',
    'content_table',
    'content_column'
]


def loadFromFile(path='config.conf'):
    raw_lines = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            while True:
                l = f.readline()
                if not l: break
                if l and l[0] == '#': continue
                raw_lines.append(l)
        return load(''.join(raw_lines))
    except:
        return None


def load(rawText):
    try:
        loaded = json.loads(rawText)
        return loaded
    except:
        return None


def check(conf):
    for attr in ATTR_LIST:
        if attr not in conf.keys():
            return False
    return True


def get_default():
    with open('config.conf', 'w', encoding='utf-8') as f:
        f.write('# Configure file for Generate-HeadLine\n{\n')
        lines = []
        for attr in ATTR_LIST:
            lines.append('   "{}": ""'.format(attr))
        f.write(',\n'.join(lines))
        f.write('\n}')