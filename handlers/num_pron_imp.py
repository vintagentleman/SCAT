import tools
import lib
import re
from handlers.noun import noun_fl


def get_params(t):

    form = t.form
    pos = t.pos
    nb = t.nb

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

    if '/' in t.decl and t.decl != 'р/скл':
        decl = t.decl[:t.decl.index('/')]
        new_decl = t.decl[t.decl.index('/') + 1:]
    else:
        decl = new_decl = t.decl

    if '/' in t.case:
        case = t.case[t.case.index('/') + 1:]
    else:
        case = t.case

    if '/' in t.num:
        num = t.num[t.num.index('/') + 1:]
    else:
        num = t.num

    if t.gen == '0':
        gen = 'м'
    elif '/' in t.gen:
        gen = t.gen[t.gen.index('/') + 1:]
    else:
        gen = t.gen

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


def pron_fl(s, decl):

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


def pron_adj_fl(s):

    if s.endswith(lib.cons_palat):
        return 'ИИ'
    else:
        return 'ЫИ'


def num_fl(s, decl, gen):

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
            return noun_fl(s, False, decl, gen)


def main(token):

    form, pos, zhe, neg, decl, new_decl, case, num, gen, nb = get_params(token)
    stem = ''
    fl = ''

    if pos == 'мест':
        # Проверка на исключительность
        if re.search('Ж[ЪЬ]?Д[ЕО]$', form):
            stem = 'КОЖДО'

        # Проверка на вопросительность
        for key in lib.pron_interr.keys():
            if re.match(key[0], form) and (decl, case) == key[1]:
                stem = lib.pron_interr[key]
                break
    else:
        # Проверка на изменяемость обеих частей
        for key in lib.num_spec.keys():
            if re.match(key, form):
                stem = lib.num_spec[key]
                break

    if not stem:

        if decl != 'р/скл':
            # Сначала ищем в местоименной парадигме
            stem = tools.find_stem(form, (new_decl, case, num, gen), lib.pron_infl)

            # Если не нашли, то обращаемся к именной. Актуально прежде всего для им. и вин. п., но бывает всякое
            if stem == 'NONE':

                if new_decl == 'тв':
                    if gen in ('м', 'ср'):
                        # Если склонение 'тв', а род 'м' или 'ср', то ищем так, как если бы склонение было 'o'
                        stem = tools.find_stem(form, ('o', case, num, gen), lib.nom_infl)
                    else:
                        # Аналогично: 'тв' и 'ж' --> 'a'
                        stem = tools.find_stem(form, ('a', case, num, gen), lib.nom_infl)

                elif new_decl == 'м':
                    if gen in ('м', 'ср'):
                        # Аналогично: 'м' и 'м'/'ср' --> 'jo'
                        stem = tools.find_stem(form, ('jo', case, num, gen), lib.nom_infl)
                    else:
                        # Аналогично: 'м' и 'ж' --> 'ja'
                        stem = tools.find_stem(form, ('ja', case, num, gen), lib.nom_infl)

                else:
                    # If all else fails, проверяем именную парадигму. Особо актуально для числительных
                    if new_decl in ('a', 'ja', 'i') and gen == 'ср':
                        stem = tools.find_stem(form, (new_decl, case, num, 'м'), lib.nom_infl)
                    else:
                        stem = tools.find_stem(form, (new_decl, case, num, gen), lib.nom_infl)

        else:

            if (case, num, gen) in (('тв', 'ед', 'м'), ('тв', 'ед', 'ср')) or num == 'мн':
                # В этих позициях парадигмы тип твёрдый
                stem = tools.find_stem(form, ('тв', case, num, gen), lib.pron_infl)
            else:
                # В этих мягкий
                stem = tools.find_stem(form, ('м', case, num, gen), lib.pron_infl)

            # Опять же, в им./вин. (стандартно) обращаемся к именной парадигме
            if stem == 'NONE':

                if gen in ('м', 'ср'):
                    stem = tools.find_stem(form, ('jo', case, num, gen), lib.nom_infl)
                else:
                    stem = tools.find_stem(form, ('ja', case, num, gen), lib.nom_infl)

        if stem != 'NONE':
            # Модификация основы
            if pos == 'мест':
                stem = pron_modif(stem)

            # Плюс-минус
            stem = tools.plus_minus(stem, nb)

            # Отмена палатализации
            if '*' in nb:
                stem = tools.de_palat(stem, decl, new_decl)

            # Нахождение флексии
            if pos == 'мест':
                if stem not in ('К', 'КОТОР'):
                    fl = pron_fl(stem, decl)
                else:
                    fl = pron_adj_fl(stem)
            else:
                fl = num_fl(stem, decl, gen)

    if stem != 'NONE' and pos == 'мест':
        if zhe:
            stem += 'ЖЕ'

        if neg:
            stem = neg.group() + stem

        # Префикс НИ- тут отсечён предлогом
        if stem in ('КТОЖЕ', 'ЧТОЖЕ'):
            stem = 'НИ' + stem

    return stem, fl
