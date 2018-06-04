titlo_on_start = {
    'Б([АУЪЬ])#': 'БОГ\\1#',
    'БЕ#': 'БОЖЕ#',
    'БЪО(\(Т\))?Ц([ЪЬ])': 'БОГЪОТЕЦ\\2',
    'БГ?([ВМ])': 'БОГО\\1',
    'Б([ГЖЗ])': 'БО\\1',
    'БЕСТВ': 'БОЖЕСТВ',
    'БОМТР': 'БОГОМАТЕР',
    'БОМТ': 'БОГОМАТ',
    'БЦ': 'БОГОРОДИЦ',

    'Г([АЕ+ИУ])#': 'ГОСПОД\\1#',
    'ГВИ#': 'ГОСПОДЕВИ#',
    'ГМ([ЪЬ])': 'ГОСПОДОМ\\1',
    'Г([ЪЬ])': 'ГОСПОД\\1',

    'ДНЬ#': 'ДЕНЬ#',
    'ДВДВ': 'ДАВИДОВ',
    'ДВД': 'ДАВИД',
    'ДВ([ИОУЪЬЫ])': 'ДЕВ\\1',

    'И(И|\(С\))?С': 'ИИСУС',

    'МЛО': 'МИЛО',
    'МЛ([Е+ИЯ])': 'МОЛ\\1',
    'МЛТ': 'МОЛИТ',
    'МРИ': 'МАРИ',

    '(ДО|О\(Т\)|ПО)?НН([Е+])': '\\1НЫН\\2',
    'НЕ?БС': 'НЕБЕС',
    'НБ': 'НЕБ',
    'НШ([ГМ])': 'НАШЕ\\1',
    'НШ': 'НАШ',

    'ОЧ': 'ОТЧ',

    'ПР\(С\)НОДВ': 'ПРИСНОДЕВ',
    'ПРЧ': 'ПРЕЧ',

    'СЛВ': 'СЛАВ',
    'СНВ': 'СЫНОВ',
    'СН': 'СЫН',
    '(ПРЕ)?СТГ': '\\1СВЯТАГ',
    '(ПРЕ)?СТМ': '\\1СВЯТОМ',
    '(ВСЕ|О|ПРЕ)СТ': '\\1СВЯТ',
    'СТИЛЬ': 'СВЯТИТЕЛЬ',
    'СТЛ': 'СВЯТИТЕЛ',
    'СТ': 'СВЯТ',

    'Х([АЕ+ОУ])': 'ХРИСТ\\1',
    'ХВ': 'ХРИСТОВ',
    'Х([ЪЬ])': 'ХРИСТОС\\1',
    'ХС': 'ХРИСТОС',
    'Х\(С\)': 'ХРИСТ',
}

titlo_on_start_var = {
    'ГН': {
        'сущ': 'ГОСПОДИН',
        '': 'ГОСПОДН',
    },
}

