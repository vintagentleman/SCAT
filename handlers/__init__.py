import re
import lib


__all__ = ['adj', 'noun', 'num_pron_imp', 'pron_pers_refl']


class Gram(object):

    def __init__(self, t):
        self.form = t.reg.replace('(', '').replace(')', '')
        self.pos = t.ana[0]


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

        # Типы склонения: старый для основы, новый для флексии
        if '/' in t.ana[1] and t.ana[1] != 'р/скл':
            self.d_old, self.d_new = t.ana[1].split('/')
        else:
            self.d_old = self.d_new = t.ana[1]

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

        self.nb = t.ana[5]


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
