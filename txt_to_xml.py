import os
import re
import glob
import csv
import json
import lib
import tools
from handlers import *


class Token(object):

    def get_orig(self):

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

        s = self.src

        # Учёт исправлений (обрабатывается исходный вариант)
        if '<' in s:
            s = s[:s.index('<') - 1]

        # Маркеры собственности и ошибочности (но вставки оставляем)
        s = s.replace('*', '').replace('~', '')

        # Разрыв части внутри слова - невероятно, но подстраховаться не грех
        if r'%' in s:
            s = s.replace(r'%', '<milestone/>')

        # Разрывов строк внутри одной словоформы может быть несколько
        while '&' in s:
            data['line'] += 1
            s = s.replace('&', '<lb n="%d"/>' % data['line'], 1)

        # Разрывы колонок/страниц - по тому же принципу, что и между словоформами
        if '\\' in s or self.pb:
            if '\\' in s:
                data['col'] = 'b'
            else:
                data['page'] = self.pb.group(1)
                if 'col' in data:
                    data['col'] = 'a'

            data['line'] = 1
            s = re.sub(r'\\|Z -?\d+ ?', '<pb n="%s"/>' % (data['page'] + data.get('col', '')), s)

        # Символы Юникода
        s = re.sub(r'\((.+?)\)', overline, s)
        s = tools.replace_chars(s, 'IRVWU+FSGDLQЯ$', 'їѧѵѡѹѣѳѕѫꙋѯѱꙗ҂')

        if '#' in s:
            s = s.replace('#', '')

            if tools.count_chars(s) > 1:
                s = s[:tools.count_chars(s, 1) + 1] + '҃' + s[tools.count_chars(s, 1) + 1:]
            else:
                s = s[:tools.count_chars(s, 0) + 1] + '҃' + s[tools.count_chars(s, 0) + 1:]

        s = s.replace('ѡⷮ', 'ѿ')
        return s.lower()

    def get_reg(self):
        s = self.src

        # Учёт исправлений (обрабатывается исправленный вариант)
        if '<' in s:
            s = s[s.index('<') + 1:s.index('>')]

        # Знаки препинания (NB: в режиме генерации XML этот блок не нужен)
        for sign in '.,:;?!':
            s = s.replace(sign, '')

        # Разрывы
        s = s.replace(r'%', '').replace('&', '').replace('\\', '')
        s = re.sub(r'Z -?\d+ ?', '', s)

        # Вставки и непечатные символы
        s = s.replace('[', '').replace(']', '').strip()

        # Упрощение графики и нормализация
        if hasattr(self, 'ana'):
            # Цифирь заменяем арабскими цифрами
            if not self.ana[0].isnumeric():
                # Цифирные прилагательные типа '$ЗПF#ГО' иногда размечаются (непоследовательно)
                if self.ana[0] == 'числ/п' and '#' in s:
                    return s.upper().replace('(', '').replace(')', '')
                else:
                    return tools.normalise(s, self.ana[0], self.ana[5])

            else:
                return self.ana[0]
        else:
            return tools.normalise(s, '', '')

    def get_gram(self):

        if self.pos != 'мест':
            if self.pos == 'сущ':
                return noun.main(self)
            elif self.pos in ('прил', 'прил/ср', 'числ/п'):
                return adj.main(self)
            elif self.pos == 'числ':
                return num_pron_imp.main(self)
            elif self.pos in ('гл', 'гл/в'):
                return verb.main(self)
            elif self.pos in ('прич', 'прич/в'):
                return part.main(self)
            elif self.pos in ('прил/н', 'инф', 'инф/в', 'суп', 'нар', 'пред', 'посл', 'союз', 'част', 'межд'):
                lemma = self.reg.replace('(', '').replace(')', '')

                if lemma.endswith(lib.cons):
                    if lemma[-1] in lib.cons_hush:
                        lemma += 'Ь'
                    else:
                        lemma += 'Ъ'

                if self.pos == 'пред':
                    if lemma in lib.prep_var:
                        lemma = lemma[:-1] + 'Ъ'

                    for regex in lib.prep_rep:
                        if re.match(regex, lemma):
                            lemma = re.sub(regex, lib.prep_rep[regex], lemma)

                elif self.pos == 'суп':
                    lemma = lemma[:-1] + 'И'

                return ('', lemma), ''

            else:
                return ('', 'NONE'), ''

        else:
            if self.ana[1] == 'личн':
                return pron_pers_refl.main(self)
            else:
                return num_pron_imp.main(self)

    def __init__(self, src, token_id, ana=None):
        self.src = tools.replace_chars(src, 'ABEKMHOPCTXЭaeopcyx', 'АВЕКМНОРСТХ+аеорсух')
        self.token_id = token_id
        self.pb = re.search(r'Z (-?\d+) ?', self.src)

        if ana:
            self.ana = ana
            self.pos = tools.replace_chars(self.ana[0], 'aeopcyx', 'аеорсух')
            if not any(self.pos.endswith(spec) for spec in ('/в', '/н', '/п', '/ср')):
                self.pos = self.pos.split('/')[-1]

        self.orig = self.get_orig()
        self.reg = self.get_reg()

        if hasattr(self, 'ana') and self.ana[0] and not self.ana[0].isnumeric():
            # stem - кортеж из основы до и после модификаций
            self.stem, self.fl = self.get_gram()
            if self.stem[1] or self.fl:
                self.lemma = self.stem[1] + self.fl

    def __repr__(self):
        ana = lemma = ''
        src = self.src.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        if hasattr(self, 'ana'):
            if not self.ana[0].isnumeric():
                ana = ' ana="%s"' % ';'.join(item for item in self.ana if item)
                if hasattr(self, 'lemma'):
                    lemma = ' lemma="%s"' % self.lemma
            else:
                return '<num><w xml:id="%s" reg="%s" src="%s">%s</w></num>' % (self.token_id, self.reg, src, self.orig)

        return '<w xml:id="%s"%s%s reg="%s" src="%s">%s</w>' % (self.token_id, ana, lemma, self.reg, src, self.orig)


