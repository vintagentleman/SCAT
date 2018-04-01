import re
import lib
import modif


def count_chars(string, num=-1):

    def skip_chars(s, start):

        if s[start] == '<':
            start += len(re.search(r'(<.+?>)', s[start:]).group(1))
        elif s[start] == '&':
            start += len(re.search(r'(&.+?;)', s[start:]).group(1)) - 1

        if s[start] in '<&':
            start = skip_chars(s, start)

        return start

    if num > -1:
        result = 0
        result = skip_chars(string, result)

        for i in range(num):
            result += 1
            result = skip_chars(string, result)

        return result

    string = re.sub(r'<.+?>', '', string)
    string = re.sub(r'&.+?;', 'S', string)

    return len(string)


def replace_chars(string, fr, to):

    if len(fr) != len(to):
        raise RuntimeError

    result = list(string)

    for i in range(len(result)):
        if result[i] in fr:
            result[i] = to[fr.index(result[i])]

    return ''.join(result)


def normalise(string, pos, nb):

    def simplify_graphics(s):
        # Однозначные графические дублеты
        s = replace_chars(s, 'SIWDGUFRLQ', ('З', 'И', 'О', 'У', 'У', 'У', 'Ф', 'Я', 'КС', 'ПС'))

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


def de_palat(s, pos, pair=None):
    # Для имён номер палатализации не имеет значения
    if pos not in ('гл', 'прич'):

        if pair == ('jo', 'o'):
            if s[-1] == 'Ч':
                return s[:-1] + 'Ц'
            elif s[-1] == 'Ж':
                return s[:-1] + 'З'
            elif s[-1] == 'Ш':
                return s[:-1] + 'С'

        else:
            if s[-1] in 'ЧЦ' or s[-2:] == 'СТ':
                return s[:-1] + 'К'
            elif s[-1] in 'ЖЗ':
                return s[:-1] + 'Г'
            elif s[-1] in 'ШС':
                return s[:-1] + 'Х'

    # Для глаголов актуальна только вторая
    else:
        if s[-1] == 'Ч':
            return s[:-1] + 'К'
        elif s[-1] == 'Ж':
            return s[:-1] + 'Г'
        elif s[-1] == 'Ш':
            return s[:-1] + 'Х'

    return s


def de_jot(s):

    if s.endswith(('БЛ', 'ВЛ', 'МЛ', 'ПЛ', 'ФЛ')):
        return s[:-1]

    elif s.endswith(('Ж', 'ЖД')):
        debut = s[:-len(re.search('ЖД?$', s).group())]

        for fin in ('Д', 'З', 'ЗД'):
            for regex in lib.cnj_2_zh:
                if re.search(regex + '$', debut + fin):
                    return debut + fin

    elif s.endswith(('Ч', 'Щ', 'ШТ')):
        debut = s[:-len(re.search('(Ч|Щ|ШТ)$', s).group())]

        for fin in ('Т', 'СТ'):
            for regex in lib.cnj_2_tsch:
                if re.search(regex + '$', debut + fin):
                    return debut + fin

    elif s.endswith('Ш'):
        for regex in lib.cnj_2_sch:
            if re.search(regex + '$', s[:-1] + 'С'):
                return s[:-1] + 'С'

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
        if (new_decl in ('a', 'ja') and (case, num) == ('род', 'мн')
                or new_decl in ('o', 'jo') and gen == 'м' and (case, num) in (('им', 'ед'), ('вин', 'ед'), ('род', 'мн'))
                or new_decl in ('o', 'jo') and gen == 'ср' and (case, num) == ('род', 'мн')):
            return True

    return False


def de_reduce(s, decl, nb):

    if decl in ('a', 'ja'):
        # 'ОВЕЦЬ' --> 'ОВЦА', 'СУДЕБЪ' --> 'СУДБА'
        if any(tag in nb for tag in ('-о', '-е')) or s.endswith('ЕЦ'):
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

    return s