titlo = {
    'АГГЕ?Л': 'АНГЕЛ',
    'АН[ЪЬ]ГЛ': 'АНГЕЛ',

    'БЛГОЧ\(С\)ТВ': 'БЛАГОЧЕСТИВ',
    'БЛГОЧ\(С\)Т': 'БЛАГОЧЕСТ',
    'БЛГОДН': 'БЛАГОДЕН',
    'БЛГ?ВЕ?Н': 'БЛАГОСЛОВЕН',
    'БЛГВ': 'БЛАГОСЛОВ',
    'БЛГО?\(Д\)Т': 'БЛАГОДАТ',
    'БЛЖН': 'БЛАЖЕН',
    'БЛ([ГЖ])': 'БЛА\\1',

    'ГЛ': 'ГЛАГОЛ',

    'ДВЦ': 'ДЕВИЦ',
    'ДР\(?В\)?Н': 'ДЕРЕВН',
    'ДХ([ВМ])': 'ДУХО\\1',
    'ДХ': 'ДУХ',
    'ДШВ': 'ДУШЕВ',
    'Д([СШ])': 'ДУ\\1',

    '([ЖМ])РТ': '\\1ЕРТ',

    'КНГН': 'КНЯГИН',
    'КН([ГЖЗ])': 'КНЯ\\1',
    'КРЩН': 'КРЕЩЕН',
    'КР([СШЩ])': 'КРЕ\\1',

    'М\(?Д\)?Р': 'МУДР',
    'МЛ\(И\)Т': 'МОЛИТ',
    'МТР#': 'МАТЕРЬ#',
    'МТР': 'МАТЕР',
    'МТ': 'МАТ',
    'МЧНК': 'МУЧЕНИК',
    'МЧН': 'МУЧЕН',
    'М\(С\)Ц': 'МЕСЯЦ',

    'О(\(?Т\)?)?Ц([ЪЬ])': 'ОТЕЦ\\2',
    'О(\(?Т\)?)?ЦМ': 'ОТЦЕМ',
    'О(\(Т\))?Ц': 'ОТЦ',

    'ПСЛМЪ': 'ПСАЛОМЪ',
    'ПСЛМ': 'ПСАЛМ',

    'СЛНЧ': 'СОЛНЕЧ',
    'СЛН': 'СОЛН',
    'СМРТН([ЪЬ])': 'СМЕРТЕН\\1',
    'СПСТИ': 'СПАСТИ',
    'СПС([НТ])': 'СПАСЕ\\1',
    'С[ЪЬ]?ПС': 'СПАС',
    'СРЦ': 'СЕРДЦ',
    'СЩН': 'СВЯЩЕН',
    'СЩ': 'СВЯЩ',

    'УЧН([КЦЧ])': 'УЧЕНИ\\1',
    'УЧН': 'УЧЕН',
    'УЧТЛ': 'УЧИТЕЛ',

    'ЦРКВ([ЪЬ])': 'ЦЕРКОВ\\1',
    'ЦРК\(?В\)?Н': 'ЦЕРКОВН',
    'ЦР[ЪЬ]?К': 'ЦЕРК',
    'ЦРЦ': 'ЦАРИЦ',
    'ЦРВЧ': 'ЦАРЕВИЧ',
    'ЦРВ': 'ЦАРЕВ',
    'ЦР': 'ЦАР',

    'ЧЛВ?([КЦЧ])': 'ЧЕЛОВ+\\1',
    'ЧС': 'ЧАС',
}

abbr_var_super = {
    'Г\(С\)ДН': {
        'сущ': 'ГОСПОДИН',
        '': 'ГОСПОДН',
    },
}

