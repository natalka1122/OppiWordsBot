import settings
import os
os.environ["POLYGLOT_DATA_PATH"]=settings.polyglot_env
from polyglot.text import Word
from loguru import logger
api_url = settings.w2v_api

from bot.bot_utils import mysql_connect

N_LAST = 3

CODES = {
    'finnish': 'fi',
    'german': 'de',
    'english': 'en',
    'italian': 'it',
    'estonian': 'et',
    'thai': 'th',
    'japanese': 'ja',
    'spanish': 'es',
    'french': 'fr',
    'dutch': 'nl'

}

QUERY = 'SELECT w.word, s.last_date ' \
        'FROM spaced_repetition s ' \
        'INNER JOIN words w ON w.hid = s.hid ' \
        'WHERE w.user=%s ' \
        'AND w.language=\'{}\'' \
        'AND last_date IS NOT NULL ' \
        'ORDER BY last_date DESC;'
# select word from words where language='english' and user='444209921';

def get_user_words(user_id, lang):
    result = set()
    words = mysql_connect.fetchall(QUERY.format(lang), (user_id,))
    words = words[:N_LAST]
    for w in words:
        result.add(w[0])
    return result


def get_sems(word, lang):
    print(word)
    w = Word(word.lower(), language=CODES[lang.lower()])
    try:
        res = w.neighbors
    except Exception as e:
        logger.warning(e)
        return None
    return res


def get_list(user_id, lang):
    result = list()
    words = get_user_words(user_id, lang)
    words = [w.lower() for w in words]
    for w in words:
        sems = get_sems(w, lang)
        if sems is None:
            continue
        for s in sems:
            if s in words:
                continue
            result.append(s)
    return result[:20]

if __name__ == '__main__':
    words = get_list(0000)
    print(words)

