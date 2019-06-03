from telegram import ReplyKeyboardMarkup
import re
from visulast.core import vars, models, scrappers


def keyboard_to_regex(keyboard):
    res = ""
    for row in keyboard:
        for button in row:
            if button != "Custom":
                res += button + "|"
    return res[:-1]


def convert_period_to_var(period):
    return {
        'Overall': vars.PERIOD_OVERALL,
        'Week': vars.PERIOD_7DAYS,
        'Month': vars.PERIOD_1MONTH,
        '3 Months': vars.PERIOD_3MONTHS,
        '6 Months': vars.PERIOD_6MONTHS,
        'Year': vars.PERIOD_12MONTHS,
    }.get(period, vars.PERIOD_OVERALL)


def is_username_set(context):
    if 'username' in context.user_data.keys() and context.user_data['username'] != '':
        return True
    return False


def get_friends_keyboard(username):
    friends = scrappers.FriendsScrapper.get_friends_by_username(username)
    return ReplyKeyboardMarkup([[friend] for friend in friends])