def process(fn):

    def split_block(mo, s):
        if mo:
            return s[:mo.start()].strip(), s[mo.start():].strip()
        else:
            return s, ''

    inpt = open(fn + '.csv', mode='r', encoding='utf-8')
    reader = csv.reader(inpt, delimiter='\t')
    os.chdir(root + '\\xml')
    otpt = open(fn + '.xml', mode='w', encoding='utf-8')
    xmlid = 1

    otpt.write('''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader type="text">
    <fileDesc>

      <titleStmt>
        <title>%s</title>''' % data['title'])

    for pair in data['resp']:
        otpt.write('''
        <respStmt>
          <resp>%s</resp>
          <name>%s</name>
        </respStmt>''' % tuple(pair))

    otpt.write('''
      </titleStmt>

      <publicationStmt>
        <publisher>%s</publisher>
        <pubPlace>%s</pubPlace>
        <date>%s</date>
        <idno type="ISBN">%s</idno>
      </publicationStmt>\n''' % tuple(data['pub']))

    otpt.write('''
      <sourceDesc>
        <bibl>%s</bibl>
      </sourceDesc>

    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <pb n="%s"/>\n''' % (data['bibl'], (data['page'] + data.get('col', ''))))

    for i, row in enumerate(reader):
        form = row[0].strip()

        # Расчленяем строку-словоформу на три блока (обязательно наличие хотя бы одного): 1) саму словоформу,
        # 2) висячие (конечные) знаки препинания и 3) висячие разрывы. Порядок именно такой: ср. 'МIРЪ. Z 27'
        pc_mo = re.search('(?<![%s#])[%s]+' % (2 * ('.,:;?!',)), form)
        form, pc = split_block(pc_mo, form)

        if pc:
            br_mo = re.search(r'[%&\\]$|Z (-?\d+)$', pc)
            pc, br = split_block(br_mo, pc)
        else:
            br_mo = re.search(r'[%&\\]$|Z (-?\d+)$', form)
            form, br = split_block(br_mo, form)

        tokens = []

        # Обработка словоформы (если она есть)
        if form:
            if len(row) == 7:
                # Словоформа плюс разметка
                token = Token(form, '%s_%d' % (fn, xmlid), [row[i].strip() for i in range(1, 7)])
            elif len(row) == 1:
                # Только словоформа
                token = Token(form, '%s_%d' % (fn, xmlid))
            else:
                print('Warning: corrupt data in line %d.' % (i + 1))
                continue

            tokens += [token]
            xmlid += 1

        # Далее пунктуация и разрывы
        if pc:
            tokens += ['<pc xml:id="%s_%s">%s</pc>' % (fn, xmlid, pc)]
            xmlid += 1

        if br:
            if r'%' in br:
                tokens += ['<milestone/>']

            elif '&' in br:
                data['line'] += 1
                tokens += ['<lb n="%d"/>' % data['line']]

            # Если в рукописи есть колонки, то разрыв колонки обозначает переход ко второй,
            # разрыв страницы - обновление нумерации и переход к первой. Третьей не дано
            elif '\\' in br or re.search(r'Z -?\d+ ?', br):
                if '\\' in br:
                    data['col'] = 'b'
                else:
                    data['page'] = br_mo.group(1)
                    if 'col' in data:
                        data['col'] = 'a'

                data['line'] = 1
                tokens += ['<pb n="%s"/>' % (data['page'] + data.get('col', ''))]

        for token in tokens:
            otpt.write('      %s\n' % str(token))

    otpt.write('    </body>\n  </text>\n</TEI>\n')
    otpt.close()
    os.chdir(root + '\\txt')
    inpt.close()


if __name__ == '__main__':
    metadata = json.load(open('metadata.json', mode='r', encoding='utf-8'))

    root = os.getcwd()
    os.makedirs(root + '\\xml', exist_ok=True)
    os.chdir(root + '\\txt')
    files = glob.glob('*.csv')

    for file in files:
        name = file[:-4]
        data = metadata[name]
        process(name)
