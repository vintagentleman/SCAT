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

    if s_old == 'NONE':
        return ('', 'NONE'), ''
    else:
        s_new = s_old

    # Удаление словоизменительных суффиксов
    suff = re.search('В$|В?[ЪЬ]?Ш$', s_new)
    if suff:
        s_new = s_new[:-len(suff.group())]

    # Основы-исключения
    for regex in lib.part_spec:
        mo = re.match(regex, s_new)
        if mo:
            s_modif = re.sub(regex, mo.group(1) + lib.part_spec[regex], s_new)
            if s_new != s_modif:
                return (s_old, s_modif), 'ТИ'

    # Проблемные классы
    s_modif, infl = verb.cls_cons_modif(s_new)
    if infl:
        return (s_old, s_modif), infl

    # Сочетания с йотом
    if s_new.endswith(('Л', 'Н', 'Р', 'Ж', 'ЖД', 'Ч', 'Ш', 'ШТ', 'Щ')):
        s_new = tools.de_jot(s_new) + 'И'
    # 4 класс
    elif s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def pas_past(gr):
    # Стемминг
    if gr.d_old != 'тв':
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    if s_old == 'NONE':
        return ('', 'NONE'), ''
    else:
        s_new = s_old

    # Удаление словоизменительных суффиксов
    suff = re.search('Е?Н?Н$|Т$', s_new)
    if suff:
        s_new = s_new[:-len(suff.group())]

    # Проблемные классы
    s_modif, infl = verb.cls_cons_modif(s_new[:-1] + lib.palat_1.get(s_new[-1], s_new[-1]))
    if infl:
        return (s_old, s_modif), infl

    # Сочетания с йотом
    if s_new.endswith(('Л', 'Н', 'Р', 'Ж', 'ЖД', 'Ч', 'Ш', 'ШТ', 'Щ')):
        s_new = tools.de_jot(s_new) + 'И'

    # Чередование /u:/: 'вдохновенный', 'проникновенный'; 'омовенный', 'незабвенный'. Но - 'благословенный'
    elif suff and suff.group().startswith('ЕН'):
        mo = re.search('[ОЪ]?В$', s_new)

        if not s_new.endswith('СЛОВ') and mo:
            s_new = s_new[:-len(mo.group())]

            if s_new[-1] == 'Н':
                s_new += 'У'
            else:
                s_new += 'Ы'
        else:
            s_new += 'И'

    # 4 класс
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
