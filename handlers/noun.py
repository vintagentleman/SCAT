import re
import lib
import tools
from handlers import adj_noun_tools


def decl_spec_modif(stem, decl, new_decl, nb):

    def de_suffix(s, decl, new_decl):

        if 'men' in (decl, new_decl):
            suf = re.search('([ЕЯ]|[ЪЬ]?)Н$', s)
            if suf:
                s = s[:-len(suf.group())]

        elif 'ent' in (decl, new_decl):
            suf = re.search('[АЯ]Т$', s)
            if suf:
                s = s[:-len(suf.group())]

        elif 'es' in (decl, new_decl):
            suf = re.search('(Е|[ЪЬ]?)С$', s)
            if suf:
                s = s[:-len(suf.group())]

        else:
            suf = re.search('(Е|[ЪЬ]?)Р$', s)
            if suf:
                s = s[:-len(suf.group())]

        return s

    def add_suffix(s, decl):

        # Единственное мерзкое исключение
        if decl == 'en' and not s.endswith('ЕН'):
            if not re.match('Д[ЕЪЬ]?Н', s):
                suf = re.search('[ЪЬ]?Н$', s)
                if suf:
                    s = s[:-len(suf.group())]

                s += 'ЕН'

        elif decl == 'uu' and not s.endswith('ОВ'):
            suf = re.search('[ЪЬ]?В$', s)
            if suf:
                s = s[:-len(suf.group())]

            s += 'ОВ'

        return s

    # Удаление/добавление тематических суффиксов
    if decl in ('ent', 'men', 'es', 'er') or new_decl in ('ent', 'men', 'es', 'er'):
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


def noun_fl(s, pt, decl, gen):

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

    if prop:
        x = re.search('(ГРАД|ГОРОД)$', s)
        if x:
            s = s[:x.start()]
            grd = x.end() - x.start()
        else:
            grd = 0
    else:
        grd = 0

    return s, grd


def grd_handler(grd):

    if grd == 4:
        return 'ГРАД'
    else:
        return 'ГОРОД'


def main(token):
    # Извлечение данных по токену
    form, prop, pos, decl, new_decl, case, num, pt, gen, nb = adj_noun_tools.get_params(token)
    stem = ''
    fl = ''

    # Проверка на исключительность
    for key in lib.noun_spec:
        if re.match(key, form):
            stem, fl = lib.noun_spec[key], ''
            break

    if not stem:
        # Стемминг (с учётом особого смешения)
        if new_decl in ('a', 'ja', 'i') and gen == 'ср':
            stem = tools.find_stem(form, (new_decl, case, num, 'м'), lib.nom_infl)
        else:
            stem = tools.find_stem(form, (new_decl, case, num, gen), lib.nom_infl)

        # Проверка на склоняемость второй части
        stem, grd = grd_check(stem, prop)
        if grd:
            stem = tools.find_stem(stem, (new_decl, case, num, gen), lib.nom_infl)

        # Обработка основы
        if stem != 'NONE':
            # Модификации по типам склонения и другие
            stem = decl_spec_modif(stem, decl, new_decl, nb)

            # Отмена палатализации
            if '*' in nb:
                stem = tools.de_palat(stem, decl, new_decl)

            # Прояснение/исчезновение редуцированных
            if (any(tag in nb for tag in ('+о', '+е', '-о', '-е'))
                    or adj_noun_tools.reduction_on(pos, new_decl, case, num, gen)):
                stem = adj_noun_tools.de_reduce(stem, pos, decl, nb)

            # 'НОВЪ' --> 'НОВГОРОДЪ'; 'ЦАРЬ' --> 'ЦАРГРАДЪ' (?)
            if grd:
                stem += grd_handler(grd)

            # Возвращение маркера одушевлённости
            if prop:
                stem = '*' + stem

            # Нахождение флексии
            fl = noun_fl(stem, pt, decl, gen)

    return stem, fl
