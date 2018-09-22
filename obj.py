import re
import csv
import glob
import json
import lib
import tools
from handlers import *


def token_gener(pattern='*.csv'):
    names = glob.glob(pattern)

    for name in names:
        with open(name, mode='r', encoding='utf-8') as fo:
            reader = csv.reader(fo, delimiter='\t')

            for i, row in enumerate(reader):
                yield Token(row[0].strip(), name[:-4], i + 1, [row[j].strip() for j in range(1, 7)])


class Token:
    metadata = json.load(open('metadata.json', mode='r', encoding='utf-8'))

    @staticmethod
    def ascii_to_unicode(s):

        def overline(match):
            result = tools.replace_chars(
                match.group(1).upper(),
                'БВГДЖЗКЛМНОПРСТХЦЧШЩFАЕD+ЮRGЯИIЪЬWЫУU',
                (
                    'ⷠ', 'ⷡ', 'ⷢ', 'ⷣ', 'ⷤ', 'ⷥ', 'ⷦ', 'ⷧ', 'ⷨ',
                    'ⷩ', 'ⷪ', 'ⷫ', 'ⷬ', 'ⷭ', 'ⷮ', 'ⷯ', 'ⷰ', 'ⷱ',
                    'ⷲ', 'ⷳ', 'ⷴ', 'ⷶ', 'ⷷ', 'ⷹ', 'ⷺ', 'ⷻ', 'ⷽ',
                    'ⷾ', 'ⷼ', 'ꙶ', 'ꙵ', 'ꙸ', 'ꙺ', 'ꙻ', 'ꙹ', 'ꙷ',
                    'ⷪꙷ',  # Здесь два символа
                )
            )
            if match.group(1).islower():
                result = '҇' + result

            return result

        s = re.sub(r'\((.+?)\)', overline, s)
        s = tools.replace_chars(s, 'IRVWU+FSGDLQЯ$', 'їѧѵѡѹѣѳѕѫꙋѯѱꙗ҂')

        if '#' in s:
            s = s.replace('#', '')

            if tools.count_chars(s) > 1:
                s = s[:tools.count_chars(s, 1) + 1] + '҃' + s[tools.count_chars(s, 1) + 1:]
            else:
                s = s[:tools.count_chars(s, 0) + 1] + '҃' + s[tools.count_chars(s, 0) + 1:]

        return s.replace('ѡⷮ', 'ѿ').lower()

    def get_orig(self, s):
        # Маркеры собственности и ошибочности (но вставки оставляем)
        s = s.replace('*', '').replace('~', '')

        # Разрывов строк внутри одной словоформы может быть несколько
        while '&' in s:
            self.data['line'] += 1
            s = s.replace('&', '<lb n="%d"/>' % self.data['line'], 1)

        # Разрывы колонок/страниц - по тому же принципу, что и между словоформами
        if '\\' in s or self.pb:
            if '\\' in s:
                self.data['col'] = 'b'
            else:
                self.data['page'] = self.pb.group(1)
                if 'col' in self.data:
                    self.data['col'] = 'a'

            self.data['line'] = 1
            s = re.sub(r'\\|Z -?\d+ ?', '<pb n="%s"/><lb n="1"/>' % (self.data['page'] + self.data.get('col', '')), s)

        return self.ascii_to_unicode(s)

    def get_corr(self, s):
        s = s.replace('*', '').replace('~', '').replace('[', '').replace(']', '')
        s = s.replace(r'%', '').replace('&', '').replace('\\', '')
        s = re.sub(r'Z -?\d+ ?', '', s)

        return self.ascii_to_unicode(s)

    def get_reg(self, s):
        # Знаки препинания и разрывы
        for sign in '.,:;[]':
            s = s.replace(sign, '')

        s = s.replace(r'%', '').replace('&', '').replace('\\', '')
        s = re.sub(r'Z -?\d+ ?', '', s)
        s = s.strip()

        # Упрощение графики и нормализация
        if hasattr(self, 'pos'):
            # Цифирь заменяется арабскими цифрами
            if not self.pos.isnumeric():
                # Цифирные прилагательные типа '$ЗПF#ГО' иногда размечаются (непоследовательно)
                if self.pos == 'числ/п' and '#' in s:
                    return s.upper().replace('(', '').replace(')', '')
                else:
                    return tools.normalise(s, self.pos)
            else:
                return self.pos
        else:
            return tools.normalise(s)

    def get_gram(self):
        pos = self.pos

        if '/' in pos and not re.search(r'/([внп]|ср)$', pos):
            pos = pos.split('/')[-1]

        if pos != 'мест':
            if pos in ('сущ', 'прил', 'прил/ср', 'числ', 'числ/п', 'прич', 'прич/в'):
                self.msd[0] = tools.replace_chars(self.msd[0], 'аеоу', 'aeoy')  # Тип склонения; К → Л
            elif pos.startswith('гл'):
                self.msd[0] = tools.replace_chars(self.msd[0], 'aeopcyx', 'аеорсух')  # Наклонение; Л → К

        if pos != 'мест':
            if pos == 'сущ':
                return noun.main(Nom(self))
            elif pos in ('прил', 'прил/ср', 'числ/п'):
                return adj.main(Nom(self))
            elif pos == 'числ':
                return num_pron_imp.main(Nom(self))
            elif pos in ('гл', 'гл/в'):
                return verb.main(Verb(self))
            elif pos in ('прич', 'прич/в'):
                return part.main(Part(self))
            elif pos in ('прил/н', 'инф', 'инф/в', 'суп', 'нар', 'пред', 'посл', 'союз', 'част', 'межд'):
                lemma = self.reg.replace('(', '').replace(')', '')

                if lemma.endswith(lib.cons):
                    if lemma[-1] in lib.cons_hush:
                        lemma += 'Ь'
                    else:
                        lemma += 'Ъ'

                if pos == 'пред':
                    if lemma in lib.prep_var:
                        lemma = lemma[:-1] + 'Ъ'

                    for regex in lib.prep_rep:
                        if re.match(regex, lemma):
                            lemma = re.sub(regex, lib.prep_rep[regex], lemma)

                elif pos == 'суп':
                    lemma = lemma[:-1] + 'И'

                return ('', lemma), ''

            else:
                return ('', 'NONE'), ''

        else:
            if self.msd[0] == 'личн':
                return pron_pers_refl.main(Pron(self))
            else:
                return num_pron_imp.main(Nom(self))

    def __init__(self, src, fn, i, ana=None):
        self.src = tools.replace_chars(src, 'ABEKMHOPCTXЭaeopcyx', 'АВЕКМНОРСТХ+аеорсух')
        self.xmlid = '%s.%d' % (fn, i)
        self.data = Token.metadata.get(fn)
        self.pb = re.search(r'Z (-?\d+) ?', self.src)

        if ana is not None:
            # Латиница в кириллицу
            self.pos = tools.replace_chars(ana[0], 'aeopcyx', 'аеорсух')
            self.msd = ana[1:]

        if self.data is not None:
            if '<' in self.src:
                self.orig = self.get_orig(self.src[:self.src.index('<') - 1])
                self.corr = self.get_corr(self.src[self.src.index('<') + 1:self.src.index('>')])
            else:
                self.orig = self.get_orig(self.src)
                self.corr = None

        if '<' in self.src:
            self.reg = self.get_reg(self.src[self.src.index('<') + 1:self.src.index('>')])
        else:
            self.reg = self.get_reg(self.src)

        if hasattr(self, 'pos') and self.pos and not self.pos.isnumeric():
            # stem - кортеж из исходной основы и модифицированной
            self.stem, self.fl = self.get_gram()
            if self.stem[1] or self.fl:
                self.lemma = self.stem[1] + self.fl

    def __repr__(self):
        s = '<w xml:id="%s"' % self.xmlid

        if hasattr(self, 'pos') and not self.pos.isnumeric():
            s += ' pos="%s"' % self.pos

            if self.msd[0]:
                s += ' msd="%s"' % ';'.join(item for item in self.msd if item)
            if hasattr(self, 'lemma'):
                s += ' lemma="%s"' % self.lemma.lower()

        s += ' reg="%s" src="%s">%s</w>' % (self.reg.lower(), self.src.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), self.orig)

        if '*' in self.src:
            s = '<name>' + s + '</name>'
        elif hasattr(self, 'pos') and self.pos.isnumeric():
            s = '<num>' + s + '</num>'

        if self.corr is not None:
            s += '<note type="corr">%s</note>' % self.corr

        return s


class Gram:

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

        # Типы склонения: старый для основы, новый для флексии
        if '/' in t.msd[0] and t.msd[0] != 'р/скл':
            self.d_old, self.d_new = t.msd[0].split('/')
        else:
            self.d_old = self.d_new = t.msd[0]

        self.case = t.msd[1].split('/')[-1]
        self.pt = bool(t.msd[2] == 'pt')
        if self.pt:
            self.num = 'мн'
        else:
            self.num = t.msd[2].split('/')[-1] if t.msd[2] != '0' else 'ед'
        self.gen = t.msd[3].split('/')[-1] if t.msd[3] != '0' else 'м'

        self.nb = t.msd[4]


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

        self.mood = t.msd[0]

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
            self.d_old, self.d_new = t.msd[0].split('/')
        else:
            self.d_old = self.d_new = t.msd[0]

        self.tense = t.msd[1]
        self.case = t.msd[2].split('/')[-1]
        self.num = t.msd[3].split('/')[-1]
        self.gen = t.msd[4].split('/')[-1] if t.msd[4] != '0' else 'м'
