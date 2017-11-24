import re
import lib
import tools
from handlers import adj_noun_tools


def decl_spec_modif(stem, decl, new_decl, nb):

    def de_suffix(s, d, nd):

        them_suff = {
            'men': '([ЕЯ]|[ЪЬ]?)Н$',
            'ent': '[АЯ]Т$',
            'es': '(Е|[ЪЬ]?)С$',
            'er': '(Е|[ЪЬ]?)Р$',
        }

        for th in them_suff:
            if th in (d, nd):
                suf = re.search(them_suff[th], s)

                if suf:
                    s = s[:-len(suf.group())]

        return s

    def add_suffix(s, d):

        # Единственное мерзкое исключение
        if d == 'en' and not s.endswith('ЕН'):
            if not re.match('Д[ЕЪЬ]?Н', s):

                suf = re.search('[ЪЬ]?Н$', s)
                if suf:
                    s = s[:-len(suf.group())]

                s += 'ЕН'

        elif d == 'uu' and not s.endswith('ОВ'):
            suf = re.search('[ЪЬ]?В$', s)
            if suf:
                s = s[:-len(suf.group())]

            s += 'ОВ'

        return s

    # Удаление/добавление тематических суффиксов
    if {decl, new_decl} & {'ent', 'men', 'es', 'er'}:
        stem = de_suffix(stem, decl, new_decl)

    if decl in ('en', 'uu'):
        stem = add_suffix(stem, decl)

    # Плюс-минус
    stem = tools.plus_minus(stem, nb)

    if stem == 'ХРИСТ':
        stem += 'ОС'

    # Для слова 'БРАТЪ' во мн. ч. - минус Ь или И
    if (decl, new_decl) == ('o', 'ja'):
        stem = stem[:-1]

    # Для гетероклитик на -ин- во мн. ч.
    if (decl, new_decl) == ('o', 'en') and not stem.endswith(('АР', 'ТЕЛ')):
        stem += 'ИН'

    return stem


def noun_infl(s, pt, decl, gen):

    if not pt:

        if decl == 'a':
            return 'А'

        elif decl == 'ja':
            if s.endswith(lib.cons_hush):
                return 'А'
            else:
                return 'Я'

        elif decl == 'o':
            if gen == 'м':
                return 'Ъ'
            elif gen == 'ср':
                return 'О'

        elif decl == 'jo':
            if gen == 'м':
                if s.endswith(lib.cons_soft + lib.cons_hush):
                    return 'Ь'
                else:
                    return 'И'
            elif gen == 'ср':
                return 'Е'

        elif decl == 'u':
            return 'Ъ'

        elif decl == 'i':
            return 'Ь'

        elif decl == 'en':
            return 'Ь'

        elif decl == 'men':
            return 'Я'

        elif decl == 'ent':
            if s.endswith(lib.cons_hush):
                return 'А'
            else:
                return 'Я'

        elif decl == 'er':
            return 'И'

        elif decl == 'es':
            return 'О'

        else:
            return 'Ь'

    else:

        if decl == 'a':
            return 'Ы'

        elif decl == 'o':
            return 'А'

        else:
            if gen == 'м':
                return 'ИЕ'
            else:
                return 'И'


def grd_check(s, prop):
    grd = ''

    if prop:
        x = re.search('(ГРАД|ГОРОД)$', s)
        if x:
            s = s[:x.start()]
            grd = x.group()

    return s, grd


def main(token):
    # Извлечение данных по токену
    form, prop, pos, decl, new_decl, case, num, pt, gen, nb = adj_noun_tools.get_params(token)

    # Проверка на исключительность
    for key in lib.noun_spec:
        if re.match(key, form):
            return ('', lib.noun_spec[key]), ''

    # Стемминг (с учётом особого смешения)
    if new_decl in ('a', 'ja', 'i') and gen == 'ср':
        s_old = tools.find_stem(form, (new_decl, case, num, 'м'), lib.nom_infl)
    else:
        s_old = tools.find_stem(form, (new_decl, case, num, gen), lib.nom_infl)

    s_new = s_old

    # Проверка на склоняемость второй части
    s_new, grd = grd_check(s_new, prop)
    if grd:
        s_new = tools.find_stem(s_new, (new_decl, case, num, gen), lib.nom_infl)

    # Обработка основы
    if s_new != 'NONE':
        # Модификации по типам склонения и другие
        s_new = decl_spec_modif(s_new, decl, new_decl, nb)

        # Отмена палатализации
        if '*' in nb:
            s_new = tools.de_palat(s_new, decl, new_decl)

        # Прояснение/исчезновение редуцированных
        if (any(tag in nb for tag in ('+о', '+е', '-о', '-е'))
                or adj_noun_tools.reduction_on(pos, new_decl, case, num, gen)):
            s_new = adj_noun_tools.de_reduce(s_new, pos, decl, nb)

        # 'НОВЪ' --> 'НОВГОРОДЪ'; 'ЦАРЬ' --> 'ЦАРГРАДЪ' (?)
        if grd:
            s_new += grd

        # Возвращение маркера одушевлённости
        if prop:
            s_old = '*' + s_old
            s_new = '*' + s_new

        # Нахождение флексии
        infl = noun_infl(s_new, pt, decl, gen)

    else:
        infl = ''

    return (s_old, s_new), infl
