import re
import lib
import modif


def lat_light(s):
    s = s.replace('а', 'a')
    s = s.replace('е', 'e')
    s = s.replace('о', 'o')

    return s


def rus_light(s):
    s = s.replace('a', 'а')
    s = s.replace('e', 'е')
    s = s.replace('o', 'о')

    return s


def rus_full(s):
    s = s.replace('A', 'А')
    s = s.replace('a', 'а')
    s = s.replace('B', 'В')
    s = s.replace('E', 'Е')
    s = s.replace('e', 'е')
    s = s.replace('K', 'К')
    s = s.replace('M', 'М')
    s = s.replace('H', 'Н')
    s = s.replace('O', 'О')
    s = s.replace('o', 'о')
    s = s.replace('P', 'Р')
    s = s.replace('C', 'С')
    s = s.replace('c', 'с')
    s = s.replace('T', 'Т')
    s = s.replace('X', 'Х')
    s = s.replace('x', 'х')

    return s


def remove_punctuation(s, nb):
    # Учёт исправлений (обработка производится над исправленным вариантом)
    if '<' in s:
        s = s[s.index('<') + 1:s.index('>')]

    # 'Безумные' (неэтимологические) еры и ери на концах строки, можем удалять их без разметки
    # Не трогаем, если 1) они оканчивают словоформу либо 2) входят в состав префиков типа ВЪ- и СЪ-
    if not ('+ъ' in nb or '+ь' in nb):
        for yer in ('Ъ&', 'ЪZ', 'Ь&', 'ЬZ'):
            if yer in s and not (s.endswith(yer) or s[1:].startswith(yer)):
                    s = s.replace(yer, '')

    # Знаки препинания
    for sign in '&Z.,:;[]- ':
        s = s.replace(sign, '')

    # Номера страниц
    for i in range(10):
        s = s.replace(str(i), '')

    return s


def normalise(s, pos):

    def simplify_graphics(s):
        # Однозначные графические дублеты
        s = s.replace('S', 'З')
        s = s.replace('I', 'И')
        s = s.replace('W', 'О')
        s = s.replace('D', 'У')
        s = s.replace('G', 'У')
        s = s.replace('U', 'У')
        s = s.replace('F', 'Ф')
        s = s.replace('R', 'Я')
        s = s.replace('L', 'КС')
        s = s.replace('Q', 'ПС')

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

    prop = bool('*' in s)
    if prop:
        s = s.replace('*', '')

    s = s.upper()
    s = simplify_graphics(s)
    s = modif.modif(s, pos)
    s = s.replace('(', '').replace(')', '')

    if prop:
        s = '*' + s

    # Если в итоге есть титло - плохо, но что поделать
    if '#' in s:
        s = s.replace('#', '')

    return s


def find_stem(form, gram_comb, fl_dict):
    stem = 'NONE'

    # Проверка на корректность сочетания граммем
    if gram_comb in fl_dict.keys():

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
