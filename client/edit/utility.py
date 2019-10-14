import logging
import re


# TeamRome
def check_input_str(string: str, title=True) -> str or None:
    """ pattern: одно-два слова, слова с русскими и английскими буквами,
    апострафами, двойние слова, слова с цыфрами"""
    if re.match("^[a-zA-Zа-яА-Я0-9'-_]{1,100}[ ]?[-]?[a-zA-Zа-яА-Я0-9'-_]{0,100}$", string):
        print("check_input_str(): %s" % string)
        if title:
            return string.title()
        else:
            return string
    else:
        logging.error("check_input_str() Fail: %s" % string)
        return None


# TeamRome
def check_telegram(string: str) -> str or None:
    """ pattern: @tele, @123qwe, @qwe12, @asd11_sd1 """
    if re.match("^[@][a-zA-Zа-яА-Я_0-9]{1,100}$", string):
        print("check_telegram(): %s" % string)
        return string
    else:
        logging.error("check_telegram() Fail: %s" % string)
        return None


# TeamRome
def check_home_number(string: str) -> str or None:
    """ pattern: 12/4, 13-4, 1a, f/2, 5/e, 6-y """
    if re.match("^[0-9a-zA-Zа-яА-Я/-]{1,10}$", string):
        print("check_home_number(): %s" % string)
        return string
    else:
        logging.error("check_home_number() Fail: %s" % string)
        return None


# TeamRome
def check_phone(phone: str) -> str or None:
    """ pattern: +375291234567 """
    if re.match("^[+][0-9]{1,20}$", phone):
        print("check_phone(): %s" % phone)
        return phone
    else:
        logging.error("check_phone() Fail: %s" % phone)
        return None


# TeamRome
def check_if_str(string: str, out: str or None) -> str:
    print("check_if_str()")
    if string:
        return string
    else:
        return out
