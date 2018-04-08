import re
import lib
import tools
from handlers import Verb


def cls_cons_modif(s):
    # VI.2.а и VII.1 классы: основы на гласный
    if re.search('(БЛЮ|БРЕ|ВЕ|КЛА|КЛЯ|КРА|МЕ|ПА|ПЛЕ|СЕ|ЧЕ)$', s):
        return s, 'СТИ'

    # VI.2.а и VII.1 классы: основы на согласный
    for regex in lib.cnj_1_sti:
        mo = re.match('(.*)%s$' % regex, s)
        if mo:
            return re.sub('(.*)%s$' % regex, mo.group(1) + lib.cnj_1_sti[regex], s), 'ТИ'

    # VI.1 класс
    for regex in lib.cnj_1_tschi:
        if re.search('%s$' % regex, s):
            s = s[:-1]

            # Чередование с нулём
            if s == 'ТОЛ':
                s += 'О'
            elif s == 'Ж':
                s += 'Е'

            return s, 'ЩИ'

    # VI.2.б и VI.2.в классы
    if re.search('[МПТ][+Е]Р$', s):
        return s + 'Е', 'ТИ'
    elif re.search('ШИБ$', s):
        return s + 'И', 'ТИ'

    return s, ''


def part_el(gr):
    # Стемминг
    s_old = tools.find_stem(gr.form, (gr.gen, gr.num), lib.part_el_infl)

    if s_old == 'NONE':
        return ('', 'NONE'), ''
    else:
        s_new = s_old

    # Основы-исключения
    for regex in lib.part_el_spec:
        mo = re.match(regex, s_new)
        if mo:
            s_modif = re.sub(regex, mo.group(1) + lib.part_el_spec[regex], s_new)
            if s_new != s_modif:
                return (s_old, s_modif), 'ТИ'

    # Проблемные классы
    s_modif, infl = cls_cons_modif(s_new)
    if infl:
        return (s_old, s_modif), infl

    # 4 класс
    if s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def aor_simp(gr):
    # Стемминг
    s_old = tools.find_stem(gr.form, (gr.pers, gr.num), lib.aor_simp_infl)

    if s_old == 'NONE':
        return ('', 'NONE'), ''
    else:
        s_new = s_old

    # Основы-исключения (настоящего времени)
    if s_new.endswith(('ДАД', 'ЖИВ', 'ИД', 'ЫД')):
        s_new = s_new[:-1]

    # Первая палатализация
    if s_new[-1] in 'ЧЖШ':
        s_new = s_new[:-1] + lib.palat_1[s_new[-1]]

    # Проблемные классы
    s_modif, infl = cls_cons_modif(s_new)
    if infl:
        return (s_old, s_modif), infl

    # 4 класс
    if s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def aor_sigm(gr):
    # Простейший случай
    if gr.tense == 'аор гл' and gr.pers in ('2', '3') and gr.num == 'ед':
        mo = re.search('С?Т[ЪЬ`]$', gr.form)
        if mo:
            return (gr.form, gr.form[:-len(mo.group())]), 'ТИ'
        else:
            return (gr.form, gr.form), 'ТИ'

    # Стемминг
    s_old = tools.find_stem(gr.form, (gr.pers, gr.num), lib.aor_sigm_infl)
    # Осложнение тематического суффикса
    if gr.tense == 'аор нов' and s_old.endswith('О'):
        s_old = s_old[:-1]

    if s_old == 'NONE':
        return ('', 'NONE'), ''
    elif gr.tense == 'аор гл':
        return (s_old, s_old), 'ТИ'
    else:
        s_new = s_old

    # Основы-исключения (настоящего времени)
    if s_new.endswith(('ДАД', 'ЖИВ', 'ИД', 'ЫД')):
        s_new = s_new[:-1]

    # Удлинение корневого гласного
    if gr.tense == 'аор сигм' and s_new == 'Р+':
        return (s_old, 'РЕ'), 'ЩИ'

    # Проблемные классы
    s_modif, infl = cls_cons_modif(s_new)
    if infl:
        return (s_old, s_modif), infl

    # 4 класс
    if s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def main(token):
    gr = Verb(token)
    stem, fl = ('', ''), ''

    if gr.mood == 'изъяв':
        # --- Простые времена --- #

        if gr.tense == 'прош':
            stem, fl = part_el(gr)
        elif gr.tense == 'аор пр':
            stem, fl = aor_simp(gr)
        elif gr.tense.startswith('аор'):
            stem, fl = aor_sigm(gr)

        elif gr.tense == 'а/имп':
            # Тут лексема одна-единственная
            if gr.pers in ('2', '3') and gr.num == 'ед':
                s_old = gr.form
            else:
                s_old = tools.find_stem(gr.form, (gr.pers, gr.num), lib.aor_sigm_infl)

            if s_old != 'NONE':
                stem, fl = (s_old, 'БЫ'), 'ТИ'

        # --- Сложные времена --- #

        elif re.match('перф|плюскв|буд ?[12]', gr.tense):

            if gr.role.endswith('св'):
                if gr.tense in lib.ana_tenses:
                    return ('', lib.ana_tenses[gr.tense]), ''
                else:
                    return ('', 'NONE'), ''

            elif gr.role == 'инф':
                return ('', gr.form), ''
            elif gr.role.startswith('пр'):
                stem, fl = part_el(gr)

    elif gr.mood == 'сосл':

        if gr.role == 'св':
            return ('', 'AUX-SBJ'), ''
        elif gr.role.startswith('пр'):
            stem, fl = part_el(gr)

    # В конце всей эпопеи убрать первое условие
    if stem[1] not in ('', 'NONE') and gr.refl:
        fl += 'СЯ'

    return stem, fl
