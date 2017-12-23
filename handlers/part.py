import re
import lib
import tools
from handlers import Part, verb


def act_past(gr):
    # Стемминг
    if gr.d_old != 'м':
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    s_new = s_old

    if s_new == 'NONE':
        return ('', 'NONE'), ''

    # Удаление словоизменительных суффиксов
    suff = re.search('В$|В?[ЪЬ]?Ш$', s_new)
    if suff:
        s_new = s_new[:-len(suff.group())]

    # Основы-исключения
    for regex in lib.part_spec:
        mo = re.match(regex, s_new)
        if mo:
            s_modif = re.sub(regex, mo.group(1) + lib.part_spec[regex][0], s_new)
            if s_new != s_modif:
                return (s_old, s_modif), lib.part_spec[regex][1]

    # Проблемные классы
    s_modif, infl = verb.cls_cons_modif(s_new)
    if infl:
        return (s_old, s_modif), infl

    jot = bool(s_new.endswith(tuple('ЛНРЖЧШЩ')) or s_new.endswith(('ЖД', 'ШТ')))

    # Сочетания с йотом
    if jot:
        s_new = tools.de_jot(s_new) + 'И'
    # 3*-й класс
    elif s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def pas_past(gr):
    # Стемминг
    if gr.d_old != 'тв':
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    s_new = s_old

    if s_new == 'NONE':
        return ('', 'NONE'), ''

    # Удаление словоизменительных суффиксов
    suff = re.search('Е?Н?Н$|Т$', s_new)
    if suff:
        s_new = s_new[:-len(suff.group())]

    # Основы-исключения
    for regex in lib.part_spec:
        mo = re.match(regex, s_new)
        if mo:
            s_modif = re.sub(regex, mo.group(1) + lib.part_spec[regex][0], s_new)
            if s_new != s_modif:
                return (s_old, s_modif), lib.part_spec[regex][1]

    # Проблемные классы
    s_modif, infl = verb.cls_cons_modif(tools.de_palat(s_new, gr.pos))
    if infl:
        return (s_old, s_modif), infl

    jot = bool(s_new.endswith(tuple('ЛНРЖЧШЩ')) or s_new.endswith(('ЖД', 'ШТ')))

    # Сочетания с йотом
    if jot:
        s_new = tools.de_jot(s_new) + 'И'
    # TODO -ЪВ- (-ОВ-) // -Ы-
    elif suff and suff.group().startswith('ЕН'):
        s_new += 'И'
    # 3*-й класс
    elif s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def main(token):
    gr = Part(token)

    if gr.tense == 'прош':
        # Страдательные
        if gr.d_old in ('a', 'o', 'тв'):
            stem, fl = pas_past(gr)
        # Действительные
        else:
            stem, fl = act_past(gr)

    else:
        return ('', ''), ''

    if stem[1] != 'NONE' and gr.refl:
        fl += 'СЯ'

    return stem, fl
