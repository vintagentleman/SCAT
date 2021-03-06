vows = ('+', 'А', 'Е', 'И', 'О', 'У', 'Ъ', 'Ы', 'Ь', 'Ю', 'Я',)
cons = ('Б', 'В', 'Г', 'Д', 'Ж', 'З', 'К', 'Л', 'М', 'Н', 'П', 'Р', 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ',)

cons_soft = ('З', 'Л', 'Н', 'Р', 'С',)
cons_hush = ('Ж', 'ЖД', 'Ц', 'Ч', 'Ш', 'ШТ', 'Щ',)
cons_sonor = ('Л', 'М', 'Н', 'Р',)
cons_palat = ('К', 'Г', 'Х',)

palat_1 = {'Ч': 'К', 'Ж': 'Г', 'Ш': 'Х'}
palat_1_jo = {'Ч': 'Ц', 'Ж': 'З', 'Ш': 'С'}
palat_2 = {'Ц': 'К', 'З': 'Г', 'С': 'Х', 'Т': 'К'}

letter_values = {
    'А': 1,
    'В': 2,
    'Г': 3,
    'Д': 4,
    'Е': 5,
    'S': 6,
    'З': 7,
    'И': 8,
    'I': 10,
    'К': 20,
    'Л': 30,
    'М': 40,
    'Н': 50,
    'О': 70,
    'П': 80,
    'Р': 100,
    'С': 200,
    'Т': 300,
    'U': 400,
    'D': 400,
    'Ф': 500,
    'Х': 600,
    'W': 800,
    'Ц': 900,
    'Ч': 90,
    'R': 900,
    'L': 60,
    'Q': 700,
    'F': 9,
    'V': 400,
}

nom_infl = {
    # *a, мужской род
    ('a', 'им', 'ед', 'м'): 'А',
    ('a', 'род', 'ед', 'м'): '[ИЫ]',
    ('a', 'дат', 'ед', 'м'): '[+ЕИЫ]',
    ('a', 'вин', 'ед', 'м'): 'У',
    ('a', 'тв', 'ед', 'м'): 'ОЮ',
    ('a', 'мест', 'ед', 'м'): '[+ЕИЫ]',
    ('a', 'зв', 'ед', 'м'): 'О',

    ('a', 'им', 'дв', 'м'): '[+Е]',
    ('a', 'род', 'дв', 'м'): 'У',
    ('a', 'дат', 'дв', 'м'): 'АМА',
    ('a', 'вин', 'дв', 'м'): '[+Е]',
    ('a', 'тв', 'дв', 'м'): 'АМА',
    ('a', 'мест', 'дв', 'м'): 'У',
    ('a', 'зв', 'дв', 'м'): '[+Е]',

    ('a', 'им', 'мн', 'м'): '[ИЫ]',
    ('a', 'род', 'мн', 'м'): '[ЪЬ]',
    ('a', 'дат', 'мн', 'м'): 'АМ[ЪЬ`]',
    ('a', 'вин', 'мн', 'м'): '[ИЫ]',
    ('a', 'тв', 'мн', 'м'): 'АМИ',
    ('a', 'мест', 'мн', 'м'): 'АХ[ЪЬ`]',
    ('a', 'зв', 'мн', 'м'): '[ИЫ]',

    # *ja, мужской род
    ('ja', 'им', 'ед', 'м'): '[АИЫЯ]',
    ('ja', 'род', 'ед', 'м'): '[+АЕИЫЯ]',
    ('ja', 'дат', 'ед', 'м'): '[+ЕИЫ]',
    ('ja', 'вин', 'ед', 'м'): '[УЮ]',
    ('ja', 'тв', 'ед', 'м'): '[ЕО]Ю',
    ('ja', 'мест', 'ед', 'м'): '[+ЕИЫ]',
    ('ja', 'зв', 'ед', 'м'): '[+Е]',

    ('ja', 'им', 'дв', 'м'): '[ИЫ]',
    ('ja', 'род', 'дв', 'м'): '[УЮ]',
    ('ja', 'дат', 'дв', 'м'): '[АЯ]МА',
    ('ja', 'вин', 'дв', 'м'): '[ИЫ]',
    ('ja', 'тв', 'дв', 'м'): '[АЯ]МА',
    ('ja', 'мест', 'дв', 'м'): '[УЮ]',
    ('ja', 'зв', 'дв', 'м'): '[ИЫ]',

    ('ja', 'им', 'мн', 'м'): '[+АЕИЫЯ]',
    ('ja', 'род', 'мн', 'м'): '[+ЕИЫ]И|[ЪЬ]',
    ('ja', 'дат', 'мн', 'м'): '[АЯ]М[ЪЬ`]',
    ('ja', 'вин', 'мн', 'м'): '[+АЕИЫЯ]',
    ('ja', 'тв', 'мн', 'м'): '[АЯ]МИ',
    ('ja', 'мест', 'мн', 'м'): '[АЯ]Х[ЪЬ`]',
    ('ja', 'зв', 'мн', 'м'): '[+АЕИЫЯ]',

    # *a, женский род
    ('a', 'им', 'ед', 'ж'): 'А',
    ('a', 'род', 'ед', 'ж'): '[ИЫ]',
    ('a', 'дат', 'ед', 'ж'): '[+ЕИЫ]',
    ('a', 'вин', 'ед', 'ж'): 'У',
    ('a', 'тв', 'ед', 'ж'): 'ОЮ',
    ('a', 'мест', 'ед', 'ж'): '[+ЕИЫ]',
    ('a', 'зв', 'ед', 'ж'): 'О',

    ('a', 'им', 'дв', 'ж'): '[+Е]',
    ('a', 'род', 'дв', 'ж'): 'У',
    ('a', 'дат', 'дв', 'ж'): 'АМА',
    ('a', 'вин', 'дв', 'ж'): '[+Е]',
    ('a', 'тв', 'дв', 'ж'): 'АМА',
    ('a', 'мест', 'дв', 'ж'): 'У',
    ('a', 'зв', 'дв', 'ж'): '[+Е]',

    ('a', 'им', 'мн', 'ж'): '[ИЫ]',
    ('a', 'род', 'мн', 'ж'): '[ЪЬ]',
    ('a', 'дат', 'мн', 'ж'): 'АМ[ЪЬ`]',
    ('a', 'вин', 'мн', 'ж'): '[ИЫ]',
    ('a', 'тв', 'мн', 'ж'): 'АМИ',
    ('a', 'мест', 'мн', 'ж'): 'АХ[ЪЬ`]',
    ('a', 'зв', 'мн', 'ж'): '[ИЫ]',

    # *ja, женский род
    ('ja', 'им', 'ед', 'ж'): '[АЯИЫ]',
    ('ja', 'род', 'ед', 'ж'): '[+АЕИЫЯ]',
    ('ja', 'дат', 'ед', 'ж'): '[+ЕИЫ]',
    ('ja', 'вин', 'ед', 'ж'): '[УЮ]',
    ('ja', 'тв', 'ед', 'ж'): '[ЕО]Ю',
    ('ja', 'мест', 'ед', 'ж'): '[+ЕИЫ]',
    ('ja', 'зв', 'ед', 'ж'): '[+Е]',

    ('ja', 'им', 'дв', 'ж'): '[ИЫ]',
    ('ja', 'род', 'дв', 'ж'): '[УЮ]',
    ('ja', 'дат', 'дв', 'ж'): '[АЯ]МА',
    ('ja', 'вин', 'дв', 'ж'): '[ИЫ]',
    ('ja', 'тв', 'дв', 'ж'): '[АЯ]МА',
    ('ja', 'мест', 'дв', 'ж'): '[УЮ]',
    ('ja', 'зв', 'дв', 'ж'): '[ИЫ]',

    ('ja', 'им', 'мн', 'ж'): '[+АЕИЫЯ]',
    ('ja', 'род', 'мн', 'ж'): '[+ЕИЫ]И|[ЪЬ]',
    ('ja', 'дат', 'мн', 'ж'): '[АЯ]М[ЪЬ`]',
    ('ja', 'вин', 'мн', 'ж'): '[+АЕИЫЯ]',
    ('ja', 'тв', 'мн', 'ж'): '[АЯ]МИ',
    ('ja', 'мест', 'мн', 'ж'): '[АЯ]Х[ЪЬ`]',
    ('ja', 'зв', 'мн', 'ж'): '[+АЕИЫЯ]',

    # *o, мужской род
    ('o', 'им', 'ед', 'м'): '[ЪЬ]',
    ('o', 'род', 'ед', 'м'): 'А',
    ('o', 'дат', 'ед', 'м'): 'У',
    ('o', 'вин', 'ед', 'м'): '[АЪЬ]',
    ('o', 'тв', 'ед', 'м'): 'ОМ[ЪЬ`]',
    ('o', 'мест', 'ед', 'м'): '[+ЕИЫ]',
    ('o', 'зв', 'ед', 'м'): '[+Е]',

    ('o', 'им', 'дв', 'м'): 'А',
    ('o', 'род', 'дв', 'м'): 'У',
    ('o', 'дат', 'дв', 'м'): 'ОМА',
    ('o', 'вин', 'дв', 'м'): 'А',
    ('o', 'тв', 'дв', 'м'): 'ОМА',
    ('o', 'мест', 'дв', 'м'): 'У',
    ('o', 'зв', 'дв', 'м'): 'А',

    ('o', 'им', 'мн', 'м'): '[ИЫ]',
    ('o', 'род', 'мн', 'м'): '[ЪЬ]',
    ('o', 'дат', 'мн', 'м'): 'ОМ[ЪЬ`]',
    ('o', 'вин', 'мн', 'м'): '[ИЫ]',
    ('o', 'тв', 'мн', 'м'): '[ИЫ]',
    ('o', 'мест', 'мн', 'м'): '[+Е]Х[ЪЬ`]',
    ('o', 'зв', 'мн', 'м'): '[ИЫ]',

    # *jo, мужской род
    ('jo', 'им', 'ед', 'м'): '[+ЕИЪЬ]',
    ('jo', 'род', 'ед', 'м'): '[АЯ]',
    ('jo', 'дат', 'ед', 'м'): '[УЮ]',
    ('jo', 'вин', 'ед', 'м'): '[+АЕИЪЬЯ]',
    ('jo', 'тв', 'ед', 'м'): '[+ЕО]М[ЪЬ`]',
    ('jo', 'мест', 'ед', 'м'): '[+ЕИЫ]',
    ('jo', 'зв', 'ед', 'м'): '[+ЕУЮ]',

    ('jo', 'им', 'дв', 'м'): '[АЯ]',
    ('jo', 'род', 'дв', 'м'): '[УЮ]',
    ('jo', 'дат', 'дв', 'м'): '[+ЕО]МА',
    ('jo', 'вин', 'дв', 'м'): '[АЯ]',
    ('jo', 'тв', 'дв', 'м'): '[+ЕО]МА',
    ('jo', 'мест', 'дв', 'м'): '[УЮ]',
    ('jo', 'зв', 'дв', 'м'): '[АЯ]',

    ('jo', 'им', 'мн', 'м'): '[+ЕИЫ]',
    ('jo', 'род', 'мн', 'м'): '[ИЪЬЫ]',
    ('jo', 'дат', 'мн', 'м'): '[+ЕО]М[ЪЬ`]',
    ('jo', 'вин', 'мн', 'м'): '[+АЕИЫЯ]',
    ('jo', 'тв', 'мн', 'м'): '[ИЫ]',
    ('jo', 'мест', 'мн', 'м'): '[+ЕИ]Х[ЪЬ`]',
    ('jo', 'зв', 'мн', 'м'): '[ИЫ]',

    # *o, средний род
    ('o', 'им', 'ед', 'ср'): 'О',
    ('o', 'род', 'ед', 'ср'): 'А',
    ('o', 'дат', 'ед', 'ср'): 'У',
    ('o', 'вин', 'ед', 'ср'): 'О',
    ('o', 'тв', 'ед', 'ср'): 'ОМ[ЪЬ`]',
    ('o', 'мест', 'ед', 'ср'): '[+ЕИЫ]',
    ('o', 'зв', 'ед', 'ср'): 'О',

    ('o', 'им', 'дв', 'ср'): '[+Е]',
    ('o', 'род', 'дв', 'ср'): 'У',
    ('o', 'дат', 'дв', 'ср'): 'ОМА',
    ('o', 'вин', 'дв', 'ср'): '[+Е]',
    ('o', 'тв', 'дв', 'ср'): 'ОМА',
    ('o', 'мест', 'дв', 'ср'): 'У',
    ('o', 'зв', 'дв', 'ср'): '[+Е]',

    ('o', 'им', 'мн', 'ср'): 'А',
    ('o', 'род', 'мн', 'ср'): '[ЪЬ]',
    ('o', 'дат', 'мн', 'ср'): 'ОМ[ЪЬ`]',
    ('o', 'вин', 'мн', 'ср'): 'А',
    ('o', 'тв', 'мн', 'ср'): '[ИЫ]',
    ('o', 'мест', 'мн', 'ср'): '[+Е]Х[ЪЬ`]',
    ('o', 'зв', 'мн', 'ср'): 'А',

    # *jo, средний род
    ('jo', 'им', 'ед', 'ср'): '[ЕО]',
    ('jo', 'род', 'ед', 'ср'): '[АЯ]',
    ('jo', 'дат', 'ед', 'ср'): '[УЮ]',
    ('jo', 'вин', 'ед', 'ср'): '[ЕО]',
    ('jo', 'тв', 'ед', 'ср'): '[+ЕО]М[ЪЬ`]',
    ('jo', 'мест', 'ед', 'ср'): '[+ЕИЫ]',
    ('jo', 'зв', 'ед', 'ср'): '[+Е]',

    ('jo', 'им', 'дв', 'ср'): '[ИЫ]',
    ('jo', 'род', 'дв', 'ср'): '[УЮ]',
    ('jo', 'дат', 'дв', 'ср'): '[+ЕО]МА',
    ('jo', 'вин', 'дв', 'ср'): '[ИЫ]',
    ('jo', 'тв', 'дв', 'ср'): '[+ЕО]МА',
    ('jo', 'мест', 'дв', 'ср'): '[УЮ]',
    ('jo', 'зв', 'дв', 'ср'): '[ИЫ]',

    ('jo', 'им', 'мн', 'ср'): '[АЯ]',
    ('jo', 'род', 'мн', 'ср'): '[ИЪЬЫ]',
    ('jo', 'дат', 'мн', 'ср'): '[+ЕО]М[ЪЬ`]',
    ('jo', 'вин', 'мн', 'ср'): '[АЯ]',
    ('jo', 'тв', 'мн', 'ср'): '[ИЫ]',
    ('jo', 'мест', 'мн', 'ср'): '[+ЕИ]Х[ЪЬ`]',
    ('jo', 'зв', 'мн', 'ср'): '[АЯ]',

    # *u, мужской род
    ('u', 'им', 'ед', 'м'): '[ЪЬ]',
    ('u', 'род', 'ед', 'м'): 'У',
    ('u', 'дат', 'ед', 'м'): '[+ЕО]ВИ',
    ('u', 'вин', 'ед', 'м'): '[ЪЬ]',
    ('u', 'тв', 'ед', 'м'): '[+ЕОЪЬ]М[ЪЬ`]',
    ('u', 'мест', 'ед', 'м'): 'У',
    ('u', 'зв', 'ед', 'м'): 'У',

    ('u', 'им', 'дв', 'м'): 'Ы',
    ('u', 'род', 'дв', 'м'): 'У',
    ('u', 'дат', 'дв', 'м'): '[+ЕОЪЬ]?МА',
    ('u', 'вин', 'дв', 'м'): 'Ы',
    ('u', 'тв', 'дв', 'м'): '[+ЕОЪЬ]?МА',
    ('u', 'мест', 'дв', 'м'): 'У',
    ('u', 'зв', 'дв', 'м'): 'Ы',

    ('u', 'им', 'мн', 'м'): '[+ЕО]ВЕ',
    ('u', 'род', 'мн', 'м'): '[+ЕО]В[ЪЬ`]',
    ('u', 'дат', 'мн', 'м'): '([+ЕО]В)?[+ЕОЪЬ]М[ЪЬ`]',
    ('u', 'вин', 'мн', 'м'): 'Ы',
    ('u', 'тв', 'мн', 'м'): '([+ЕО]В)?[+ЕОЪЬ]?МИ',
    ('u', 'мест', 'мн', 'м'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('u', 'зв', 'мн', 'м'): '[ЕО]ВЕ',

    # *i, мужской род
    ('i', 'им', 'ед', 'м'): '[ЪЬ]',
    ('i', 'род', 'ед', 'м'): 'И',
    ('i', 'дат', 'ед', 'м'): '[+ЕИ]',
    ('i', 'вин', 'ед', 'м'): '[ЪЬ]',
    ('i', 'тв', 'ед', 'м'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('i', 'мест', 'ед', 'м'): '[+ЕИ]',
    ('i', 'зв', 'ед', 'м'): 'И',

    ('i', 'им', 'дв', 'м'): 'И',
    ('i', 'род', 'дв', 'м'): '[ИЪЬ]?Ю',
    ('i', 'дат', 'дв', 'м'): '[ИЪЬ]?МА',
    ('i', 'вин', 'дв', 'м'): 'И',
    ('i', 'тв', 'дв', 'м'): '[ИЪЬ]?МА',
    ('i', 'мест', 'дв', 'м'): '[ИЪЬ]?Ю',
    ('i', 'зв', 'дв', 'м'): 'И',

    ('i', 'им', 'мн', 'м'): '[ИЪЬ]?Е',
    ('i', 'род', 'мн', 'м'): '[+ЕИЪЬ]?И',
    ('i', 'дат', 'мн', 'м'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('i', 'вин', 'мн', 'м'): 'И',
    ('i', 'тв', 'мн', 'м'): '[+ЕИЪЬ]?МИ',
    ('i', 'мест', 'мн', 'м'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('i', 'зв', 'мн', 'м'): '[ИЪЬ]Е',

    # *i, женский род
    ('i', 'им', 'ед', 'ж'): '[ЪЬ]',
    ('i', 'род', 'ед', 'ж'): 'И',
    ('i', 'дат', 'ед', 'ж'): '[+ЕИ]',
    ('i', 'вин', 'ед', 'ж'): '[ЪЬ]',
    ('i', 'тв', 'ед', 'ж'): '[ИЪЬ]?Ю',
    ('i', 'мест', 'ед', 'ж'): '[+ЕИ]',
    ('i', 'зв', 'ед', 'ж'): 'И',

    ('i', 'им', 'дв', 'ж'): 'И',
    ('i', 'род', 'дв', 'ж'): '[ИЪЬ]?Ю',
    ('i', 'дат', 'дв', 'ж'): '[ИЪЬ]?МА',
    ('i', 'вин', 'дв', 'ж'): 'И',
    ('i', 'тв', 'дв', 'ж'): '[ИЪЬ]?МА',
    ('i', 'мест', 'дв', 'ж'): '[ИЪЬ]?Ю',
    ('i', 'зв', 'дв', 'ж'): 'И',

    ('i', 'им', 'мн', 'ж'): 'И',
    ('i', 'род', 'мн', 'ж'): '[+ЕИЪЬ]?И',
    ('i', 'дат', 'мн', 'ж'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('i', 'вин', 'мн', 'ж'): 'И',
    ('i', 'тв', 'мн', 'ж'): '[+ЕИЪЬ]?МИ',
    ('i', 'мест', 'мн', 'ж'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('i', 'зв', 'мн', 'ж'): 'И',

    # *en, мужской род
    ('en', 'им', 'ед', 'м'): '[ЪЬЫ]',
    ('en', 'род', 'ед', 'м'): '[+ЕИ]',
    ('en', 'дат', 'ед', 'м'): '[+ЕИ]',
    ('en', 'вин', 'ед', 'м'): '[ЪЬЫ]',
    ('en', 'тв', 'ед', 'м'): '[+ЕОЪЬ]М[ЪЬ`]',
    ('en', 'мест', 'ед', 'м'): '[+ЕИ]',
    ('en', 'зв', 'ед', 'м'): '[ЪЬЫ]',

    ('en', 'им', 'дв', 'м'): '[+ЕИ]',
    ('en', 'род', 'дв', 'м'): '[УЮ]',
    ('en', 'дат', 'дв', 'м'): '[ЪЬ]?МА',
    ('en', 'вин', 'дв', 'м'): '[+ЕИ]',
    ('en', 'тв', 'дв', 'м'): '[ЪЬ]?МА',
    ('en', 'мест', 'дв', 'м'): '[УЮ]',
    ('en', 'зв', 'дв', 'м'): '[+ЕИ]',

    ('en', 'им', 'мн', 'м'): '[+ЕИ]',
    ('en', 'род', 'мн', 'м'): '[ЪЬ]',
    ('en', 'дат', 'мн', 'м'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('en', 'вин', 'мн', 'м'): '[+ЕИ]',
    ('en', 'тв', 'мн', 'м'): '[+ЕИЪЬ]?МИ|[+ЕИ]',
    ('en', 'мест', 'мн', 'м'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('en', 'зв', 'мн', 'м'): '[+ЕИ]',

    # *men, средний род
    ('men', 'им', 'ед', 'ср'): '[АЯ]',
    ('men', 'род', 'ед', 'ср'): '[+ЕИ]',
    ('men', 'дат', 'ед', 'ср'): '[+ЕИ]',
    ('men', 'вин', 'ед', 'ср'): '[АЯ]',
    ('men', 'тв', 'ед', 'ср'): '[+ЕОЪЬ]М[ЪЬ`]',
    ('men', 'мест', 'ед', 'ср'): '[+ЕИ]',
    ('men', 'зв', 'ед', 'ср'): '[АЯ]',

    ('men', 'им', 'дв', 'ср'): '[+ЕИ]',
    ('men', 'род', 'дв', 'ср'): '[УЮ]',
    ('men', 'дат', 'дв', 'ср'): '[ЪЬ]?МА',
    ('men', 'вин', 'дв', 'ср'): '[+ЕИ]',
    ('men', 'тв', 'дв', 'ср'): '[ЪЬ]?МА',
    ('men', 'мест', 'дв', 'ср'): '[УЮ]',
    ('men', 'зв', 'дв', 'ср'): '[+ЕИ]',

    ('men', 'им', 'мн', 'ср'): 'А',
    ('men', 'род', 'мн', 'ср'): '[ЪЬ]',
    ('men', 'дат', 'мн', 'ср'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('men', 'вин', 'мн', 'ср'): 'А',
    ('men', 'тв', 'мн', 'ср'): 'Ы',
    ('men', 'мест', 'мн', 'ср'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('men', 'зв', 'мн', 'ср'): 'А',

    # *ent, средний род
    ('ent', 'им', 'ед', 'ср'): '[АЯ]',
    ('ent', 'род', 'ед', 'ср'): '[+ЕИ]',
    ('ent', 'дат', 'ед', 'ср'): '[+ЕИ]',
    ('ent', 'вин', 'ед', 'ср'): '[АЯ]',
    ('ent', 'тв', 'ед', 'ср'): '[+ЕОЪЬ]М[ЪЬ`]',
    ('ent', 'мест', 'ед', 'ср'): '[+ЕИ]',
    ('ent', 'зв', 'ед', 'ср'): '[АЯ]',

    ('ent', 'им', 'дв', 'ср'): '[+ЕИ]',
    ('ent', 'род', 'дв', 'ср'): '[УЮ]',
    ('ent', 'дат', 'дв', 'ср'): '[ЪЬ]?МА',
    ('ent', 'вин', 'дв', 'ср'): '[+ЕИ]',
    ('ent', 'тв', 'дв', 'ср'): '[ЪЬ]?МА',
    ('ent', 'мест', 'дв', 'ср'): '[УЮ]',
    ('ent', 'зв', 'дв', 'ср'): '[+ЕИ]',

    ('ent', 'им', 'мн', 'ср'): 'А',
    ('ent', 'род', 'мн', 'ср'): '[ЪЬ]',
    ('ent', 'дат', 'мн', 'ср'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('ent', 'вин', 'мн', 'ср'): 'А',
    ('ent', 'тв', 'мн', 'ср'): 'Ы',
    ('ent', 'мест', 'мн', 'ср'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('ent', 'зв', 'мн', 'ср'): 'А',

    # *es, средний род
    ('es', 'им', 'ед', 'ср'): 'О',
    ('es', 'род', 'ед', 'ср'): '[+ЕИ]',
    ('es', 'дат', 'ед', 'ср'): '[+ЕИ]',
    ('es', 'вин', 'ед', 'ср'): 'О',
    ('es', 'тв', 'ед', 'ср'): '[+ЕОЪЬ]М[ЪЬ`]',
    ('es', 'мест', 'ед', 'ср'): '[+ЕИ]',
    ('es', 'зв', 'ед', 'ср'): 'О',

    ('es', 'им', 'дв', 'ср'): '[+ЕИ]',
    ('es', 'род', 'дв', 'ср'): '[УЮ]',
    ('es', 'дат', 'дв', 'ср'): '[ЪЬ]?МА',
    ('es', 'вин', 'дв', 'ср'): '[+ЕИ]',
    ('es', 'тв', 'дв', 'ср'): '[ЪЬ]?МА',
    ('es', 'мест', 'дв', 'ср'): '[УЮ]',
    ('es', 'зв', 'дв', 'ср'): '[+ЕИ]',

    ('es', 'им', 'мн', 'ср'): '[+АЕИ]',
    ('es', 'род', 'мн', 'ср'): '[ЪЬ]',
    ('es', 'дат', 'мн', 'ср'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('es', 'вин', 'мн', 'ср'): '[+АЕИ]',
    ('es', 'тв', 'мн', 'ср'): 'Ы',
    ('es', 'мест', 'мн', 'ср'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('es', 'зв', 'мн', 'ср'): '[+АЕИ]',

    # *er, женский род
    ('er', 'им', 'ед', 'ж'): '[+ЕИЪЬ]',
    ('er', 'род', 'ед', 'ж'): '[+ЕИ]',
    ('er', 'дат', 'ед', 'ж'): '[+ЕИ]',
    ('er', 'вин', 'ед', 'ж'): '[+ЕИЪЬ]',
    ('er', 'тв', 'ед', 'ж'): '[ИЪЬ]?Ю',
    ('er', 'мест', 'ед', 'ж'): '[+ЕИ]',
    ('er', 'зв', 'ед', 'ж'): '[+ЕИЪЬ]',

    ('er', 'им', 'дв', 'ж'): '[+ЕИ]',
    ('er', 'род', 'дв', 'ж'): '[УЮ]',
    ('er', 'дат', 'дв', 'ж'): '[ЪЬ]?МА',
    ('er', 'вин', 'дв', 'ж'): '[+ЕИ]',
    ('er', 'тв', 'дв', 'ж'): '[ЪЬ]?МА',
    ('er', 'мест', 'дв', 'ж'): '[УЮ]',
    ('er', 'зв', 'дв', 'ж'): '[+ЕИ]',

    ('er', 'им', 'мн', 'ж'): '[+ЕИ]',
    ('er', 'род', 'мн', 'ж'): '[ЪЬ]',
    ('er', 'дат', 'мн', 'ж'): '[+ЕИЪЬ]М[ЪЬ`]',
    ('er', 'вин', 'мн', 'ж'): '[+ЕИ]',
    ('er', 'тв', 'мн', 'ж'): '[+ЕИЪЬ]?МИ|[+ЕИ]',
    ('er', 'мест', 'мн', 'ж'): '[+ЕИЪЬ]Х[ЪЬ`]',
    ('er', 'зв', 'мн', 'ж'): '[+ЕИ]',

    # *uu, женский род
    ('uu', 'им', 'ед', 'ж'): '[ЪЬЫ]',
    ('uu', 'род', 'ед', 'ж'): '[+ЕИ]',
    ('uu', 'дат', 'ед', 'ж'): '[+ЕИ]',
    ('uu', 'вин', 'ед', 'ж'): '[ЪЬЫ]',
    ('uu', 'тв', 'ед', 'ж'): '[ИЪЬ]?Ю',
    ('uu', 'мест', 'ед', 'ж'): '[+ЕИ]',
    ('uu', 'зв', 'ед', 'ж'): '[ЪЬЫ]',

    ('uu', 'им', 'дв', 'ж'): '[+ЕИ]',
    ('uu', 'род', 'дв', 'ж'): '[УЮ]',
    ('uu', 'дат', 'дв', 'ж'): '[АО]МА',
    ('uu', 'вин', 'дв', 'ж'): '[+ЕИ]',
    ('uu', 'тв', 'дв', 'ж'): '[АО]МА',
    ('uu', 'мест', 'дв', 'ж'): '[УЮ]',
    ('uu', 'зв', 'дв', 'ж'): '[+ЕИ]',

    ('uu', 'им', 'мн', 'ж'): '[+ЕИ]',
    ('uu', 'род', 'мн', 'ж'): '[ЪЬ]',
    ('uu', 'дат', 'мн', 'ж'): '[АО]М[ЪЬ`]',
    ('uu', 'вин', 'мн', 'ж'): '[+ЕИ]',
    ('uu', 'тв', 'мн', 'ж'): '[АО]МИ',
    ('uu', 'мест', 'мн', 'ж'): '[АО]Х[ЪЬ`]',
    ('uu', 'зв', 'мн', 'ж'): '[+ЕИ]',
}

pron_infl = {
    # Твёрдый подтип, мужской род
    ('тв', 'им', 'ед', 'м'): '[ИЫ]И?|ОИ',
    ('тв', 'род', 'ед', 'м'): 'А?[АЕО]?ГО',
    ('тв', 'дат', 'ед', 'м'): 'У?[ЕОУ]?МУ',
    ('тв', 'вин', 'ед', 'м'): '[ИЫ]И?|ОИ',
    ('тв', 'тв', 'ед', 'м'): '[ИЫ]?[+ЕИЫ]М[ЪЬ`]',
    ('тв', 'мест', 'ед', 'м'): '[+Е]?[+ЕО]М[ЪЬ`]',
    ('тв', 'зв', 'ед', 'м'): '[ИЫ]И?|ОИ',

    ('тв', 'им', 'дв', 'м'): 'А[АЯ]',
    ('тв', 'род', 'дв', 'м'): '[ОУ]Ю',
    ('тв', 'дат', 'дв', 'м'): '[ИЫ]?[+ЕИЫ]?МА',
    ('тв', 'вин', 'дв', 'м'): 'А[АЯ]',
    ('тв', 'тв', 'дв', 'м'): '[ИЫ]?[+ЕИЫ]?МА',
    ('тв', 'мест', 'дв', 'м'): '[ОУ]Ю',
    ('тв', 'зв', 'дв', 'м'): 'А[АЯ]',
    
    ('тв', 'им', 'мн', 'м'): 'ИИ',
    ('тв', 'род', 'мн', 'м'): '[ИЫ]?[+ЕИЫ]Х[ЪЬ`]',
    ('тв', 'дат', 'мн', 'м'): '[ИЫ]?[+ЕИЫ]М[ЪЬ`]',
    ('тв', 'вин', 'мн', 'м'): '[ИЫ][АЕИЯ]',
    ('тв', 'тв', 'мн', 'м'): '[ИЫ]?[+ЕИЫ]?МИ',
    ('тв', 'мест', 'мн', 'м'): '[ИЫ]?[+ЕИЫ]Х[ЪЬ`]',
    ('тв', 'зв', 'мн', 'м'): 'ИИ',

    # Твёрдый подтип, женский род
    ('тв', 'им', 'ед', 'ж'): 'А[АЯ]',
    ('тв', 'род', 'ед', 'ж'): '[ИОЫ][АЕИЯ]',
    ('тв', 'дат', 'ед', 'ж'): '[+ЕО]И',
    ('тв', 'вин', 'ед', 'ж'): '[ОУ]Ю',
    ('тв', 'тв', 'ед', 'ж'): '[ОУ]Ю',
    ('тв', 'мест', 'ед', 'ж'): '[+ЕО]И',
    ('тв', 'зв', 'ед', 'ж'): 'А[АЯ]',

    ('тв', 'им', 'дв', 'ж'): '[+Е]И',
    ('тв', 'род', 'дв', 'ж'): '[ОУ]Ю',
    ('тв', 'дат', 'дв', 'ж'): '[ИЫ]?[+ЕИЫ]?МА',
    ('тв', 'вин', 'дв', 'ж'): '[+Е]И',
    ('тв', 'тв', 'дв', 'ж'): '[ИЫ]?[+ЕИЫ]?МА',
    ('тв', 'мест', 'дв', 'ж'): '[ОУ]Ю',
    ('тв', 'зв', 'дв', 'ж'): '[+Е]И',

    ('тв', 'им', 'мн', 'ж'): '[ИЫ][АЕИЯ]',
    ('тв', 'род', 'мн', 'ж'): '[ИЫ]?[+ЕИЫ]Х[ЪЬ`]',
    ('тв', 'дат', 'мн', 'ж'): '[ИЫ]?[+ЕИЫ]М[ЪЬ`]',
    ('тв', 'вин', 'мн', 'ж'): '[ИЫ][АЕИЯ]',
    ('тв', 'тв', 'мн', 'ж'): '[ИЫ]?[+ЕИЫ]?МИ',
    ('тв', 'мест', 'мн', 'ж'): '[ИЫ]?[+ЕИЫ]Х[ЪЬ`]',
    ('тв', 'зв', 'мн', 'ж'): '[ИЫ][АЕИЯ]',

    # Твёрдый подтип, средний род
    ('тв', 'им', 'ед', 'ср'): 'О?Е',
    ('тв', 'род', 'ед', 'ср'): 'А?[АЕО]?ГО',
    ('тв', 'дат', 'ед', 'ср'): 'У?[ЕОУ]?МУ',
    ('тв', 'вин', 'ед', 'ср'): 'О?Е',
    ('тв', 'тв', 'ед', 'ср'): '[ИЫ]?[+ЕИЫ]М[ЪЬ`]',
    ('тв', 'мест', 'ед', 'ср'): '[+Е]?[+ЕО]М[ЪЬ`]',
    ('тв', 'зв', 'ед', 'ср'): 'О?Е',

    ('тв', 'им', 'дв', 'ср'): '[+Е]И',
    ('тв', 'род', 'дв', 'ср'): '[ОУ]Ю',
    ('тв', 'дат', 'дв', 'ср'): '[ИЫ]?[+ЕИЫ]?МА',
    ('тв', 'вин', 'дв', 'ср'): '[+Е]И',
    ('тв', 'тв', 'дв', 'ср'): '[ИЫ]?[+ЕИЫ]?МА',
    ('тв', 'мест', 'дв', 'ср'): '[ОУ]Ю',
    ('тв', 'зв', 'дв', 'ср'): '[+Е]И',

    ('тв', 'им', 'мн', 'ср'): 'А[АЯ]|[ИЫ][АЕИЯ]',
    ('тв', 'род', 'мн', 'ср'): '[ИЫ]?[+ЕИЫ]Х[ЪЬ`]',
    ('тв', 'дат', 'мн', 'ср'): '[ИЫ]?[+ЕИЫ]М[ЪЬ`]',
    ('тв', 'вин', 'мн', 'ср'): 'А[АЯ]|[ИЫ][АЕИЯ]',
    ('тв', 'тв', 'мн', 'ср'): '[ИЫ]?[+ЕИЫ]?МИ',
    ('тв', 'мест', 'мн', 'ср'): '[ИЫ]?[+ЕИЫ]Х[ЪЬ`]',
    ('тв', 'зв', 'мн', 'ср'): 'А[АЯ]|[ИЫ][АЕИЯ]',

    # Мягкий подтип, мужской род
    ('м', 'им', 'ед', 'м'): '[ИЪЬЫ]?И|ОИ',
    ('м', 'род', 'ед', 'м'): 'Я?[АЕОЯ]?ГО',
    ('м', 'дат', 'ед', 'м'): 'Ю?[ЕОУЮ]?МУ',
    ('м', 'вин', 'ед', 'м'): '[ИЪЬЫ]?И|ОИ',
    ('м', 'тв', 'ед', 'м'): 'И?ИМ[ЪЬ`]',
    ('м', 'мест', 'ед', 'м'): 'И?[ЕИО]М[ЪЬ`]',
    ('м', 'зв', 'ед', 'м'): '[ИЪЬЫ]?И|ОИ',

    ('м', 'им', 'дв', 'м'): '[АЯ][АЯ]',
    ('м', 'род', 'дв', 'м'): '[ЕОУЮ][УЮ]',
    ('м', 'дат', 'дв', 'м'): 'И?И?МА',
    ('м', 'вин', 'дв', 'м'): '[АЯ][АЯ]',
    ('м', 'тв', 'дв', 'м'): 'И?И?МА',
    ('м', 'мест', 'дв', 'м'): '[ЕОУЮ][УЮ]',
    ('м', 'зв', 'дв', 'м'): '[АЯ][АЯ]',

    ('м', 'им', 'мн', 'м'): 'ИИ',
    ('м', 'род', 'мн', 'м'): 'И?ИХ[ЪЬ`]',
    ('м', 'дат', 'мн', 'м'): 'И?ИМ[ЪЬ`]',
    ('м', 'вин', 'мн', 'м'): '[АЯ][АЯ]',
    ('м', 'тв', 'мн', 'м'): 'И?И?МИ',
    ('м', 'мест', 'мн', 'м'): 'И?ИХ[ЪЬ`]',
    ('м', 'зв', 'мн', 'м'): 'ИИ',

    # Мягкий подтип, женский род
    ('м', 'им', 'ед', 'ж'): '[АЯ][АЯ]',
    ('м', 'род', 'ед', 'ж'): '[АЕОЯ][АИЯ]',
    ('м', 'дат', 'ед', 'ж'): '[ЕИО]И',
    ('м', 'вин', 'ед', 'ж'): '[УЮ]Ю',
    ('м', 'тв', 'ед', 'ж'): '[ЕОУЮ][УЮ]',
    ('м', 'мест', 'ед', 'ж'): '[ЕИО]И',
    ('м', 'зв', 'ед', 'ж'): '[АЯ][АЯ]',

    ('м', 'им', 'дв', 'ж'): 'ИИ',
    ('м', 'род', 'дв', 'ж'): '[ЕОУЮ][УЮ]',
    ('м', 'дат', 'дв', 'ж'): 'И?И?МА',
    ('м', 'вин', 'дв', 'ж'): 'ИИ',
    ('м', 'тв', 'дв', 'ж'): 'И?И?МА',
    ('м', 'мест', 'дв', 'ж'): '[ЕОУЮ][УЮ]',
    ('м', 'зв', 'дв', 'ж'): 'ИИ',

    ('м', 'им', 'мн', 'ж'): '[АЯ][АЯ]',
    ('м', 'род', 'мн', 'ж'): 'И?ИХ[ЪЬ`]',
    ('м', 'дат', 'мн', 'ж'): 'И?ИМ[ЪЬ`]',
    ('м', 'вин', 'мн', 'ж'): '[АЯ][АЯ]',
    ('м', 'тв', 'мн', 'ж'): 'И?И?МИ',
    ('м', 'мест', 'мн', 'ж'): 'И?ИХ[ЪЬ`]',
    ('м', 'зв', 'мн', 'ж'): '[АЯ][АЯ]',

    # Мягкий подтип, средний род
    ('м', 'им', 'ед', 'ср'): '[ЕО]?Е',
    ('м', 'род', 'ед', 'ср'): 'Я?[АЕОЯ]?ГО',
    ('м', 'дат', 'ед', 'ср'): 'Ю?[ЕОУЮ]?МУ',
    ('м', 'вин', 'ед', 'ср'): '[ЕО]?Е',
    ('м', 'тв', 'ед', 'ср'): 'И?ИМ[ЪЬ`]',
    ('м', 'мест', 'ед', 'ср'): 'И?[ЕИО]М[ЪЬ`]',
    ('м', 'зв', 'ед', 'ср'): '[ЕО]?Е',

    ('м', 'им', 'дв', 'ср'): 'ИИ',
    ('м', 'род', 'дв', 'ср'): '[ЕОУЮ][УЮ]',
    ('м', 'дат', 'дв', 'ср'): 'И?И?МА',
    ('м', 'вин', 'дв', 'ср'): 'ИИ',
    ('м', 'тв', 'дв', 'ср'): 'И?И?МА',
    ('м', 'мест', 'дв', 'ср'): '[ЕОУЮ][УЮ]',
    ('м', 'зв', 'дв', 'ср'): 'ИИ',

    ('м', 'им', 'мн', 'ср'): '[АЯ][АЯ]',
    ('м', 'род', 'мн', 'ср'): 'И?ИХ[ЪЬ`]',
    ('м', 'дат', 'мн', 'ср'): 'И?ИМ[ЪЬ`]',
    ('м', 'вин', 'мн', 'ср'): '[АЯ][АЯ]',
    ('м', 'тв', 'мн', 'ср'): 'И?И?МИ',
    ('м', 'мест', 'мн', 'ср'): 'И?ИХ[ЪЬ`]',
    ('м', 'зв', 'мн', 'ср'): '[АЯ][АЯ]',
}

them_suff = {
    'en': '[ЪЬ]?Н$',
    'men': '([ЕЯ]|[ЪЬ]?)Н$',
    'ent': '[АЯ]Т$',
    'es': '(Е|[ЪЬ]?)С$',
    'er': '(Е|[ЪЬ]?)Р$',
    'uu': '[ЪЬ]?В$',
}

noun_spec = {
    'И([ИС]|ИСУС)[ЪЬ`]?$': ('*ИИСУС', 'Ъ'),
    'ПОЛ.*Д[ЕЬ]?Н': ('ПОЛДЕН', 'Ь'),
    'ПОЛ.*НОЧ': ('ПОЛНОЧ', 'Ь'),
    'ПОЛ.*НОЩ': ('ПОЛНОЩ', 'Ь'),
}

pron_pers = {
    ('1', 'им', 'ед'): ('АЗ[ЪЬ`]?$', 'АЗЪ'),
    ('1', 'род', 'ед'): ('М([ЕЪЬ]?Н)?[+ЕЯ]$', 'АЗЪ'),
    ('1', 'дат', 'ед'): ('М([ЕЪЬ]?Н[+Е]|И)$', 'АЗЪ'),
    ('1', 'вин', 'ед'): ('М([ЕЪЬ]?Н)?[+ЕЯ]$', 'АЗЪ'),
    ('1', 'тв', 'ед'): ('М[ЪЬ]?НОЮ$', 'АЗЪ'),
    ('1', 'мест', 'ед'): ('М[ЪЬ]?Н[+Е]$', 'АЗЪ'),

    ('2', 'им', 'ед'): ('ТЫ$', 'ТЫ'),
    ('2', 'род', 'ед'): ('Т([ЕО]Б)?[+ЕЯ]$', 'ТЫ'),
    ('2', 'дат', 'ед'): ('Т([ЕО]Б[+Е]|И)$', 'ТЫ'),
    ('2', 'вин', 'ед'): ('Т([ЕО]Б)?[+ЕЯ]$', 'ТЫ'),
    ('2', 'тв', 'ед'): ('ТОБОЮ$', 'ТЫ'),
    ('2', 'мест', 'ед'): ('Т[ЕО]Б[+Е]$', 'ТЫ'),

    ('1', 'им', 'дв'): ('В[+Е]$', 'В+'),
    ('1', 'род', 'дв'): ('НАЮ$', 'В+'),
    ('1', 'дат', 'дв'): ('НАМА$', 'В+'),
    ('1', 'вин', 'дв'): ('Н[АЫ]$', 'В+'),
    ('1', 'тв', 'дв'): ('НАМА$', 'В+'),
    ('1', 'мест', 'дв'): ('НАЮ$', 'В+'),

    ('2', 'им', 'дв'): ('ВА$', 'ВА'),
    ('2', 'род', 'дв'): ('ВАЮ$', 'ВА'),
    ('2', 'дат', 'дв'): ('ВАМА$', 'ВА'),
    ('2', 'вин', 'дв'): ('В[АЫ]$', 'ВА'),
    ('2', 'тв', 'дв'): ('ВАМА$', 'ВА'),
    ('2', 'мест', 'дв'): ('ВАЮ$', 'ВА'),

    ('1', 'им', 'мн'): ('МЫ$', 'МЫ'),
    ('1', 'род', 'мн'): ('НАС[ЪЬ`]?$', 'МЫ'),
    ('1', 'дат', 'мн'): ('Н(АМ[ЪЬ`]?|Ы)$', 'МЫ'),
    ('1', 'вин', 'мн'): ('Н(АС[ЪЬ`]?|Ы)$', 'МЫ'),
    ('1', 'тв', 'мн'): ('НАМИ$', 'МЫ'),
    ('1', 'мест', 'мн'): ('НАС[ЪЬ`]?$', 'МЫ'),

    ('2', 'им', 'мн'): ('ВЫ$', 'ВЫ'),
    ('2', 'род', 'мн'): ('ВАС[ЪЬ`]?$', 'ВЫ'),
    ('2', 'дат', 'мн'): ('В(АМ[ЪЬ`]?|Ы)$', 'ВЫ'),
    ('2', 'вин', 'мн'): ('В(АС[ЪЬ`]?|Ы)$', 'ВЫ'),
    ('2', 'тв', 'мн'): ('ВАМИ$', 'ВЫ'),
    ('2', 'мест', 'мн'): ('ВАС[ЪЬ`]?$', 'ВЫ'),
}

pron_refl = {
    'род': ('С([ЕО]Б)?[+ЕЯ]$', 'СЕБЕ'),
    'дат': ('С([ЕО]Б[+Е]|И)$', 'СЕБЕ'),
    'вин': ('С([ЕО]Б)?[+ЕЯ]$', 'СЕБЕ'),
    'тв': ('СОБОЮ$', 'СЕБЕ'),
    'мест': ('С[ЕО]Б[+Е]$', 'СЕБЕ'),
}

pron_interr = {
    ('тв', 'им'): ('К[ЪЬ]?ТО$', 'КТО'),
    ('тв', 'род'): ('КОГО$', 'КТО'),
    ('тв', 'дат'): ('КОМУ$', 'КТО'),
    ('тв', 'вин'): ('КОГО$', 'КТО'),
    ('тв', 'тв'): ('Ц[+Е]М[ЪЬ`]?$', 'КТО'),
    ('тв', 'мест'): ('КОМ[ЪЬ`]?$', 'КТО'),

    ('м', 'им'): ('Ч[ЪЬ]?ТО$', 'ЧТО'),
    ('м', 'род'): ('Ч[ЕЬ]?(СО)?(ГО)?$', 'ЧТО'),
    ('м', 'дат'): ('Ч[ЕЬ]?(СО)?МУ$', 'ЧТО'),
    ('м', 'вин'): ('Ч[ЪЬ]?ТО$', 'ЧТО'),
    ('м', 'тв'): ('ЧИМ[ЪЬ`]?$', 'ЧТО'),
    ('м', 'мест'): ('Ч[ЕЬ]?(СО)?М[ЪЬ`]?$', 'ЧТО'),
}

pron_spec = {
    '': 'И',
    'ВАШ': 'Ь',
    'ВЕС': 'Ь',
    'ЕЛИК': 'О',
    'М': 'ОИ',
    'НАШ': 'Ь',
    'ОН': 'Ъ',
    'ОНСИЦ': 'А',
    'САМ': 'Ъ',
    'СВ': 'ОИ',
    'СИЦ': 'Ь',
    'Т': 'ОИ',
    'ТВ': 'ОИ',
}

num_spec = {
    'ЕДИН.*НАДЕСЯТ': 'ЕДИННАДЕСЯТЕ',
    'Д[ЪЬ]?В.*НАДЕСЯТ': 'ДВАНАДЕСЯТЕ',
    'ТР.*НАДЕСЯТ': 'ТРИНАДЕСЯТЕ',
    'ЧЕТЫР.*НАДЕСЯТ': 'ЧЕТЫРЕНАДЕСЯТЕ',
    'ПЯТ.*НАДЕСЯТ': 'ПЯТЬНАДЕСЯТЕ',
    'ШЕСТ.*НАДЕСЯТ': 'ШЕСТЬНАДЕСЯТЕ',
    'СЕДМ.*НАДЕСЯТ': 'СЕДМЬНАДЕСЯТЕ',
    'ОСМ.*НАДЕСЯТ': 'ОСМЬНАДЕСЯТЕ',
    'ДЕВЯТ.*НАДЕСЯТ': 'ДЕВЯТЬНАДЕСЯТЕ',

    'Д[ЪЬ]?В.*ДЕСЯТ': 'ДВАДЕСЯТИ',
    'ТР.*ДЕСЯТ': 'ТРИДЕСЯТЕ',
    'ЧЕТЫР.*ДЕСЯТ': 'ЧЕТЫРЕДЕСЯТЕ',
    'ПЯТ.*ДЕСЯТ': 'ПЯТЬДЕСЯТЪ',
    'ШЕСТ.*ДЕСЯТ': 'ШЕСТЬДЕСЯТЪ',
    'СЕДМ.*ДЕСЯТ': 'СЕДМЬДЕСЯТЪ',
    'ОСМ.*ДЕСЯТ': 'ОСМЬДЕСЯТЪ',
    'ДЕВЯТ.*ДЕСЯТ': 'ДЕВЯТЬДЕСЯТЪ',

    'Д[ЪЬ]?В.*С[ЪО]?Т': 'ДВ+СТ+',
    'ТР.*С[ЪО]?Т': 'ТРИСТА',
    'ЧЕТЫР.*С[ЪО]?Т': 'ЧЕТЫРЕСТА',
    'ПЯТ.*С[ЪО]?Т': 'ПЯТЬСОТЪ',
    'ШЕСТ.*С[ЪО]?Т': 'ШЕСТЬСОТЪ',
    'СЕДМ.*С[ЪО]?Т': 'СЕДМЬСОТЪ',
    'ОСМ.*С[ЪО]?Т': 'ОСМЬСОТЪ',
    'ДЕВЯТ.*С[ЪО]?Т': 'ДЕВЯТЬСОТЪ',
}

ana_tenses = {
    'перф': 'AUX-PRF',
    'плюскв': 'AUX-PQP',
    'буд 1': 'AUX-FT1',
    'буд 2': 'AUX-FT2',
}

aor_simp_infl = {
    ('1', 'ед'): '[ЪЬ]',
    ('2', 'ед'): '[+Е]',
    ('3', 'ед'): '[+Е]',

    ('1', 'дв'): 'ОВ[+Е]',
    ('2', 'дв'): 'ЕТ[+АЕ]',
    ('3', 'дв'): 'ЕТ[+АЕ]',

    ('1', 'мн'): 'ОМ[ЪЬ`]',
    ('2', 'мн'): 'ЕТЕ',
    ('3', 'мн'): 'у',
}

aor_sigm_infl = {
    ('1', 'ед'): 'Х?[ЪЬ`]',
    ('2', 'ед'): '[+Е]',
    ('3', 'ед'): '[+Е]',

    ('1', 'дв'): 'Х?ОВ[+Е]',
    ('2', 'дв'): 'С?Т[+АЕ]',
    ('3', 'дв'): 'С?Т[+АЕ]',

    ('1', 'мн'): 'Х?ОМ[ЪЬ`]',
    ('2', 'мн'): 'С?ТЕ',
    ('3', 'мн'): 'Ш?[АЯ]',
}

part_el_infl = {
    ('м', 'ед'): 'Л?[ЪЬ`]',
    ('м', 'дв'): 'Л?А',
    ('м', 'мн'): 'Л?И',

    ('ж', 'ед'): 'Л?А',
    ('ж', 'дв'): 'Л?[+И]',
    ('ж', 'мн'): 'Л?[ЫИ]',

    ('ср', 'ед'): 'Л?О',
    ('ср', 'дв'): 'Л?[+И]',
    ('ср', 'мн'): 'Л?[АИ]',
}

part_el_spec = {
    '(.[ЪЬ]?)ШЕ$': 'ОИ',
    '(.*)ШЕ$': 'И',
}

part_spec = {
    '(.*)[ЕИ][МН]$': 'Я',
    '(.[ЪЬ]?)Ш[+Е]Д$': 'ОИ',
    '(.*)Ш[+Е]Д$': 'И',
}

cnj_1_sti = {
    'БЛЮД': 'БЛЮС',
    'БР[+Е]Д': 'БРЕС',
    'БР[+Е]Т': 'БР+С',
    'В[+Е]Д': 'ВЕС',
    'В[+Е]З': 'ВЕЗ',
    'В[ЕЬ]РЗ': 'ВЕРЗ',
    'ГР[+Е]Б': 'ГРЕС',
    'ГРЫЗ': 'ГРЫЗ',
    'КЛАД': 'КЛАС',
    'КЛЯН': 'КЛЯС',
    'КРАД': 'КРАС',
    'КР[+Е]Б': 'КРЕС',
    'Л[+Е]З': 'ЛЕЗ',
    'МЕТ': 'МЕС',
    'Н[+Е]С': 'НЕС',
    'ПА[ДС]': 'ПАС',
    'ПЛ[+Е]Т': 'ПЛЕС',
    'ПОЛЗ': 'ПОЛЗ',
    'Р[АО]СТ?': 'РАС',
    'С[+ЕИ]Д': 'С+С',
    'ТРЯС': 'ТРЯС',
    'ЦВ[+Е]Т': 'ЦВЕС',
    'ЧТ': 'ЧЕС',
}

cnj_1_tschi = (
    '[БВ]Л[+Е]К',
    '[БВ]ОЛОК',
    '[БВ]ЫК',
    'Б[+Е]Г',
    'Ж[ЕЬ]?Г',
    'Л[+Е]Г',
    'Л[+Е]К',
    'МОГ',
    'НЕБР[+Е]Г',
    'НИК',
    'П[+Е]К',
    'ПРЯГ',
    'Р[+Е]Г',
    'Р[+Е]К',
    'С[+Е]К',
    'С[+Е]К',
    'СТ[+Е]Р[+Е]Г',
    'СТРИГ',
    'Т[+Е]К',
    'ТОЛ[ОЪ]?К',
)

cnj_2_zh = (
    '[+Е]ЗД',
    'Б[+Е]Д',
    'БЛИЗ',
    'БОРОЗД',
    'БУД',
    'ВАД',
    'ВОД',
    'ВОЗ',
    'Г(РА|ОРО)Д',
    'ГАД',
    'ГВОЗД',
    'ГРОМОЗД',
    'КАЗ',
    'ЛАД',
    'М(ЛА|ОЛО)Д',
    'М(РА|ОРО)З',
    'НИЗ',
    'НУД',
    'ОБИД',
    'ПЛОД',
    'ПРУД',
    'Р[+Е]Д',
    'РАЗ',
    'РОД',
    'РЯД',
    'С[+Е]РД',
    'С[+ЕИ]Д',
    'САД',
    'СВОБОД',
    'СЛ[+Е]Д',
    'СНАБД',
    'СТУД',
    'СТЫД',
    'СУД',
    'ТВ[+Е]РД',
    'УД',
    'УЗ',
    'Х(ЛА|ОЛО)Д',
    'ХОД',
    'Ц[+Е]Д',
    'ЧУД',
    'ЩАД',
)

cnj_2_sch = (
    'Б[+Е]С',
    'В[+Е]С',
    'ВЫС',
    'Г(ЛА|ОЛО)С',
    'ГАС',
    'КВАС',
    'КОС',
    'КР[+Е]С',
    'КРАС',
    'КУС',
    'М[+Е]С',
    'НОС',
    'РОС',
    'ТРУС',
)

cnj_2_tsch = (
    '[БВ](РА|ОРО)Т',
    'Б(ЛА|ОЛО)Т',
    'БОГАТ',
    'В(РА|ОРО)Т',
    'В[+Е]РТ',
    'В[+Е]СТ',
    'ВСТР[+Е]Т',
    'ГЛОТ',
    'ГОСТ',
    'ГУСТ',
    'З(ЛА|ОЛО)Т',
    'ЗАБОТ',
    'К(ЛА|ОЛО)Т',
    'К(РА|ОРО)Т',
    'К(РА|ОРО)Т',
    'КАТ',
    'КОПТ',
    'КОСТ',
    'КР[+Е]СТ',
    'КРОТ',
    'КРУТ',
    'Л[ЕЬ]СТ',
    'ЛОПАТ',
    'ЛОХМАТ',
    'М(ЛА|ОЛО)Т',
    'М[+Е]СТ',
    'М[+Е]Т',
    'МОСТ',
    'МСТ',
    'МУТ',
    'ПЛАТ',
    'ПЛОТ',
    'ПОРТ',
    'ПОСТ',
    'ПР[+Е]Т',
    'ПРОСТ',
    'ПУСТ',
    'ПЯТ',
    'РАБОТ',
    '(?<!М)РАСТ',
    'С[+Е]Т',
    'СВ[+Е]Т',
    'СВЯТ',
    'СЛАСТ',
    'СМ[+Е]РТ',
    'СНАСТ',
    'СЫТ',
    'ТРАТ',
    'ТЯГОТ',
    'ХВАТ',
    'ХИТ',
    'ЦВ[+Е]Т',
    'Ч[+Е]РТ',
    'Ч[+Е]СТ',
    'ЧАСТ',
    'ЧИСТ',
    'ЩИТ',
    'ЩУТ',
)

prep_var = (
    'БЕЗО',
    'ВО',
    'ИЗО',
    'КО',
    'НАДО',
    'ОБО',
    'ОТО',
    'ПЕРЕДО',
    'ПОДО',
    'ПРЕДО',
    'ПРОТИВУ',
    'СО',
    'СУПРОТИВУ',
)

prep_rep = {
    '(.+)С[ЪЬ]$': '\\1ЗЪ',
    'Г[ЪЬ]$': 'КЪ',
    'З[ЪЬ]$': 'СЪ',
    'ОБ[ЪЬ]$': 'О',
}
