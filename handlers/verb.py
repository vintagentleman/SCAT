import re
import lib
import tools
from handlers import Verb


def part_el(gr):
    # Стемминг
    s_old = tools.find_stem(gr.form, (gr.gen, gr.num), lib.part_el_infl)
    s_new = s_old

    if s_new != 'NONE':
        if s_new.endswith('Л'):
            s_new = s_new[:-1]

        ok = False

        # Исключение (-я?)
        if re.match('(.*)Ш[+Е]$', s_new):
            s_new = re.sub('(.*)Ш[+Е]$', '\\1ИТИ', s_new)
            ok = True

        # 1-й подкласс 6-го класса
        for regex in lib.cls_6_subcls_1:
            if re.match('(.*)%s$' % regex, s_new):
                # Чередование с нулём
                if '?' not in regex:
                    s_new = s_new[:-1]

                s_new += 'ЧИ'
                ok = True

        # TODO: 4-й класс (-ну-), 2-й подкласс 6-го класса и 7-й класс (-сти)

        if not ok:
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
