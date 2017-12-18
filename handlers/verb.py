import re
import lib
import tools
from handlers import Verb


def cls_cons_modif(s):
    # 7-й класс (основы на гласный)
    for regex in lib.cls_7_vow:
        if re.match('(.*)%s$' % regex, s):
            return s + 'СТИ'

    # 7-й класс (основы на согласный)
    for regex in lib.cls_7_cons:
        mo = re.match('(.*)%s$' % regex, s)
        if mo:
            return re.sub('(.*)%s$' % regex, mo.group(1) + lib.cls_7_cons[regex], s) + 'ТИ'

    # 8-й класс (ГСРЯ)
    for regex in lib.cls_8:
        if re.match('(.*)%s$' % regex, s):
            s = s[:-1]

            # Чередование с нулём
            if s == 'ТОЛ':
                s += 'О'
            elif s == 'Ж':
                s += 'Е'

            return s + 'ЧИ'

    # 9-й класс (ГСРЯ)
    if re.match('(.*)[МПТ][+Е]Р$', s):
        return s + 'ЕТИ'

    return s


def part_el(gr):
    # Стемминг
    s_old = tools.find_stem(gr.form, (gr.gen, gr.num), lib.part_el_infl)
    s_new = s_old

    if s_new != 'NONE':
        if s_new.endswith('Л'):
            s_new = s_new[:-1]

        ok = False

        # Исключение
        if re.match('(.*)Ш[+Е]$', s_new):
            s_new = re.sub('(.*)Ш[+Е]$', '\\1ИТИ', s_new)
            ok = True
        else:
            # Проблемные классы
            s_modif = cls_cons_modif(s_new)
            if s_new != s_modif:
                s_new = s_modif
                ok = True

        if not ok:
            # 3*-й класс (4-й по АГ)
            if s_new[-1] in 'БГЗКПСХ' or s_new in ('ВЯ', 'СТЫ'):
                s_new += 'НУ'

            s_new += 'ТИ'

        if gr.refl:
            s_new += 'СЯ'

    return (s_old, s_new), ''


def main(token):
    gr = Verb(token)

    if gr.mood == 'изъяв':
        # Простые времена
        if gr.tense == 'прош':
            return part_el(gr)

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
                return part_el(gr)

    elif gr.mood == 'сосл':
        if gr.role == 'св':
            return ('', 'AUX-SBJ'), ''
        elif gr.role.startswith('пр'):
            return part_el(gr)

    return ('', ''), ''
