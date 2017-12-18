import re
import lib
from tools import replace_chars

__all__ = ['adj', 'noun', 'num_pron_imp', 'pron_pers_refl', 'part', 'verb']


class Gram(object):

    def __init__(self, t):
        self.form = t.reg.replace('(', '').replace(')', '')
        # Латиница в кириллицу
        self.pos = t.pos


class Nom(Gram):

    def __init__(self, t):
        super().__init__(t)

        # Маркер собственности
        self.prop = bool('*' in self.form)
        if self.prop:
            self.form = self.form[1:]

        # НЕ- и -ЖЕ
        if self.pos == 'мест':
            self.zhe = bool(self.form.endswith('ЖЕ'))
            self.neg = re.match('Н[+ЕИ](?=[КЧ])', self.form)

            if self.zhe:
                self.form = self.form[:-2]
            if self.neg:
                self.form = self.form[2:]

        else:
            self.zhe = False
            self.neg = False

        # Гласный-пустышка
        if self.form[-1] not in lib.vows:
            self.form += '`'

        # Типы склонения: старый для основы, новый для флексии; здесь кириллица в латиницу (для гласных)
        if '/' in t.ana[1] and t.ana[1] != 'р/скл':
            self.d_old, self.d_new = replace_chars(t.ana[1], 'аеоу', 'aeoy').split('/')
        else:
            self.d_old = self.d_new = replace_chars(t.ana[1], 'аеоу', 'aeoy')

        self.case = t.ana[2].split('/')[-1]

        # Маркер pluralia tantum
        self.pt = bool(t.ana[3] == 'pt')
        if self.pt:
            self.num = 'мн'
        else:
            self.num = t.ana[3].split('/')[-1]

        # Учёт особого смешения (en/i и других)
        if t.ana[4] == '0':
            self.gen = 'м'
        else:
            self.gen = t.ana[4].split('/')[-1]

        # Латиница в кириллицу
        self.nb = replace_chars(t.ana[5], 'aeopcyx', 'аеорсух')


class Pron(Gram):

    def __init__(self, t):
        super().__init__(t)

        if self.form[-1] not in lib.vows:
            self.form += '`'

        self.pers = t.ana[2]
        self.case = t.ana[3].split('/')[-1]

        if self.pers != 'возвр':
            self.num = t.ana[4].split('/')[-1]
        else:
            self.num = ''


class Verb(Gram):

    def __init__(self, t):
        super().__init__(t)

        # Маркер возвратности
        self.refl = bool(self.pos.endswith('/в'))
        if self.refl:
            self.form = self.form[:-2]
            self.pos = self.pos[:-2]

        if self.form[-1] not in lib.vows:
            self.form += '`'

        self.mood = replace_chars(t.ana[1], 'aeopcyx', 'аеорсух')

        if self.mood == 'изъяв':
            self.tense = t.ana[2]

            if t.ana[3].isnumeric():
                self.pers = t.ana[3]
                self.gen = ''
            else:
                self.pers = ''
                self.gen = t.ana[3]

            self.num = t.ana[4]

            if t.ana[5].isnumeric():
                self.role = ''
                self.cls = t.ana[5]
            else:
                self.role = t.ana[5]
                self.cls = ''

        elif self.mood == 'сосл':
            if t.ana[2].isnumeric():
                self.pers = t.ana[2]
                self.gen = ''
            else:
                self.pers = ''
                self.gen = t.ana[2]

            self.num = t.ana[3]
            self.role = t.ana[4]

        elif self.mood == 'повел':
            self.pers = t.ana[2]
            self.num = t.ana[3]
            self.cls = t.ana[4]


class Part(Gram):

    def __init__(self, t):
        super().__init__(t)

        self.refl = bool(self.pos.endswith('/в'))
        if self.refl:
            self.form = self.form[:-2]
            self.pos = self.pos[:-2]

        if re.match('НЕ(?!ДО)', self.form):
            self.form = self.form[2:]

        if self.form[-1] not in lib.vows:
            self.form += '`'

        if '/' in t.ana[1]:
            self.d_old, self.d_new = replace_chars(t.ana[1], 'аеоу', 'aeoy').split('/')
        else:
            self.d_old = self.d_new = replace_chars(t.ana[1], 'аеоу', 'aeoy')

        self.tense = t.ana[2]
        self.case = t.ana[3].split('/')[-1]
        self.num = t.ana[4].split('/')[-1]
        self.gen = t.ana[5].split('/')[-1]
