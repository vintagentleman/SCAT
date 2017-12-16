import re
import lib
import tools
from handlers import Part, verb


exc = {
    '[ЕИ]М': 'ЯТИ',
    'В[ОЪ]?Ш[+Е]Д': 'ВОИТИ',
    '(?<=[%s])Ш[+Е]Д' % ''.join(lib.cons): 'ЫТИ',
    'Ш[+Е]Д': 'ИТИ',
}


def act_past(gr):
    # Стемминг
    if gr.d_old != 'м':
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.nom_infl)
    else:
        s_old = tools.find_stem(gr.form, (gr.d_new, gr.case, gr.num, gr.gen), lib.pron_infl)

    s_new = s_old

    if s_new != 'NONE':
        # Удаление словоизменительных суффиксов
        if gr.d_old != 'м' and gr.case == 'им' and gr.num == 'ед' and gr.gen in ('м', 'ср'):
            if s_new.endswith('В'):
                s_new = s_new[:-1]
        else:
            mo = re.search('В?[ЪЬ]?Ш$', s_new)
            if mo:
                s_new = s_new[:-len(mo.group())]

        ok = False

        # Основы-исключения
        for stem in exc:
            po = re.compile('(.*)%s$' % stem)
            mo = po.match(s_new)
            if mo:
                s_new = re.sub(po.pattern, mo.group(1) + exc[stem], s_new)
                ok = True

        # Проблемные классы
        s_modif = verb.past_stem_modif(s_new, trim=True)
        if s_new != s_modif:
            s_new = s_modif
            ok = True

        if not ok:
            # Палатализация
            s_modif = tools.de_palat(s_modif, gr.pos)
            if s_new != s_modif:
                s_new = s_modif + 'И'
            elif s_new[-1] in lib.cons_sonor:
                s_new += 'И'
            elif s_new[-1] in lib.cons:
                s_new += 'НУ'

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