abbr = {
    'А[НГ][ЪЬ]?ГЛ\(С\)К': 'АНГЕЛЬСК',
    'АГ\(?Г\)?Е?Л': 'АНГЕЛ',
    'АН[ЪЬ]ГЛ': 'АНГЕЛ',
    'АП\(С\)Л': 'АПОСТОЛ',

    'БГ\(О\)В': 'БОГОВ',
    'БЖ\(С\)ТВ': 'БОЖЕСТВ',
    'БЛА?\(?Ж\)?Н': 'БЛАЖЕН',
    'БЛГ?О?\(?С\)?ВН': 'БЛАГОСЛОВЕН',
    'БЛС\(В\)Н': 'БЛАГОСЛОВЕН',
    'БЛГ?О?\(?С\)?В': 'БЛАГОСЛОВ',
    'БЛГ\(Д\)Р': 'БЛАГОДАР',
    'БЛГО?\(Д\)Т': 'БЛАГОДАТ',
    'БЛА?\(Г\)': 'БЛАГО',
    'Б\(ДИ?\)Ц': 'БОГОРОДИЦ',

    'ВЛ\(Д\)ЧЦ': 'ВЛАДЫЧИЦ',
    'ВЛ\(Д\)([КЦЧ])': 'ВЛАДЫ\\1',
    'В[ОЪ]СКР\(С\)Н': 'ВОСКРЕСЕН',

    'ГЛ\(С\)': 'ГЛАС',
    'Г\(С\)В': 'ГОСПОДЕВ',
    'Г\(С\)ДРВ': 'ГОСУДАРЕВ',
    'Г\(С\)ДР': 'ГОСУДАР',
    'Г\(С\)Ж': 'ГОСПОЖ',
    'Г\(С\)Д?': 'ГОСПОД',

    'ДР\(В\)Н([ЪЬ])': 'ДЕРЕВЕН\\1',
    'ДР\(В\)Н': 'ДЕРЕВН',

    'ЕВА?\(Г\)Л': 'ЕВАНГЕЛ',
    'ЕП\(С\)К?П': 'ЕПИСКОП',
    'Е\(С\)СТВ': 'ЕСТЕСТВ',

    'ИЕР\(С\)ЛМ': 'ИЕРУСАЛИМ',
    'ИЕР\(С\)Л': 'ИЕРУСАЛ',
    'ИИСЪ': 'ИИСУСЪ',
    'И\(С\)С': 'ИИСУС',
    'ИС\([ОС]\)В': 'ИИСУСОВ',

    'КР\(С\)ТЛ': 'КРЕСТИТЕЛ',
    'КР\(С\)': 'КРЕС',

    'МДР\(С\)Т': 'МУДРОСТ',
    'ПРМ\(Д\)Р': 'ПРЕМУДР',
    'М\(Д\)Р': 'МУДР',
    'М\(О\)ЛТВ': 'МОЛИТВ',
    'МЛ\(С\)РД': 'МИЛОСЕРД',
    'МЛ\(С\)ТВ': 'МИЛОСТИВ',
    'МЛ\(С\)ТН': 'МИЛОСТЫН',
    'МЛ\(С\)Т': 'МИЛОСТ',
    'МЛ\(Д\)Н': 'МЛАДЕН',
    'МН\(С\)Т[ИЫ]?Р': 'МОНАСТЫР',
    'М\(С\)Ц': 'МЕСЯЦ',
    '\(?М\)?СК': 'МОСК',
    'М\(Ч\)НК': 'МУЧЕНИК',

    'НА\(Ч\)Л': 'НАЧАЛ',
    'НЕ?Б\(С\)Н': 'НЕБЕСН',
    '\(Н\)Б\(С\)': 'НЕБЕС',
    'Н\(Е\)Б\(С\)': 'НЕБЕС',
    'ПН\(Д\)Л': 'ПОНЕДЕЛ',
    'НЕ?\(Д\)Л': 'НЕДЕЛ',

    'ОБА\(Ч\)': 'ОБАЧЕ',

    'ПРВЕ?\(Д\)Н': 'ПРАВЕДН',
    'ПРВЕ\(Д\)': 'ПРАВЕД',
    'ПРВ\(Д\)': 'ПРАВД',
    'ПРП\(Д\)БН([ЪЬ])': 'ПРЕПОДОБЕН\\1',
    'ПРП\(Д\)О?Б': 'ПРЕПОДОБ',
    'ПРПО?\(ДО\)Б': 'ПРЕПОДОБ',
    'ПРРЧ\(С\)Т': 'ПРОРОЧЕСТ',
    'ПРР([КЦЧ])': 'ПРОРО\\1',
    'ПРР': 'ПРОР',
    'ПР\(С\)Н': 'ПРИСН',
    'ПР\(С\)ТО?Л': 'ПРЕСТОЛ',
    'ПР\(С\)Т': 'ПРЕСВЯТ',
    'П\(С\)ЛМ': 'ПСАЛМ',

    'РОДИТ\(Л\)': 'РОДИТЕЛ',

    'СВ\+\(Д\)ТЕЛ': 'СВ+Д+ТЕЛ',
    'СП\(С\)ТИ': 'СПАСТИ',
    'СП\(С\)([НТ])': 'СПАСЕ\\1',
    'СР\(Д\)Ц([ЪЬ])': 'СЕРДЕ\\1',
    'СР\(Д\)Ч': 'СЕРДЕЧ',
    'СР\(Д\)': 'СЕРД',
    'СТР\(С\)Т': 'СТРАСТ',

    'ТР\(О\)([ЦЧ])': 'ТРОИ\\1',

    'Х\(С\)([ВМС])': 'ХРИСТО\\1',
    'ХР?\(С\)Т?': 'ХРИСТ',
    'ЦР\(С\)': 'ЦАРС',
    'ЧЛЧ\(С\)К': 'ЧЕЛОВ+ЧЕСК',
    'ЧЛВ([ЦЧ])': 'ЧЕЛОВ\\1',

    'БЛГОЧ\(С\)ТИ?В': 'БЛАГОЧЕСТИВ',
    'БЛГОЧ\(С\)Т': 'БЛАГОЧЕСТ',
    'НЕЧ\(С\)ТИ?В': 'НЕЧЕСТИВ',
    'НЕЧ\(С\)Т': 'НЕЧИСТ',
    'ПОЧ\(С\)Т': 'ПОЧЕСТ',
    'ОЧ\(С\)Т': 'ОЧИСТ',
    'ПРЕ?Ч\(С\)Т(Е)?Н': 'ПРЕЧЕСТ\\1Н',
    'ПРЕ?Ч\(С\)ТИ': 'ПРЕЧЕСТИ',
    'ПРЕ?Ч\(С\)Т': 'ПРЕЧИСТ',
    'ПРИ\(Ч\)СТ': 'ПРИЧАСТ',
    'Ч\(С\)ТВ': 'ЧЕСТИВ',
    'Ч\(С\)Т(Е)?Н': 'ЧЕСТ\\1Н',
    'Ч\(С\)ТИ': 'ЧЕСТИ',
    'Ч\(С\)ТН([ЪЬ])': 'ЧЕСТЕН\\1',
    'Ч\(С\)ТОТ': 'ЧИСТОТ',
}

