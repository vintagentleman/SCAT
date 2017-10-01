import os
import re
import tools
from handlers import *


def count_chars(string, num=-1):

    def skip_chars(s, start):

        if s[start] == '<':
            start += len(re.search(r'(<.+?>)', s[start:]).group(1))
        elif s[start] == '&':
            start += len(re.search(r'(&.+?;)', s[start:]).group(1)) - 1

        if s[start] in '<&':
            start = skip_chars(s, start)

        return start

    if num > -1:
        result = 0
        result = skip_chars(string, result)

        for i in range(num):
            result += 1
            result = skip_chars(string, result)

        return result

    string = re.sub(r'<.+?>', '', string)
    string = re.sub(r'&.+?;', 'S', string)

    return len(string)


def replace_chars(string, fr, to):
    if len(fr) != len(to):
        raise RuntimeError

    result = list(string)

    for i in range(len(result)):
        if result[i] in fr:
            result[i] = to[fr.index(result[i])]

    return ''.join(result)


class Token(object):

    def get_reg(self):
        # strip() добавил я: пробелы перед висячими разрывами создают проблемы
        self.reg = self.src
        self.reg = self.reg.replace('&', '').replace('\\', '')
        self.reg = re.sub(r'Z -?\d+ ?', '', self.reg)
        self.reg = replace_chars(self.reg, 'SIWDGUFRLQ', ('З', 'И', 'О', 'У', 'У', 'У', 'Ф', 'Я', 'КС', 'ПС'))
        self.reg = replace_chars(self.reg, 'siwdgufrlq', ('з', 'и', 'о', 'у', 'у', 'у', 'ф', 'я', 'кс', 'пс'))
        self.reg = self.reg.replace('<', '&lt;').replace('>', '&gt;').strip()

        return self.reg

    def get_orig(self):

        def overline(match):
            result = replace_chars(match.group(1).upper(), 'БВГДЖЗКЛМНОПРСТХЦЧШЩFАЕD+ЭЮRGЯИIЪЬWЫУU', (
                'ⷠ', 'ⷡ', 'ⷢ', 'ⷣ', 'ⷤ', 'ⷥ', 'ⷦ', 'ⷧ', 'ⷨ', 'ⷩ',
                'ⷪ', 'ⷫ', 'ⷬ', 'ⷭ', 'ⷮ', 'ⷯ', 'ⷰ', 'ⷱ', 'ⷲ', 'ⷳ',
                'ⷴ', 'ⷶ', 'ⷷ', 'ⷹ', 'ⷺ', 'ⷺ', 'ⷻ', 'ⷽ', 'ⷾ', 'ⷼ',
                '&i8-overline;', '&i10-overline;', '꙽', '&yer-overline;',
                '&omega-overline;', '&yeri-overline;', '&u-overline;', '&ou-overline;'
            ))
            if match.group(1).islower():
                result = '҇' + result

            return result

        self.orig = self.src
        self.orig = self.orig.replace('*', '').replace('~', '').replace('[', '').replace(']', '')
        self.orig = self.orig.replace('&', '<lb/>').replace('\\', '<cb/>')
        self.orig = re.sub(r'Z -?\d+ ?', '<pb/>', self.orig)
        self.orig = re.sub(r'\((.+?)\)', overline, self.orig)
        self.orig = replace_chars(self.orig, 'IRVWU+ЭFSGDLQЯ$', 'їѧѵѡѹѣѣѳѕѫꙋѯѱꙗ҂')

        if '#' in self.orig:
            self.orig = self.orig.replace('#', '')

            if count_chars(self.orig) > 1:
                self.orig = self.orig[:count_chars(self.orig, 1) + 1] + '҃' + self.orig[count_chars(self.orig, 1) + 1:]
            else:
                self.orig = self.orig[:count_chars(self.orig, 0) + 1] + '҃' + self.orig[count_chars(self.orig, 0) + 1:]

        self.orig = self.orig.lower()
        self.orig = self.orig.replace('ѡⷮ', 'ѿ')
        self.orig = self.orig.replace('=', 'ѿ')

        if self.orig.find(' ') > -1:
            self.orig, self.corr = self.orig.split(' ', maxsplit=1)

            # Убрал условие (len(self.corr) > 5): проблемы с висячими разрывами, опять же
            if self.corr.endswith(('<lb/>', '<cb/>', '<pb/>')):
                self.corr = self.corr[:-5]
            # strip() - аналогичная история
            self.corr = self.corr.strip()[1:-1]

        # Но здесь убирать не надо
        if self.orig.endswith(('<lb/>', '<cb/>', '<pb/>')) and len(self.orig) > 5:
            self.orig = self.orig[:-5]

        return self.orig

    def get_form(self):

        def remove_punctuation(s, nb):
            # Учёт исправлений (обработка производится над исправленным вариантом)
            if '<' in s:
                s = s[s.index('<') + 1:s.index('>')]

            # 'Безумные' (неэтимологические) еры и ери на концах строки, можем удалять их без разметки
            # Не трогаем, если 1) они оканчивают словоформу либо 2) входят в состав префиков типа ВЪ- и СЪ-
            if not ('+ъ' in nb or '+ь' in nb):
                for yer in ('Ъ&', 'ЪZ', 'Ь&', 'ЬZ'):
                    if yer in s and not (s.endswith(yer) or s[1:].startswith(yer)):
                        s = s.replace(yer, '')

            # Знаки препинания
            for sign in '&Z.,:;[]- ':
                s = s.replace(sign, '')

            # Номера страниц
            for i in range(10):
                s = s.replace(str(i), '')

            return s

        self.form = remove_punctuation(self.src, self.ana[5])

        # Тут особая история с порядковыми прилагательными типа '$ЗПF#ГО'
        if self.ana[0] == 'числ/п' and '#' in self.form:
            # 'Упрощённое упрощение'
            return self.form.upper().replace('(', '').replace(')', '')
        else:
            # Упрощение графики и нормализация
            return tools.normalise(self.form, self.ana[0])

    def get_lemma(self):
        if self.ana[0] != 'мест':

            if self.ana[0] == 'сущ':
                return noun.main(self)
            elif self.ana[0] in ('прил', 'прил/ср', 'числ/п'):
                return adj.main(self)
            elif self.ana[0] == 'прил/н':
                return self.form, ''
            else:
                return num_pron_imp.main(self)

        else:

            if self.ana[1] == 'личн':
                return pron_pers_refl.main(self)
            else:
                return num_pron_imp.main(self)

    def __init__(self, src, token_id, ana=None):
        self.src = replace_chars(src, 'ABEKMHOPCTXaeopcyx', 'АВЕКМНОРСТХаеорсух')
        self.token_id = token_id

        # Тег смены содержательной части
        self.part_b = r'%' in src
        if self.part_b:
            self.src = self.src.replace(r'%', '')

        # Разрыв страницы
        z = re.search(r'Z (-?)(\d+) ?', src)
        if z:
            self.page_b = True
            self.next_page_is_front = bool(z.group(1) != '-')
            self.next_page_num = z.group(2)
        else:
            self.page_b = False

        # Разрыв колонки либо строки
        self.col_b = '\\' in src
        self.line_b = '&' in src

        self.is_name = '*' in self.src
        self.is_add = '[' in self.src
        self.sic = '~' in self.src
        self.corr = None

        self.reg = self.get_reg()
        self.orig = self.get_orig()

        if ana:
            self.ana = ana
            self.ana[1] = replace_chars(ana[1], 'аео', 'aeo')
            self.ana[5] = replace_chars(ana[5], 'aeo', 'аео')
            self.form = self.get_form()

            if self.ana[0].startswith(('сущ', 'прил', 'числ', 'мест')):
                self.stem, self.fl = self.get_lemma()
                self.lemma = self.stem + self.fl

            if self.ana[0].isnumeric():
                self.reg = self.src

    def __repr__(self):
        result = '<w xml:id="%s"' % self.token_id
        # Надо привести грамматику к формату TEI. Но как быть с индексами (плюс-минус)?
        if hasattr(self, 'ana') and not self.ana[0].isnumeric():
            result += ' ana="%s"' % ';'.join(item for item in self.ana if item)
        if hasattr(self, 'lemma'):
            result += ' lemma="%s"' % self.lemma
        result += '>\n  <orig>'

        # Наполняем
        if self.corr:
            result += '<choice><sic>%s</sic><corr>%s</corr></choice>' % (self.orig, self.corr)
        else:
            if self.sic:
                result += '<sic>%s</sic>' % self.orig
            else:
                result += self.orig

        result += '''</orig>
  <reg>%s</reg>
  <src>%s</src>
</w>''' % (self.reg, self.src.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

        # Обрамляем
        if hasattr(self, 'ana') and self.ana[0].isnumeric():
            result = '<num value="%s">\n%s\n</num>' % (self.ana[0], result)
        else:
            if self.is_name:
                result = '<name>\n%s\n</name>' % result
            if self.is_add:
                result = '<add place="margin">\n%s\n</add>' % result

        return result


class Punct(Token):

    def __repr__(self):
        return '<pc xml:id="%s">%s</pc>' % (self.token_id, self.reg)


class DefaultMetadata:

    prefix = 'DGlush'
    part = 1
    page = '22'
    front = True
    col = 1
    line = 1


def process_file(file, metadata=DefaultMetadata):

    def front_text(front_bool):
        if front_bool:
            return 'front'
        else:
            return 'back'

    root = os.getcwd()
    # Исключение может возбуждаться и для папок, и для файла
    os.chdir(root + '\\txt')
    inpt = open(file, mode='r', encoding='utf-8')

    # Засим всё в порядке, начинаем обработку
    print('Please wait. Python is processing your data...')
    os.chdir(root + '\\xml')
    otpt = open(file[:-3] + 'xml', mode='w', encoding='utf-8')
    xmlid = 1

    # Инициализация структуры XML
    otpt.write('''  <text>
    <div1 type="part" n="%d">
      <div2 type="page" n="%s">
        <div3 type="%s">
          <div4 type="col" n="%d">
            <l n="%d">\n''' % (metadata.part, metadata.page, front_text(metadata.front), metadata.col, metadata.line))

    for i, line in enumerate(inpt):
        items = [item.strip() for item in line.split(sep='\t')]

        # Если при словоформе есть висячие знаки препинания, сохраняем их отдельно и убираем
        punct_index = [items[0].find(c) for c in '.,:;?!' if items[0].find(c) != -1]
        if punct_index:
            punct = items[0][punct_index[0]:]
            items[0] = items[0][:punct_index[0]]
        else:
            punct = ''

        # Теперь в начальной подстроке либо ничего, либо нормальный токен
        tokens = []
        if items[0]:
            if len(items) == 7:
                # Словоформа плюс разметка
                token = Token(items[0], '%s.%d' % (metadata.prefix, xmlid), [items[i] for i in range(1, 7)])
            elif len(items) == 1:
                # Только словоформа
                token = Token(items[0], '%s.%d' % (metadata.prefix, xmlid))
            else:
                print('Warning: corrupt data in line %d.' % (i + 1))
                continue
            # Проверяем, не голый ли это символ разрыва (им идентификатор не присваиваем)
            if token.reg:
                xmlid += 1
            tokens += [token]

        if punct:
            tokens += [Punct(punct, '%s.%d' % (metadata.prefix, xmlid))]
            xmlid += 1

        for token in tokens:
            # Голые разрывы не индексируем в принципе
            if token.reg:
                otpt.write('%s\n' % str(token))

            if token.part_b:
                if not token.page_b:
                    raise RuntimeError('Error: part break w/o page break in line %d.' % (i + 1))

                metadata.part += 1
                metadata.col = 1
                metadata.line = 1
                metadata.front = token.next_page_is_front
                metadata.page = token.next_page_num
                otpt.write('''            </l>
          </div4>
        </div3>
      </div2>
    </div1>
    <div1 type="part" n="%d">
      <div2 type="page" n="%s">
        <div3 type="%s">
          <div4 type="col" n="%d">
            <l n="%d">\n''' % (metadata.part, metadata.page, front_text(metadata.front), metadata.col, metadata.line))

            elif token.page_b:
                metadata.col = 1
                metadata.line = 1
                metadata.front = token.next_page_is_front
                metadata.page = token.next_page_num
                otpt.write('''            </l>
          </div4>
        </div3>
      </div2>
      <div2 type="page" n="%s">
        <div3 type="%s">
          <div4 type="col" n="%d">
            <l n="%d">\n''' % (metadata.page, front_text(metadata.front), metadata.col, metadata.line))

            elif token.col_b:
                metadata.col += 1
                metadata.line = 1
                otpt.write('''            </l>
          </div4>
          <div4 type="col" n="%d">
            <l n="%d">\n''' % (metadata.col, metadata.line))

            elif token.line_b:
                metadata.line += 1
                otpt.write('''            </l>
            <l n="%d">\n''' % metadata.line)

    otpt.write('''            </l>
          </div4>
        </div3>
      </div2>
    </div1>
  </text>''')

    inpt.close()
    otpt.close()


if __name__ == '__main__':
    try:
        process_file('DG.txt')
    except FileNotFoundError:
        print('Error: source file missing.')
