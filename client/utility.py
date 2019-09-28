import logging
import re


def check_input_str(string: str) -> str or None:
    """ pattern: одно-два слова, слова с русскими и английскими буквами,
    апострафами, двойние слова, слова с цыфрами"""
    if re.match("^[a-zA-Zа-яА-Я0-9'-_]{1,100}[ ]?[-]?[a-zA-Zа-яА-Я0-9'-_]{0,100}$", string):
        print("string checked: %s" % string)
        return string.title()
    else:
        logging.error("String Pattern Fail: %s" % string)
        return None


def check_telegram(string: str) -> str or None:
    """ pattern: @tele, @123qwe, @qwe12, @asd11_sd1 """
    if re.match("^[@][a-zA-Zа-яА-Я_0-9]{1,100}$", string):
        print("telegram checked: %s" % string)
        return string
    else:
        logging.error("telegram Pattern Fail: %s" % string)
        return None


def check_home_number(string: str) -> str or None:
    """ pattern: 12/4, 13-4, 1a, f/2, 5/e, 6-y """
    if re.match("^[0-9a-zA-Zа-яА-Я/-]{1,10}$", string):
        print("home_number checked: %s" % string)
        return string
    else:
        logging.error("home_number Pattern Fail: %s" % string)
        return None


def check_phone(phone: str) -> str or None:
    """ pattern: +375291234567 """
    if re.match("^[+][0-9]{1,20}$", phone):
        print("phone: %s" % phone)
        return phone
    else:
        logging.error("Phone Pattern Fail: %s" % phone)
        return None


def pars_exp_request(req_post) -> list:
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели Experience. """
    # print("exp_request.POST: %s" % req_post)
    from time import perf_counter
    time_0 = perf_counter()

    arr = []
    dict_up = {'experience_1': '', 'experience_2': '', 'experience_3': '',
               'exp_date_start': '', 'exp_date_end': '', 'experience_4': ''}
    for i in req_post.items():
        # print("i: %s, %s" % (i[0], i[1]))

        if re.match('experience_1', i[0]):
            dict_up['experience_1'] = i[1]

        if re.match('experience_2', i[0]):
            dict_up['experience_2'] = req_post.getlist('experience_2')  # TODO: bug

        if re.match('experience_3', i[0]):
            dict_up['experience_3'] = i[1]

        if re.match('exp_date_start', i[0]):
            dict_up['exp_date_start'] = i[1]

        if re.match('exp_date_end', i[0]):
            dict_up['exp_date_end'] = i[1]

        if re.match('experience_4', i[0]):
            dict_up['experience_4'] = i[1]

            # print(dict_up)
            arr.append(dict_up)
            dict_up = {'experience_1': '', 'experience_2': '', 'experience_3': '',
                       'exp_date_start': '', 'exp_date_end': '', 'experience_4': ''}
            # print('----')

    print('time_it = %s sec' % (perf_counter() - time_0))
    print("arr: %s" % arr)
    return arr


def pars_cv_request(req_post: dict) -> list:
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели CV. """
    # print("exp_request.POST: %s" % req_post)
    from time import perf_counter
    time_0 = perf_counter()

    arr = []
    dict_up = {'position': '', 'employment': '', 'time_job': '', 'salary': '', 'type_salary': ''}
    for i in req_post.items():
        # print("i: %s, %s" % (i[0], i[1]))

        if re.match('position', i[0]):
            dict_up['position'] = i[1]

        if re.match('employment', i[0]):
            dict_up['employment'] = i[1]

        if re.match('time_job', i[0]):
            dict_up['time_job'] = i[1]

        if re.match('salary', i[0]):
            dict_up['salary'] = i[1]

        if re.match('type_salary', i[0]):
            dict_up['type_salary'] = i[1]

            # print(dict_up)
            arr.append(dict_up)
            dict_up = {'position': '', 'employment': '', 'time_job': '', 'salary': '', 'type_salary': ''}
            # print('----')

    print('time_it = %s sec' % (perf_counter() - time_0))
    print("arr: %s" % arr)
    return arr


def pars_edu_request(req_post, _file) -> list:
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели Education. """
    # print("exp_request.POST: %s" % req_post)
    # print("exp_request.FILE: %s" % _file)
    from time import perf_counter
    time_0 = perf_counter()

    arr = []
    dict_up = {'institution': '', 'subject_area': '', 'specialization': '', 'qualification': '',
               'date_start': '', 'date_end': '', 'certificate_img': '', 'certificate_url': ''}
    count = 0
    for i in req_post.items():
        # print("i: %s, %s" % (i[0], i[1]))

        if re.match('institution', i[0]):
            dict_up['institution'] = i[1]

        if re.match('subject_area', i[0]):
            dict_up['subject_area'] = i[1]

        if re.match('specialization', i[0]):
            dict_up['specialization'] = i[1]

        if re.match('qualification', i[0]):
            dict_up['qualification'] = i[1]

        if re.match('date_start', i[0]):
            dict_up['date_start'] = i[1]

        if re.match('date_end', i[0]):
            dict_up['date_end'] = i[1]

        if re.match('certificate_url', i[0]):
            dict_up['certificate_url'] = i[1]  # req_post.getlist('certificate_url')

            """ request.FILE == MultiValueDict{'key': [<InMemoryUploadedFile: x.png (image/png)>]} """
            for f in _file.items():
                if re.match('certificate_img[0-9]?', f[0]):
                    if (str(f[0])[-1] == str(count)) or (count == 0):
                        dict_up['certificate_img'] = f[1]
                        break

            # print(dict_up)
            arr.append(dict_up)
            dict_up = {'institution': '', 'subject_area': '', 'specialization': '', 'qualification': '',
                       'date_start': '', 'date_end': '', 'certificate_img': '', 'certificate_url': ''}
            count += 1
            # print('----')

    print('time_it = %s sec' % (perf_counter() - time_0))
    print("arr: %s" % arr)
    return arr