abbr_var_sub = {
    'Ч\(С\)Т': {
        'прил': 'ЧИСТ',
        '': 'ЧЕСТ',
    }
}

not_on_end = {
    '\(([БВЗКМПРХ])\)': '\\1',
    '([ГКХ])Ь': '\\1',
}

varia = {
    '\(([+АЕИОУЫЮЯ]|ГО)\)': '\\1',

    'ВР[ЪЬ]([ГЖЗХШ]|СТ)': 'ВЕР\\1',
    'ГР[ЪЬ]([ДЖ])': 'ГОР\\1',
    'ДЛ[ЪЬ]([ГЖЗ])': 'ДОЛ\\1',
    'ДР[ЪЬ]([ЖЗ])': 'ДЕР\\1',
    'ЖР[ЪЬ]Т': 'ЖЕРТ',
    'КР[ЪЬ]М': 'КОРМ',
    'МЛ[ЪЬ]К': 'МЛЕК',
    'МЛ[ЪЬ]Ч': 'МОЛЧ',
    'МЛ[ЪЬ]СТ': 'МОЛВСТ',
    'МЛ[ЪЬ]В': 'МОЛВ',
    'МР[ЪЬ]Т': 'МЕРТ',
    'ПР[ЪЬ](В|СТ)': 'ПЕР\\1',
    'СКР[ЪЬ]Б': 'СКОРБ',
    'СР[ЪЬ]([ДЖ])': 'СЕР\\1',
    'СТ[ЪЬ]ЛП': 'СТОЛП',
    'ТВР[ЪЬ]([ДЖ])': 'ТВЕР\\1',
    'ТР[ЪЬ]([ГЖ])': 'ТОР\\1',
    'ТР[ЪЬ]П': 'ТЕРП',

    'АА': 'АЯ',
    'АЯ([ХШ])': 'А\\1',
    '([+ЕИОУЫЯ])А': '\\1Я',

    'ЬЕ([ВМЮ])': 'ИЕ\\1',
    'Ь([ИЯ])([МХ])': 'И\\1\\2',

    'ЖЬ([ЦЧ])': 'Ж\\1',
    'ЧЬ([ШЩ])': 'Ч\\1',
    '([ГКХ])Ы': '\\1И',
    '([ЖЧШЩ])ЬН': '\\1Н',
    '([ЖЦШЩ])Ы': '\\1И',
    '([ЖЦШЩ])Ю': '\\1У',
    '([ЦЧШЩ])Я': '\\1А',

    '\(Ж\)СК': 'ЖСК',
    '\(Ж\)СТВ': 'ЖЕСТВ',
    '\(Л\)С(К|ТВ)': 'ЛЬС\\1',
    '\(([ЧШ])\)С(К|ТВ)': '\\1ЕС\\2',
}

