import tools
import lib
import re
from handlers.noun import noun_infl


def get_params(t):

    form = t.reg.replace('(', '').replace(')', '')
    pos = t.ana[0]

    if pos == 'мест':
        zhe = bool(form.endswith('ЖЕ'))
        if zhe:
            form = form.replace('ЖЕ', '')

        neg = re.match('Н[+ЕИ](?=[КЧ])', form)
        if neg:
            form = form[2:]
    else:
        zhe = False
        neg = False

    if form[-1] not in lib.vows:
        form += '`'

    if '/' in t.ana[1] and t.ana[1] != 'р/скл':
        decl = t.ana[1][:t.ana[1].index('/')]
        new_decl = t.ana[1][t.ana[1].index('/') + 1:]
    else:
        decl = new_decl = t.ana[1]

    case = t.ana[2][t.ana[2].find('/') + 1:]

    num = t.ana[3][t.ana[3].find('/') + 1:]

    if t.ana[4] == '0':
        gen = 'м'
    else:
        gen = t.ana[4][t.ana[4].find('/') + 1:]

    nb = t.ana[5]

    return form, pos, zhe, neg, decl, new_decl, case, num, gen, nb


def pron_modif(s):

    x = re.match('([ВН])[ЪЬ]?Ш', s)
    if x:
        return '%sАШ' % x.group(1)

    elif re.match('В[ЪЬ]?С$', s):
        return 'ВЕС'

    # 'КИИ' // 'КОЕГО'
    elif s == 'КО':
        return 'К'

    # Предложные формы местоимения 'И'
    elif s == 'Н':
        return ''

    # Морфемная реинтерпретация
    elif s in ('М', 'Т', 'ТВ', 'СВ'):
        return s + 'О'

    # 'СИИ' // 'СЕГО'
    elif s == 'С':
        return s + 'Е'

    return s


def pron_infl(s, decl):

    if decl in ('a', 'o', 'тв'):
        if s.endswith(lib.vows):
            return 'И'
        else:
            return 'Ъ'

    else:
        if s.endswith(lib.vows) or s == '':
            return 'И'
        elif s.endswith(lib.cons_hush + ('С', 'З')):
            return 'Ь'
        else:
            return 'Ъ'


def pron_adj_infl(s):

    if s.endswith(lib.cons_palat):
        return 'ИИ'
    else:
        return 'ЫИ'


def num_infl(s, decl, gen):

    if decl in ('тв', 'м'):
        if s.startswith('ЕДИН'):
            return 'Ъ'
        elif re.match('(Д[ЪЬ]?В|ОБ)$', s):
            return 'А'
        # Тут остаются собирательные и нумерализованные прилагательные
        else:
            if s.endswith(lib.vows):
                return 'Е'
            else:
                return 'О'

    else:
        if s.startswith('ТР'):
            return 'И'
        elif s.startswith('ЧЕТЫР'):
            return 'Е'
        else:
            return noun_infl(s, False, decl, gen)


def main(token):
    form, pos, zhe, neg, decl, new_decl, case, num, gen, nb = get_params(token)

    if pos == 'мест':
        # Проверка на исключительность
        if re.search('Ж[ЪЬ]?Д[ЕО]$', form):
            return ('', 'КОЖДО'), ''

        # Проверка на вопросительность
        for key in lib.pron_interr:
            if re.match(key[0], form) and (decl, case) == key[1]:
                return ('', lib.pron_interr[key]), ''
    else:
        # Проверка на изменяемость обеих частей
        for key in lib.num_spec:
            if re.match(key, form):
                return ('', lib.num_spec[key]), ''

    if decl != 'р/скл':
        # Сначала ищем в местоименной парадигме
        s_old = tools.find_stem(form, (new_decl, case, num, gen), lib.pron_infl)

        # Если не нашли, то обращаемся к именной. Актуально прежде всего для им. и вин. п., но бывает всякое
        if s_old == 'NONE':

            if new_decl == 'тв':
                if gen in ('м', 'ср'):
                    # Если склонение 'тв', а род 'м' или 'ср', то ищем так, как если бы склонение было 'o'
                    s_old = tools.find_stem(form, ('o', case, num, gen), lib.nom_infl)
                else:
                    # Аналогично: 'тв' и 'ж' --> 'a'
                    s_old = tools.find_stem(form, ('a', case, num, gen), lib.nom_infl)

            elif new_decl == 'м':
                if gen in ('м', 'ср'):
                    # Аналогично: 'м' и 'м'/'ср' --> 'jo'
                    s_old = tools.find_stem(form, ('jo', case, num, gen), lib.nom_infl)
                else:
                    # Аналогично: 'м' и 'ж' --> 'ja'
                    s_old = tools.find_stem(form, ('ja', case, num, gen), lib.nom_infl)

            else:
                # If all else fails, проверяем именную парадигму. Особо актуально для числительных
                if new_decl in ('a', 'ja', 'i') and gen == 'ср':
                    s_old = tools.find_stem(form, (new_decl, case, num, 'м'), lib.nom_infl)
                else:
                    s_old = tools.find_stem(form, (new_decl, case, num, gen), lib.nom_infl)

    else:

        if (case, num, gen) in (('тв', 'ед', 'м'), ('тв', 'ед', 'ср')) or num == 'мн':
            # В этих позициях парадигмы тип твёрдый
            s_old = tools.find_stem(form, ('тв', case, num, gen), lib.pron_infl)
        else:
            # В этих мягкий
            s_old = tools.find_stem(form, ('м', case, num, gen), lib.pron_infl)

        # Опять же, в им./вин. (стандартно) обращаемся к именной парадигме
        if s_old == 'NONE':

            if gen in ('м', 'ср'):
                s_old = tools.find_stem(form, ('jo', case, num, gen), lib.nom_infl)
            else:
                s_old = tools.find_stem(form, ('ja', case, num, gen), lib.nom_infl)

    s_new = s_old

    if s_new != 'NONE':
        # Модификация основы
        if pos == 'мест':
            s_new = pron_modif(s_new)

        # Плюс-минус
        s_new = tools.plus_minus(s_new, nb)

        # Отмена палатализации
        if '*' in nb:
            s_new = tools.de_palat(s_new, decl, new_decl)

        # Нахождение флексии
        if pos == 'мест':
            if s_new not in ('К', 'КОТОР'):
                infl = pron_infl(s_new, decl)
            else:
                infl = pron_adj_infl(s_new)
        else:
            infl = num_infl(s_new, decl, gen)

    else:
        infl = ''

    if s_new != 'NONE' and pos == 'мест':
        if zhe:
            infl += 'ЖЕ'

        if neg:
            s_new = neg.group() + s_new

        # Префикс НИ- тут отсечён предлогом
        if s_new in ('КТО', 'ЧТО') and zhe:
            s_new = 'НИ' + s_new

    return (s_old, s_new), infl
