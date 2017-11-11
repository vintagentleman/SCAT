import lib


def get_params(t):

    form = t.reg.replace('(', '').replace(')', '')

    # Минус маркер 'собственности'
    prop = bool('*' in form)
    if prop:
        form = form.replace('*', '')

    # Конечные согласные - благо
    if form[-1] not in lib.vows:
        form += '`'

    pos = t.ana[0]

    # Учёт смешения типов склонения: новый тип - для флексии, старый - для основы
    if '/' in t.ana[1]:
        decl = t.ana[1][:t.ana[1].index('/')]
        new_decl = t.ana[1][t.ana[1].index('/') + 1:]
    else:
        decl = new_decl = t.ana[1]

    # Одушевлённость, 'зв/им' и прочий синтаксис в расчёт не берём
    case = t.ana[2][t.ana[2].find('/') + 1:]

    # Вообще всегда отдаём предпочтение трактовке 'за чертой'
    pt = bool(t.ana[3] == 'pt')
    if pt:
        num = 'мн'
    else:
        num = t.ana[3][t.ana[3].find('/') + 1:]

    # Тут, помимо всего, учёт особого смешения (преим. en/i)
    if t.ana[4] == '0':
        gen = 'м'
    else:
        gen = t.ana[4][t.ana[4].find('/') + 1:]

    nb = t.ana[5]

    return form, prop, pos, decl, new_decl, case, num, pt, gen, nb


def reduction_on(pos, new_decl, case, num, gen):

    if pos == 'сущ':
        if (new_decl in ('a', 'ja') and (case, num) == ('род', 'мн')
                or new_decl in ('o', 'jo') and gen == 'м' and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
                or new_decl in ('o', 'jo') and gen == 'ср' and (case, num) == ('род', 'мн')
                or new_decl in ('i', 'u') and (case, num) not in (('им', 'ед'), ('вин', 'ед'))
                or new_decl.startswith('e') and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
                or new_decl == 'uu' and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))):
            return True

    elif pos.startswith('прил'):
        if (new_decl in ('a', 'ja') and (case, num) != ('род', 'мн')
                or new_decl in ('o', 'jo') and gen == 'м' and (case, num) not in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
                or new_decl in ('o', 'jo') and gen == 'ср' and (case, num) != ('род', 'мн')):
            return True

    return False


def de_reduce(s, pos, decl, nb):

    if pos == 'сущ':

        if decl in ('a', 'ja'):
            # 'ОВЕЦЬ' --> 'ОВЦА', 'СУДЕБЪ' --> 'СУДБА'
            if any(tag in nb for tag in ('-о', '-е')) or s[-1] == 'Ц' and s[-2] == 'Е':
                s = s[:-2] + s[-1]

        else:
            # 'ПРИБЫТКОМЪ' --> 'ПРИБЫТОКЪ', 'ЗОЛЪ' --> 'ЗЛО'
            if any(tag in nb for tag in ('+о', '+е', '-о', '-е')):

                if '+о' in nb:
                    s = s[:-1] + 'О' + s[-1]
                elif '+е' in nb:
                    s = s[:-1] + 'Е' + s[-1]
                else:
                    s = s[:-2] + s[-1]

            # 'САМОДЕРЖЦА' --> 'САМОДЕРЖЕЦЪ'
            elif s[-1] == 'Ц' and s[-2] in lib.cons:
                s = s[:-1] + 'Е' + s[-1]

    else:
        # ТЯЖКИ --> ТЯЖЕКЪ
        if any(tag in nb for tag in ('+о', '+е')):

            if '+о' in nb:
                s = s[:-1] + 'О' + s[-1]
            else:
                s = s[:-1] + 'Е' + s[-1]

        # БЕЗОТВ+ТНО --> БЕЗОТВ+ТЕНЪ
        elif s[-1] == 'Н' and s[-2] in lib.cons:
            s = s[:-1] + 'Е' + s[-1]

    return s