on_end = {
    '([АЯ])\(Ш\)': '\\1ШЕ',

    '([ЕЮ])\(Т\)': '\\1ТЪ',
    '([ИУ])\(Г\)': '\\1ГЪ',
    # '\(([БВКМПХ])\)': '\\1Ъ',
    '([ВГКМХ])Ь': '\\1Ъ',
    # '([ВДЗЛМСТ])': '\\1Ъ',
    '([ЖЦЧШЩ])Ъ': '\\1Ь',
    # '\(?([ЦЩ])\)?': '\\1Ь',

    'ЦИ': 'ЦЫ',
    'Ь([+АЕИУЮЯ])': 'И\\1',

    '([ШЩ])([АЕИУ])\(С\)': '\\1\\2СЯ',
    'Т([ЕИ])\(С\)': 'Т\\1СЯ',
    '([МТ])([ЪЬ])\(С\)': '\\1\\2СЯ',
    '(СТА|ХУ)\(С\)': '\\1СЯ',
    'БЫ\(С\)': 'БЫСТЬ',

    'О\(Ц\)': 'ОТЕЦ',
    'О\(Ч\)': 'ОТЧЕ',
}

on_end_var = {
    '([АЕОЯ])\(Г\)': {
        'сущ': '\\1ГЪ',
        '': '\\1ГО',
    },

    '\(Ж\)': {
        'сущ': 'ЖЬ',
        '': 'ЖЕ',
    },

    '\(С\)': {
        'гл/в': 'СЯ',
        'прич/в': 'СЯ',
        '': '(С)',
    },
}

errors = {
    'ГЛАГОЛ([ВХШ]|ТИ)': 'ГЛАГОЛА\\1',
    'ГЛАГОЛМ': 'ГЛАГОЛЕМ',
    'ГЛАГОЛЩ': 'ГЛАГОЛЮЩ',
    'ГЛАГОЛС': 'ГЛАС',
    'ГОСПОДНЬ': 'ГОСПОДЕНЬ',
    'ЕСТСТВ': 'ЕСТЕСТВ',
    'ИМРК': 'ИМЯРЕК',
    'ЮРЕВ': 'ЮРИЕВ',

    'АВРАЯ': 'АВРАА',
    'ВНЕЗАЯП': 'ВНЕЗАП',
    'ДИЯВОЛ': 'ДИАВОЛ',
    'ИОЯ': 'ИОА',
    'ИСАЯК': 'ИСААК',
    'ИЯ([КЧ])': 'ИА\\1',
    'ИЯСАФ': 'ИАСАФ',
    'КАШ([АЕ])С': 'КАЯШ\\1С',
    'ЛУКИЯН': 'ЛУКИАН',
    'МАРТИЯН': 'МАРТИАН',
    'О\(?Т\)?ЧА([ХШ])': 'ОТЧАЯ\\1',
    'ПАТРИЯР': 'ПАТРИАР',
    'РАВНОЯ': 'РАВНОА',
    'ФЕВРУЯР': 'ФЕВРУАР',
    'ФИМИЯ([МН])': 'ФИМИА\\1',
    'ХРИСТИЯН': 'ХРИСТИАН',
    'ЯРХ': 'АРХ',

    '([ЖЧШЩ])СТВ': '\\1ЕСТВ',
    'ЖЕСК': 'ЖСК',
    '([ЧШЩ])СК': '\\1ЕСК',
    'ШМЪ': 'ШМЪ#',

    '(%s)ВЪ' % '|'.join((
        'ЛЮБО',
        'ПЛАВ',
        'Я',
    )): '\\1ВЬ',
}

errors_on_start = {
    '(ВОЗ|ПО)?ДА(ШЕ|Х)': '\\1ДАЯ\\2',
    'ТА(ШЕ|Х)': 'ТАЯ\\1',

    '(%s)ВЪ' % '|'.join((
        'БРО',
        'ВЕР',
        'ВЕТ',
        'ВНО',
        'ВКРИ',
        'МОЛ',
        'МОРКО',
        'НА',
        'СВЕКРО',
        'ХОРУГ',
        'ЦЕРКО',
        'ЧЕР',
        'ЯТО'
    )): '\\1ВЬ',
}
