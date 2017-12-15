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

        # 7-й класс (ГСРЯ)

        # Основы, совпадающие с инфинитивными (группа а) 2-го подкласса 6-го класса по АГ)
        for regex in lib.cls_7_cons:
            if re.match('(.*)%s$' % regex, s_new):
                s_new += 'ТИ'
                ok = True

        # Исключения (с чередованием в основе)
        for regex in lib.cls_7_cons_exc:
            if re.match('(.*)%s$' % regex, s_new):
                s_new = re.sub('(.*)%s$' % regex, lib.cls_7_cons_exc[regex], s_new) + 'ТИ'
                ok = True

        # Не совпадающие (7-й подкласс 7-го класса по АГ)
        for regex in lib.cls_7_vow:
            if re.match('(.*)%s$' % regex, s_new):
                s_new += 'СТИ'
                ok = True

        # 8-й класс (ГСРЯ)
        for regex in lib.cls_8:
            if re.match('(.*)%s$' % regex, s_new):
                s_new = s_new[:-1]

                # Чередование с нулём
                if s_new in lib.cls_8_exc:
                    s_new += lib.cls_8_exc[s_new]

                s_new += 'ЧИ'
                ok = True

        # 9-й класс (ГСРЯ)
        for regex in lib.cls_9:
            if re.match('(.*)%s$' % regex, s_new):
                s_new += 'ЕТИ'
                ok = True

        if not ok:
            if s_new[-1] in lib.cons:
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
