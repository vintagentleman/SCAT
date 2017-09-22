import lib
import modif_lib


# Проверка наличия титла в слове
def tit_check(wort):

    tit = 0
    if wort.find('#') != -1:
        tit = 1

    return tit


# Подсчёт длины слова без титла
def real_length(wort):

    l = len(wort)
    if tit_check(wort) == 1:
        l = len(wort) - 1

    return l


# Замена буквосочетания
def repl(wort, d):

    for coll in d.keys():
        if wort.find(coll) != -1:
            wort = wort.replace(coll, d[coll])

    return wort


def modif(wort, pos):
    # Начало программы
    wort_init = wort

    if tit_check(wort) == 1:
        for coll in modif_lib.titlo_on_st.keys():
            if wort.find(coll) == 0:
                # Замена буквосочетаний под титлом (только в начале слов)
                wort = wort.replace(coll, modif_lib.titlo_on_st[coll], 1)

        # Cлучаи с двойственной трактовкой
        for coll in modif_lib.titlo_on_st_ambig.keys():
            if wort.find(coll[0]) == 0 and coll[1] == pos:
                wort = wort.replace(coll[0], modif_lib.titlo_on_st_ambig[coll])

        # Замена буквосочетаний под титлом (везде)
        wort = repl(wort, modif_lib.titlo)

    # Если была замена, отрезаем титло
    if wort_init != wort:
        wort = wort[:-1]

    # Замена буквосочетаний в сокращённых корнях без титла
    if tit_check(wort) == 0:
        # Cлучаи с двойственной трактовкой (надстроки случаев с однозначной)
        for coll in modif_lib.abbr_ambig_long.keys():
            if wort.find(coll[0]) != -1 and coll[1] == pos:
                wort = wort.replace(coll[0], modif_lib.abbr_ambig_long[coll])

        # Случаи с однозначной трактовкой
        wort = repl(wort, modif_lib.abbr)

        # Cлучаи с двойственной трактовкой (подстроки случаев с однозначной)
        for coll in modif_lib.abbr_ambig_short.keys():
            if wort.find(coll[0]) != -1 and coll[1] == pos:
                wort = wort.replace(coll[0], modif_lib.abbr_ambig_short[coll])

    # Замены только *не* на конце слов
    for coll in modif_lib.not_on_end:
        if wort.find(coll) != -1 and wort.find(coll) != real_length(wort) - len(coll):
            wort = wort.replace(coll, modif_lib.not_on_end[coll], 1)

    # Замена разных буквосочетаний вне зависимости от положения в слове
    wort = repl(wort, modif_lib.ad_post)

    # Замена -ств- и -ск-
    if wort.find('ЖСК') == -1 and wort.find('ЖЕСК') == -1 and wort.find('ЖЬСК') == -1:
        for coll in modif_lib.stv:
            if wort.find(coll) > 2:
                wort = wort.replace(coll, modif_lib.stv[coll])

        for coll in modif_lib.stv_new:
            if wort.find(coll) > 2:
                if wort[wort.find(coll) - 1] in set(lib.cons_hush) - {'Ц'}:  # 'ШТ'?
                    wort = wort[:wort.find(coll)] + 'Е' + wort[wort.find(coll):]
                elif wort[wort.find(coll) - 1] == 'Л':
                    wort = wort[:wort.find(coll)] + 'Ь' + wort[wort.find(coll):]

    # Замена -мь- и -вь- только внутри слов
    for coll in modif_lib.mv:
        if wort.find(coll) != -1 and wort.find(coll) != real_length(wort) - len(coll):
            if wort.find(coll) + len(coll) < len(wort):
                if wort[wort.find(coll) + len(coll)] not in set(lib.vows) - {'Ъ', 'Ь'}:
                    wort = wort.replace(coll, modif_lib.mv[coll])

    # Замена буквосочетаний на конце слов
    for coll in modif_lib.on_end:
        if wort.rfind(coll) != -1 and wort.rfind(coll) == real_length(wort) - len(coll):
            # Тут в слайсах раньше из rfind() вычиталась 1, я убрал
            wort = wort[:wort.rfind(coll)] + wort[wort.rfind(coll):].replace(coll, modif_lib.on_end[coll])

    # Исправление ошибок
    wort = repl(wort, modif_lib.errors)

    for coll in modif_lib.errors_on_st:
        if wort.find(coll) == 0:
            wort = wort.replace(coll, modif_lib.errors_on_st[coll])

    return wort
