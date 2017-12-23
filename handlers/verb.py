import re
import lib
import tools
from handlers import Verb


def cls_cons_modif(s):
    # 7-й класс (основы на гласный)
    for regex in lib.cls_7_vow:
        if re.match('(.*)%s$' % regex, s):
            return s, 'СТИ'

    # 7-й класс (основы на согласный)
    for regex in lib.cls_7_cons:
        mo = re.match('(.*)%s$' % regex, s)
        if mo:
            return re.sub('(.*)%s$' % regex, mo.group(1) + lib.cls_7_cons[regex], s), 'ТИ'

    # 8-й класс
    for regex in lib.cls_8:
        if re.match('(.*)%s$' % regex, s):
            s = s[:-1]

            # Чередование с нулём
            if s == 'ТОЛ':
                s += 'О'
            elif s == 'Ж':
                s += 'Е'

            return s, 'ЩИ'

    # 9-й класс
    if re.match('(.*)[МПТ][+Е]Р$', s):
        return s, 'ЕТИ'

    return s, ''


def part_el(gr):
    # Стемминг
    s_old = tools.find_stem(gr.form, (gr.gen, gr.num), lib.part_el_infl)
    s_new = s_old

    if s_new == 'NONE':
        return ('', 'NONE'), ''

    if s_new.endswith('Л'):
        s_new = s_new[:-1]

    # Основы-исключения
    for regex in lib.part_el_spec:
        mo = re.match(regex, s_new)
        if mo:
            s_modif = re.sub(regex, mo.group(1) + lib.part_el_spec[regex][0], s_new)
            if s_new != s_modif:
                return (s_old, s_modif), lib.part_el_spec[regex][1]

    # Проблемные классы
    s_modif, infl = cls_cons_modif(s_new)
    if infl:
        return (s_old, s_modif), infl

    # 3*-й класс
    if s_new[-1] in lib.cons or s_new in ('ВЯ', 'СТЫ'):
        s_new += 'НУ'

    return (s_old, s_new), 'ТИ'


def main(token):
    gr = Verb(token)
    stem, fl = ('', ''), ''

    if gr.mood == 'изъяв':
        # Простые времена
        if gr.tense == 'прош':
            stem, fl = part_el(gr)

        # Сложные времена
        if re.match('перф|плюскв|буд ?[12]', gr.tense):
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

    # Убрать, когда закончим со всеми временами
    if stem[1] not in ('', 'NONE') and gr.refl:
        fl += 'СЯ'

    return stem, fl
