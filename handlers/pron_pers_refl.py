import lib
import re


def get_params(t):

    form = t.form

    if form[-1] not in lib.vows:
        form += 'Ъ'

    pers = t.pers

    if '/' in t.case:
        case = t.case[t.case.index('/') + 1:]
    else:
        case = t.case

    if pers != 'возвр':

        if '/' in t.num:
            num = t.num[t.num.index('/') + 1:]
        else:
            num = t.num

    else:
        num = ''

    return form, pers, case, num


def main(token):

    form, pers, case, num = get_params(token)
    stem = 'NONE'

    if pers != 'возвр':
        for key in lib.pron_pers.keys():
            if re.match(key[0], form) and (pers, case, num) == key[1]:
                stem = lib.pron_pers[key]
                break
    else:
        for key in lib.pron_refl.keys():
            if re.match(key[0], form) and case == key[1]:
                stem = lib.pron_refl[key]
                break

    return stem, ''
