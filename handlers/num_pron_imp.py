import tools
import lib
import re
from handlers import Nom
from handlers.noun import noun_infl
from handlers.adj import adj_pron_infl


def stem_modif(s):

    if re.match('В[ЪЬ]?С$', s):
        return 'ВЕС'
    elif re.match('В[ЪЬ]?Ш$', s):
        return 'ВАШ'
    elif re.match('Н[ЪЬ]?Ш$', s):
        return 'НАШ'
    elif re.match('(К|ОБ|М|СВ|Т|ТВ)О$', s):
        return s[:-1]
    elif s in ('С', 'СИ'):
        return 'СЕ'
    elif s == 'Н':
        return ''

    return s


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


def neg(s, gr):

    if gr.neg is not None:
        return gr.neg.group() + s

    # Префикс тут отсечён предлогом
    elif s in ('КТО', 'ЧТО') and gr.zhe is not None:
        return 'НИ' + s

    return s


def zhe(i, gr):

    if gr.zhe is not None:
        return i + gr.zhe.group()

    return i


def main(token):
    gr = Nom(token)

    if gr.pos == 'мест':
        # Проверка на исключительность
        if re.match('К[ОЪ]$', gr.form):
            if gr.zhe is not None and 'Д' in gr.zhe.group():
                return ('', neg('КО', gr)), zhe('', gr)

        # Проверка на вопросительность
        if (gr.d_old, gr.case) in lib.pron_interr:
            if re.match(lib.pron_interr[(gr.d_old, gr.case)][0], gr.form):
                if gr.zhe is not None and 'Д' in gr.zhe.group():
                    return ('', neg('КО', gr)), zhe('', gr)
                else:
                    return ('', neg(lib.pron_interr[(gr.d_old, gr.case)][1], gr)), zhe('', gr)

    else:
        # Проверка на изменяемость обеих частей
        for key in lib.num_spec:
            if re.match(key, gr.form):
                return ('', lib.num_spec[key]), ''

    if gr.d_old != 'р/скл':
        # Сначала ищем в местоименной парадигме
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

        # Если не нашли, то обращаемся к именной. Актуально прежде всего для им. и вин. п., но бывает всякое
        if s_old == 'NONE':

            if gr.d_new == 'тв':
                if gr.gen in ('м', 'ср'):
                    # Если склонение 'тв', а род 'м' или 'ср', то ищем так, как если бы склонение было 'o'
                    s_old = tools.find_stem(gr.form, ('o', gr.case, gr.num, gr.gen), lib.nom_infl)
                else:
                    # Аналогично: 'тв' и 'ж' --> 'a'
                    s_old = tools.find_stem(gr.form, ('a', gr.case, gr.num, gr.gen), lib.nom_infl)

            elif gr.d_new == 'м':
                if gr.gen in ('м', 'ср'):
                    # Аналогично: 'м' и 'м'/'ср' --> 'jo'
                    s_old = tools.find_stem(gr.form, ('jo', gr.case, gr.num, gr.gen), lib.nom_infl)
                else:
                    # Аналогично: 'м' и 'ж' --> 'ja'
                    s_old = tools.find_stem(gr.form, ('ja', gr.case, gr.num, gr.gen), lib.nom_infl)

            else:
                # If all else fails, проверяем именную парадигму. Особо актуально для числительных
                if gr.d_new in ('a', 'ja', 'i') and gr.gen == 'ср':
                    s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, 'м'), lib.nom_infl)
                else:
                    s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)

    else:

        if (gr.case, gr.num, gr.gen) in (('тв', 'ед', 'м'), ('тв', 'ед', 'ср')) or gr.num == 'мн':
            # В этих позициях парадигмы тип твёрдый
            s_old = tools.find_stem(gr.form, ('тв', gr.case, gr.num, gr.gen), lib.pron_infl)
        else:
            # В этих мягкий
            s_old = tools.find_stem(gr.form, ('м', gr.case, gr.num, gr.gen), lib.pron_infl)

        # Опять же, в им./вин. (стандартно) обращаемся к именной парадигме
        if s_old == 'NONE':

            if gr.gen in ('м', 'ср'):
                s_old = tools.find_stem(gr.form, ('jo', gr.case, gr.num, gr.gen), lib.nom_infl)
            else:
                s_old = tools.find_stem(gr.form, ('ja', gr.case, gr.num, gr.gen), lib.nom_infl)

    s_new = s_old

    if s_new == 'NONE':
        return ('', 'NONE'), ''

    # Модификация основы
    s_new = stem_modif(s_new)

    # Плюс-минус
    s_new = tools.plus_minus(s_new, gr.nb)

    # Вторая палатализация
    if '*' in gr.nb and s_new[-1] in 'ЦЗСТ':
        s_new = s_new[:-1] + lib.palat_2[s_new[-1]]

    # Нахождение флексии
    if gr.pos == 'мест':
        if s_new in lib.pron_spec:
            infl = lib.pron_spec[s_new]
        else:
            infl = adj_pron_infl(s_new, gr.d_old)
    else:
        infl = num_infl(s_new, gr.d_old, gr.gen)

    return (s_old, neg(s_new, gr)), zhe(infl, gr)
