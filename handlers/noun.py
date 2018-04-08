import re
import lib
import tools
from handlers import Nom


def reduced(d, case, num, gen):

    if (
            d in ('a', 'ja') and (case, num) == ('род', 'мн')
            or d in ('o', 'jo') and gen == 'м' and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
            or d in ('o', 'jo') and gen == 'ср' and (case, num) == ('род', 'мн')
            or d in ('i', 'u') and (case, num) not in (('им', 'ед'), ('вин', 'ед'))
            or d.startswith('e') and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
            or d == 'uu' and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
    ):
        return True

    return False


def de_reduce_manual(s, nb):

    if '+о' in nb:
        s = s[:-1] + 'О' + s[-1]
    elif '+е' in nb:
        s = s[:-1] + 'Е' + s[-1]
    else:
        s = s[:-2] + s[-1]

    return s


def de_reduce_auto(s, d):

    if d == 'ja' and s[-2] == 'Е':
        s = s[:-2] + s[-1]
    elif d == 'jo' and s[-2] in lib.cons:
        s = s[:-1] + 'Е' + s[-1]

    return s


def decl_spec_modif(stem, decl, new_decl, nb):

    def de_suffix(s, d, nd):

        for th in lib.them_suff:
            if th in (d, nd):
                suf = re.search(lib.them_suff[th], s)

                if suf:
                    s = s[:-len(suf.group())]

        return s

    def add_suffix(s, d):
        if d == 'en' and not (s.endswith('ЕН') or re.match('Д[ЪЬ]?Н', s)):
            suf = re.search(lib.them_suff[d], s)
            if suf:
                s = s[:-len(suf.group())]

            s += 'ЕН'

        elif d == 'uu' and not s.endswith('ОВ'):
            suf = re.search(lib.them_suff[d], s)
            if suf:
                s = s[:-len(suf.group())]

            s += 'ОВ'

        return s

    # Удаление/добавление тематических суффиксов
    if {decl, new_decl} & {'ent', 'men', 'es', 'er'}:
        stem = de_suffix(stem, decl, new_decl)
    elif decl in ('en', 'uu'):
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
    gr = Nom(token)

    # Проверка на исключительность
    for key in lib.noun_spec:
        if re.match(key, gr.form):
            return ('', lib.noun_spec[key][0]), lib.noun_spec[key][1]

    # Стемминг (с учётом особого смешения)
    if gr.d_new in ('a', 'ja', 'i') and gr.gen == 'ср':
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, 'м'), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)

    s_new = s_old

    # Проверка на склоняемость второй части
    s_new, grd = grd_check(s_new, gr.prop)
    if grd:
        s_new = tools.find_stem(s_new, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)

    # Обработка основы
    if s_new == 'NONE':
        return ('', 'NONE'), ''

    # Модификации по типам склонения и другие
    s_new = decl_spec_modif(s_new, gr.d_old, gr.d_new, gr.nb)

    # Первая палатализация
    if s_new[-1] in 'ЧЖШ' and ((gr.case, gr.num, gr.gen) == ('зв', 'ед', 'м') or s_new in ('ОЧ', 'УШ')):
        if (gr.d_old, gr.d_new) == ('jo', 'o'):
            s_new = s_new[:-1] + lib.palat_1_jo[s_new[-1]]
        else:
            s_new = s_new[:-1] + lib.palat_1[s_new[-1]]

    # Вторая палатализация
    elif '*' in gr.nb and s_new[-1] in 'ЦЗСТ':
        s_new = s_new[:-1] + lib.palat_2[s_new[-1]]

    # Прояснение/исчезновение редуцированных
    if any(tag in gr.nb for tag in ('+о', '+е', '-о', '-е')):
        s_new = de_reduce_manual(s_new, gr.nb)
    elif s_new[-1] == 'Ц' and reduced(gr.d_new, gr.case, gr.num, gr.gen):
        s_new = de_reduce_auto(s_new, gr.d_old)

    # 'НОВЪ' --> 'НОВГОРОДЪ'; 'ЦАРЬ' --> 'ЦАРГРАДЪ' (?)
    if grd:
        s_new += grd

    # Возвращение маркера одушевлённости
    if gr.prop:
        s_old = '*' + s_old
        s_new = '*' + s_new

    # Нахождение флексии
    infl = noun_infl(s_new, gr.pt, gr.d_old, gr.gen)

    return (s_old, s_new), infl
