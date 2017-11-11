import lib
import re


def get_params(t):

    form = t.reg.replace('(', '').replace(')', '')

    if form[-1] not in lib.vows:
        form += 'Ъ'

    pers = t.ana[2]
    case = t.ana[3][t.ana[3].find('/') + 1:]

    if pers != 'возвр':
        num = t.ana[4][t.ana[4].find('/') + 1:]
    else:
        num = ''

    return form, pers, case, num


def main(token):

    form, pers, case, num = get_params(token)
    stem = 'NONE'

    if pers != 'возвр':
        for key in lib.pron_pers:
            if re.match(key[0], form) and (pers, case, num) == key[1]:
                stem = lib.pron_pers[key]
                break
    else:
        for key in lib.pron_refl:
            if re.match(key[0], form) and case == key[1]:
                stem = lib.pron_refl[key]
                break

    return stem, ''
