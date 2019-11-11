import random

from bot.app.core import bot, authorize
from bot.bot_utils import bot_utils


async def unscramble_message(query, callback_data):
    session, isValid = await authorize(query.from_user.id)
    if not isValid:
        return
    revield = session.unscramble_revieled
    m = query.message
    new_data = list()
    new_keys = list()
    for i in range(len(session.unscramble_data)):
        n = session.unscramble_data[i]
        if n == int(callback_data['data']):
            revield = revield + ' ' + session.unscramble_keys[i]
            continue
        new_data.append(n)
        new_keys.append(session.unscramble_keys[i])
    await do_unscramble(session, new_keys, new_data, session.unscramble_sentence, revield, m)



async def do_unscramble(session, keys, data, sentence, revieled, message):
    actions = ['unscramble'] * len(data)
    k = bot_utils.to_vertical_keyboard(keys, data, actions)
    # await message.edit_reply_markup(k)
    await message.edit_text("*" + sentence[1] + "*" + "\n" + revieled, reply_markup=k)
    session.unscramble_keys = keys
    session.unscramble_data = data
    session.unscramble_revieled = revieled
    session.unscramble_sentence = sentence


async def unscrumble(session, sentence):
    m = await bot.send_message(session.get_user_id(),
                           "Put the words in correct order")
    # tokens = mysql_connect.get_words_for_sentence(sentence[3])
    tokens = sentence[0].split(' ')
    keys = list()
    data = list()
    action=list()
    for i in range(len(tokens)):
        token = tokens[i].strip()
        if len(token) == 0:
            continue
        keys.append(token)
        data.append(i)
        action.append('unscramble')
    c = list(zip(keys, data))
    random.shuffle(c)
    keys, data = zip(*c)
    await do_unscramble(session, keys, data, sentence, "", m)