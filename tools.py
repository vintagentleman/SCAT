import re
import lib
import modif
import txt_to_xml


def normalise(string, pos):

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
    if prop:
        string = string[1:]
    sic = bool(string.startswith('*'))
    if sic:
        string = string[1:]

    string = string.upper()
    string = simplify_graphics(string)
    string = modif.modif(string, pos)
    string = string.replace('(', '').replace(')', '')

    if prop:
        string = '*' + string
    if sic:
        string = '~' + string

    return string


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
