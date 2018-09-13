import re
import lib
from tools import replace_chars


__all__ = ['adj', 'noun', 'num_pron_imp', 'pron_pers_refl', 'part', 'verb']


class Gram(object):

    def __init__(self, t):
        self.form = t.reg.replace('(', '').replace(')', '')
        self.pos = t.pos


class Nom(Gram):

    def __init__(self, t):
        super().__init__(t)

        # Маркер собственности
        self.prop = bool('*' in self.form)
        if self.prop:
            self.form = self.form[1:]

        # НЕ- и -ЖЕ/-ЖДО
        if self.pos == 'мест':
            self.zhe = re.search('ЖЕ$|Ж[ЪЬ]?Д[ЕО]$', self.form)
            self.neg = re.match('Н[+ЕИ](?=[КЧ])', self.form)

            if self.zhe:
                self.form = self.form[:-len(self.zhe.group())]
            if self.neg:
                self.form = self.form[len(self.neg.group()):]

        else:
            self.zhe = None
            self.neg = None

        # Гласный-пустышка
        if self.form[-1] not in lib.vows:
            self.form += '`'

        # Типы склонения: старый для основы, новый для флексии; здесь кириллица в латиницу (для гласных)
        if '/' in t.msd[0] and t.msd[0] != 'р/скл':
            self.d_old, self.d_new = replace_chars(t.msd[0], 'аеоу', 'aeoy').split('/')
        else:
            self.d_old = self.d_new = replace_chars(t.msd[0], 'аеоу', 'aeoy')

        self.case = t.msd[1].split('/')[-1]
        self.pt = bool(t.msd[2] == 'pt')
        self.num = t.msd[2].split('/')[-1] if not self.pt else 'мн'
        self.gen = t.msd[3].split('/')[-1] if t.msd[3] != '0' else 'м'

        # Латиница в кириллицу
        self.nb = replace_chars(t.msd[4], 'aeopcyx', 'аеорсух')


class Pron(Gram):

    def __init__(self, t):
        super().__init__(t)

        if self.form[-1] not in lib.vows:
            self.form += '`'

        self.pers = t.msd[1]
        self.case = t.msd[2].split('/')[-1]
        self.num = t.msd[3].split('/')[-1] if self.pers != 'возвр' else 'ед'


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

        self.mood = replace_chars(t.msd[0], 'aeopcyx', 'аеорсух')

        if self.mood == 'изъяв':
            self.tense = t.msd[1]

            if t.msd[2].isnumeric():
                self.pers = t.msd[2]
                self.gen = '_'
            else:
                self.pers = '_'
                self.gen = t.msd[2]

            self.num = t.msd[3].split('/')[-1]

            if t.msd[4].isnumeric():
                self.role = '_'
                self.cls = t.msd[4]
            else:
                self.role = t.msd[4]
                self.cls = '_'

        elif self.mood == 'сосл':
            if t.msd[1].isnumeric():
                self.pers = t.msd[1]
                self.gen = '_'
            else:
                self.pers = '_'
                self.gen = t.msd[1]

            self.num = t.msd[2].split('/')[-1]
            self.role = t.msd[3]

        elif self.mood == 'повел':
            self.pers = t.msd[1]
            self.num = t.msd[2]
            self.cls = t.msd[3]


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

        if '/' in t.msd[0]:
            self.d_old, self.d_new = replace_chars(t.msd[0], 'аеоу', 'aeoy').split('/')
        else:
            self.d_old = self.d_new = replace_chars(t.msd[0], 'аеоу', 'aeoy')

        self.tense = t.msd[1]
        self.case = t.msd[2].split('/')[-1]
        self.num = t.msd[3].split('/')[-1]
        self.gen = t.msd[4].split('/')[-1] if t.msd[4] != '0' else 'м'
