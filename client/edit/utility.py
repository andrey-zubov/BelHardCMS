import logging
import re


# TeamRome
def check_input_str(string: str) -> str or None:
    """ pattern: одно-два слова, слова с русскими и английскими буквами,
    апострафами, двойние слова, слова с цыфрами"""
    if re.match("^[a-zA-Zа-яА-Я0-9'-_]{1,100}[ ]?[-]?[a-zA-Zа-яА-Я0-9'-_]{0,100}$", string):
        print("string checked: %s" % string)
        return string.title()
    else:
        logging.error("String Pattern Fail: %s" % string)
        return None


# TeamRome
def check_telegram(string: str) -> str or None:
    """ pattern: @tele, @123qwe, @qwe12, @asd11_sd1 """
    if re.match("^[@][a-zA-Zа-яА-Я_0-9]{1,100}$", string):
        print("telegram checked: %s" % string)
        return string
    else:
        logging.error("telegram Pattern Fail: %s" % string)
        return None


# TeamRome
def check_home_number(string: str) -> str or None:
    """ pattern: 12/4, 13-4, 1a, f/2, 5/e, 6-y """
    if re.match("^[0-9a-zA-Zа-яА-Я/-]{1,10}$", string):
        print("home_number checked: %s" % string)
        return string
    else:
        logging.error("home_number Pattern Fail: %s" % string)
        return None


# TeamRome
def check_phone(phone: str) -> str or None:
    """ pattern: +375291234567 """
    if re.match("^[+][0-9]{1,20}$", phone):
        print("phone: %s" % phone)
        return phone
    else:
        logging.error("Phone Pattern Fail: %s" % phone)
        return None


# TeamRome
def check_if_str(string: str, out: str or None) -> str:
    if string:
        return string
    else:
        return out
