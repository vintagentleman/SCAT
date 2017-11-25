import re
import lib
import modif
import txt_to_xml


def normalise(string, pos, nb):

    def simplify_graphics(s):
        # Однозначные графические дублеты
        s = txt_to_xml.replace_chars(s, 'SIWDGUFRLQ', ('З', 'И', 'О', 'У', 'У', 'У', 'Ф', 'Я', 'КС', 'ПС'))

        # С ижицей не всё слава богу
        izh = (s.find(c) for c in s if c == 'V')

        if izh != (-1,):
            for i in izh:
                try:
                    # В окружении гласных или гласного с сонорным, а ещё после 'Е' - 'В'
                    if s[i - 1] == 'Е' or s[i - 1] in lib.vows and s[i + 1] in lib.vows + lib.cons_sonor:
                        s = s[:i] + 'В' + s[i + 1:]
                    # В остальных случаях - 'И'
                    else:
                        s = s[:i] + 'И' + s[i + 1:]
                # В абсолютном начале - тоже 'И'
                except IndexError:
                    s = s[:i] + 'И' + s[i + 1:]

        return s

    prop = bool(string.startswith('*'))
    sic = bool(string.startswith('~'))

    if prop or sic:
        string = string[1:]

    string = string.upper()
    string = simplify_graphics(string)

    # 'Безумные' (неэтимологические) еры и ери на концах строки, можем удалять их без разметки
    # Не трогаем, если 1) они оканчивают словоформу либо 2) входят в состав префиков типа ВЪ- и СЪ-
    if not ('+ъ' in nb or '+ь' in nb):
        for yer in ('Ъ&', 'ЪZ', 'Ь&', 'ЬZ'):
            if yer in string and not (string.endswith(yer) or string[1:].startswith(yer)):
                string = string.replace(yer, '')

    string = modif.modif(string, pos)

    if prop:
        string = '*' + string
    if sic:
        string = '~' + string

    # Если титло остаётся - плохо, но бывает
    if '#' in string:
        string = string.replace('#', '')

    return string


def find_stem(form, gram_comb, fl_dict):
    stem = 'NONE'

    # Проверка на корректность сочетания граммем
    if gram_comb in fl_dict:

        # Поиск флексии и стемминг
        infl = re.search('(%s|`)$' % fl_dict[gram_comb], form)
        if infl:
            stem = form[:-len(infl.group())]

    return stem


def de_palat(s, decl, new_decl):

    if (decl, new_decl) == ('jo', 'o'):
        if s.endswith('Ч'):
            s = s[:-1] + 'Ц'
        elif s.endswith('Ж'):
            s = s[:-1] + 'З'

    else:
        if s.endswith(('Ч', 'Ц')):
            s = s[:-1] + 'К'
        elif s.endswith(('Ж', 'З')):
            s = s[:-1] + 'Г'
        elif s.endswith(('Ш', 'С')):
            s = s[:-1] + 'Х'
        elif s.endswith('СТ'):
            s = s[:-1] + 'К'

    return s


def plus_minus(s, nb):

    nbl = nb
    for mark in ('+о', '+е', '-о', '-е', '+ъ', '+ь'):
        nbl = nbl.replace(mark, '')

    if '+' in nbl:
        s += nbl[nbl.index('+') + 1:].upper()
    elif '-' in nbl:
        s = s[:-len(nbl[nbl.index('-') + 1:])]

    return s


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
