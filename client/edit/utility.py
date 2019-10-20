import logging
import re

from time import perf_counter


# TeamRome
def check_input_str(string: str, title=True) -> str or None:
    """ pattern: одно-два слова, слова с русскими и английскими буквами,
    апострафами, двойние слова, слова с цыфрами"""
    if re.match("^[a-zA-Zа-яА-Я0-9'-_]{1,100}[ ]?[-]?[a-zA-Zа-яА-Я0-9'-_]{0,100}$", string):
        print("\tcheck_input_str(): %s" % string)
        if title:
            return string.title()
        else:
            return string
    else:
        logging.error("\tcheck_input_str() Fail: %s" % string)
        return None


# TeamRome
def check_telegram(string: str) -> str or None:
    """ pattern: @tele, @123qwe, @qwe12, @asd11_sd1 """
    if re.match("^[@][a-zA-Zа-яА-Я_0-9]{1,100}$", string):
        print("\tcheck_telegram(): %s" % string)
        return string
    else:
        logging.error("\tcheck_telegram() Fail: %s" % string)
        return None


# TeamRome
def check_home_number(string: str) -> str or None:
    """ pattern: 12/4, 13-4, 1a, f/2, 5/e, 6-y """
    if re.match("^[0-9a-zA-Zа-яА-Я/-]{1,10}$", string):
        print("\tcheck_home_number(): %s" % string)
        return string
    else:
        logging.error("\tcheck_home_number() Fail: %s" % string)
        return None


# TeamRome
def check_phone(phone: str) -> str or None:
    """ pattern: +375291234567 """
    if re.match("^[+][0-9]{1,20}$", phone):
        print("\tcheck_phone(): %s" % phone)
        return phone
    else:
        logging.error("\tcheck_phone() Fail: %s" % phone)
        return None


# TeamRome
def check_if_str(string: str, out: str or None) -> str:
    print("check_if_str()")
    if string:
        return string
    else:
        return out


# TeamRome
def try_except(foo):
    """ Handle exceptions in a selected function = foo_name. """

    def wrapper(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except Exception as ex:
            logging.error("\tException in - %s()\n\t%s" % (foo.__name__, ex))
            return None

    return wrapper


# TeamRome
def time_it(foo):
    """ Return the value (in fractional seconds) of a performance counter for a function = foo_name. """

    def wrapper(*args, **kwargs):
        time_0 = perf_counter()
        print("%s()" % foo.__name__)
        result = foo(*args, **kwargs)
        print('\t%s() - OK; Time: %s sec.' % (foo.__name__, perf_counter() - time_0))
        return result

    return wrapper
