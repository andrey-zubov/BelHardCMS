import re


def pars_exp_request(req_post) -> list:
    Rec_arr = []
    dict_up = {'experience_1': '', 'experience_2': '', 'experience_3': '',
               'exp_date_start': '', 'exp_date_end': '', 'experience_4': ''}
    count = 0
    for i in dict(req_post).items():
        if re.match('experience_11', i[0]):
            dict_up['experience_1'] = i[1][0]

        elif re.match('experience_21', i[0]):
            if count:
                dict_up['experience_2'] = req_post.getlist('experience_21%s' % count)
            else:
                dict_up['experience_2'] = req_post.getlist('experience_21')

        elif re.match('experience_31', i[0]):
            dict_up['experience_3'] = i[1][0]

        elif re.match('exp_date_start1', i[0]):
            dict_up['exp_date_start'] = i[1][0] if i[1][0] else None

        elif re.match('exp_date_end1', i[0]):
            dict_up['exp_date_end'] = i[1][0] if i[1][0] else None

        elif re.match('experience_41', i[0]):
            dict_up['experience_4'] = i[1][0]

            Rec_arr.append(dict_up)
            print("\tdict_up: %s" % dict_up)
            dict_up = {'experience_1': '', 'experience_2': '', 'experience_3': '',
                       'exp_date_start': '', 'exp_date_end': '', 'experience_4': ''}
            count += 1
            # print('\t----')
    print("\tout_arr: %s" % Rec_arr)

    return Rec_arr
