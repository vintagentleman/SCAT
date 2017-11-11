import re
import lib
import modif_lib


# Подсчёт длины слова без титла
def real_len(w):

    if '#' in w:
        return len(w) - 1

    return len(w)


# Замена буквосочетания
def repl(w, d, mode='search'):
    for coll in d:

        if mode == 'match':
            if re.match(coll, w):
                w = re.sub(coll, d[coll], w, 1)

        else:
            if re.search(coll, w):
                w = re.sub(coll, d[coll], w)

    return w


# Замена неоднозначного буквосочетания
def repl_var(w, p, d, mode='search'):
    for coll in d:

        if mode == 'match':
            if re.match(coll, w):
                if p in d[coll]:
                    w = re.sub(coll, d[coll][p], w, 1)
                else:
                    w = re.sub(coll, d[coll][''], w, 1)

        else:
            if re.search(coll, w):
                if p in d[coll]:
                    w = re.sub(coll, d[coll][p], w)
                else:
                    w = re.sub(coll, d[coll][''], w)

    return w


# Замена буквосочетаний под титлом (только в начале слов)
def modif_titlo_on_start(w, p):
    w = repl(w, modif_lib.titlo_on_start, 'match')

    # Случаи с неоднозначным раскрытием
    w = repl_var(w, p, modif_lib.titlo_on_start_var, 'match')

    return w


# Замена буквосочетаний под титлом (везде)
def modif_titlo(w):
    return repl(w, modif_lib.titlo)


# Замена буквосочетаний в сокращённых корнях без титла
def modif_abbr(w, p):
    # # Случаи с неоднозначным раскрытием (надстроки случаев с однозначным)
    w = repl_var(w, p, modif_lib.abbr_var_before)

    w = repl(w, modif_lib.abbr)

    # # Случаи с неоднозначным раскрытием (подстроки случаев с однозначным)
    w = repl_var(w, p, modif_lib.abbr_var_after)

    return w


# Замены *не* на конце слов
def modif_not_on_end(w):
    for coll in modif_lib.not_on_end:
        mo = re.search(coll, w)

        if mo and mo.end() != real_len(w):
            w = re.sub(coll, modif_lib.not_on_end[coll], w, 1)

    return w


# Замена разных буквосочетаний вне зависимости от положения в слове
def modif_varia(w):
    return repl(w, modif_lib.varia)


# Замена -ств- и -ск-
def modif_stv(w):
    mo = re.search('[ЕЬ]С(ТВ|К)', w)

    if mo and mo.start() > 2:
        w = re.sub('[ЕЬ]С(ТВ|К)', 'С\\1', w)

    mo = re.search('С(ТВ|К)', w)

    if mo and mo.start() > 2:
        if w[mo.start() - 1] in set(lib.cons_hush) - {'Ц'}:
            w = w[:mo.start()] + 'Е' + w[mo.start():]
        elif w[mo.start() - 1] == 'Л':
            w = w[:mo.start()] + 'Ь' + w[mo.start():]

    return w


# Замена -мь- и -вь- только внутри слов
def modif_mv(w):
    mo = re.search('([МВ])Ь', w)

    if mo and mo.end() < real_len(w):
        if w[mo.end() + 1] not in set(lib.vows) - {'Ъ', 'Ь'}:
            w = re.sub('([МВ])Ь', '\\1', w)

    return w


# Замена буквосочетаний на конце слов
def modif_on_end(w, p):
    for coll in modif_lib.on_end:
        mo = re.search(coll + '$', w)

        if mo and mo.end() == real_len(w):
            w = w[:mo.start()] + re.sub(coll, modif_lib.on_end[coll], w[mo.start():])

    for coll in modif_lib.on_end_var:
        mo = re.search(coll + '$', w)

        if mo and mo.end() == real_len(w):
            if p in modif_lib.on_end_var[coll]:
                w = w[:mo.start()] + re.sub(coll, modif_lib.on_end_var[coll][p], w[mo.start():])
            else:
                w = w[:mo.start()] + re.sub(coll, modif_lib.on_end_var[coll][''], w[mo.start():])

    return w


# Исправление ошибок
def modif_errors(w):
    w = repl(w, modif_lib.errors)
    w = repl(w, modif_lib.errors_on_start, 'match')
    
    return w


def modif(wort, pos):
    wort_init = wort

    if '#' in wort:
        wort = modif_titlo_on_start(wort, pos)
        wort = modif_titlo(wort)

    if wort_init != wort:
        wort = wort[:-1]

    if '#' not in wort:
        wort = modif_abbr(wort, pos)

    wort = modif_not_on_end(wort)
    wort = modif_varia(wort)

    if not re.search('Ж[ЕЬ]?СК', wort):
        wort = modif_stv(wort)

    wort = modif_mv(wort)
    wort = modif_on_end(wort, pos)

    return modif_errors(wort)
