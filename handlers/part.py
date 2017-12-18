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

    if s_new != 'NONE':
        # Удаление словоизменительных суффиксов
        if s_new.endswith('В'):
            s_new = s_new[:-1]
        elif re.search('В?[ЪЬ]?Ш$', s_new):
            s_new = s_new[:-len(re.search('В?[ЪЬ]?Ш?$', s_new).group())]

        ok = False

        # Основы-исключения
        for regex in lib.part_spec:
            mo = re.match('(.*)%s$' % regex, s_new)
            if mo:
                s_new = re.sub('(.*)%s$' % regex, mo.group(1) + lib.part_spec[regex], s_new)
                ok = True
                break

        # Проблемные классы
        s_modif = verb.cls_cons_modif(s_new)
        if s_new != s_modif:
            s_new = s_modif
            ok = True

        if not ok:
            s_modif = tools.de_palat(s_new, gr.pos)

            # Вторая палатализация
            if s_new != s_modif:
                s_new = s_modif + 'И'
            # 3*-й класс (4-й по АГ)
            elif s_new[-1] in 'БГЗКПСХ' or s_new in ('ВЯ', 'СТЫ'):
                s_new += 'НУ'
            # Не пойми что
            elif s_new[-1] in lib.cons:
                s_new += 'И'

            s_new += 'ТИ'

        if gr.refl:
            s_new += 'СЯ'

    return (s_old, s_new), ''


def main(token):
    gr = Part(token)

    if gr.tense == 'прош':
        # Страдательные
        if gr.d_old in ('a', 'o', 'тв'):
            pass
        # Действительные
        else:
            return act_past(gr)

    return ('', ''), ''
