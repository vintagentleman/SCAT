import os
import re
import lib
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

        s = self.src
        s = s.replace('*', '').replace('~', '').replace('[', '').replace(']', '')
        s = s.replace('&', '<lb/>').replace('\\', '<cb/>')
        s = re.sub(r'Z -?\d+ ?', '<pb/>', s)
        s = re.sub(r'\((.+?)\)', overline, s)
        s = replace_chars(s, 'IRVWU+ЭFSGDLQЯ$', 'їѧѵѡѹѣѣѳѕѫꙋѯѱꙗ҂')

        if '#' in s:
            s = s.replace('#', '')

            if count_chars(s) > 1:
                s = s[:count_chars(s, 1) + 1] + '҃' + s[count_chars(s, 1) + 1:]
            else:
                s = s[:count_chars(s, 0) + 1] + '҃' + s[count_chars(s, 0) + 1:]

        s = s.lower()
        s = s.replace('ѡⷮ', 'ѿ')
        s = s.replace('=', 'ѿ')

        if s.find(' ') > -1:
            s, self.corr = s.split(' ', maxsplit=1)

            # Убрал условие (len(self.corr) > 5): проблемы с висячими разрывами, опять же
            if self.corr.endswith(('<lb/>', '<cb/>', '<pb/>')):
                self.corr = self.corr[:-5]
            # strip() - аналогичная история
            self.corr = self.corr.strip()[1:-1]

        # Но здесь убирать не надо
        if s.endswith(('<lb/>', '<cb/>', '<pb/>')) and len(s) > 5:
            s = s[:-5]

        return s

    def get_reg(self):
        s = self.src

        # Учёт исправлений (обрабатывается исправленный вариант)
        if '<' in s:
            s = s[s.index('<') + 1:s.index('>')]

        # Знаки препинания
        for sign in '.,:;[]':
            s = s.replace(sign, '')

        # Разрывы строк, колонок и страниц
        s = s.replace('&', '').replace('\\', '')
        s = re.sub(r'Z -?\d+ ?', '', s)
        s = s.strip()

        # Упрощение графики и нормализация
        if hasattr(self, 'ana'):
            # Цифирь не трогаем
            if not self.ana[0].isnumeric():
                # Цифирные прилагательные типа '$ЗПF#ГО' иногда размечаются (непоследовательно)
                if self.ana[0] == 'числ/п' and '#' in s:
                    return s.upper().replace('(', '').replace(')', '')
                else:
                    return tools.normalise(s, self.ana[0], self.ana[5])

            else:
                return self.src
        else:
            return tools.normalise(s, '', '')

    def get_lemma(self):

        if self.ana[0] != 'мест':
            if self.ana[0] == 'сущ':
                return noun.main(self)
            elif self.ana[0] in ('прил', 'прил/ср', 'числ/п'):
                return adj.main(self)
            elif self.ana[0] == 'числ':
                return num_pron_imp.main(self)
            elif self.ana[0] in ('гл', 'гл/в', 'прич', 'прич/в'):
                pass
            # 'прил/н', 'инф', 'инф/в', 'суп', 'нар', 'пред', 'посл', 'союз', 'част', 'межд'
            else:
                lemma = self.reg.replace('(', '').replace(')', '')

                if lemma.endswith(lib.cons):
                    if lemma[-1] in lib.cons_hush:
                        lemma += 'Ь'
                    else:
                        lemma += 'Ъ'

                if self.ana[0] == 'пред':
                    if lemma in lib.prep_var:
                        lemma = lemma[:-1] + 'Ъ'

                    for regex in lib.prep_rep:
                        if re.match(regex, lemma):
                            lemma = re.sub(regex, lib.prep_rep[regex], lemma)

                return lemma, ''

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

        if ana:
            self.ana = ana
            # Латиница в кириллицу
            self.ana[0] = replace_chars(ana[0], 'aeopcyx', 'аеорсух')
            self.ana[5] = replace_chars(ana[5], 'aeopcyx', 'аеорсух')
            # Кириллица в латиницу
            self.ana[1] = replace_chars(ana[1], 'аеорсух', 'aeopcyx')

        self.orig = self.get_orig()
        self.reg = self.get_reg()

        if hasattr(self, 'ana'):
            # if self.ana[0] in ('прил/н', 'инф', 'инф/в', 'суп', 'нар', 'пред', 'посл', 'союз', 'част', 'межд'):
            if not self.ana[0].startswith(('гл', 'прич')):
                self.stem, self.fl = self.get_lemma()
                self.lemma = self.stem + self.fl

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

    os.makedirs(root + '\\xml', exist_ok=True)
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
        punct_index = sorted([items[0].find(c) for c in '.,:;?!' if items[0].find(c) != -1])
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

                if metadata.front:
                    otpt.write('''            </l>
          </div4>
        </div3>
      </div2>
      <div2 type="page" n="%s">
        <div3 type="%s">
          <div4 type="col" n="%d">
            <l n="%d">\n''' % (metadata.page, front_text(metadata.front), metadata.col, metadata.line))

                else:
                    otpt.write('''            </l>
          </div4>
        </div3>
        <div3 type="%s">
          <div4 type="col" n="%d">
            <l n="%d">\n''' % (front_text(metadata.front), metadata.col, metadata.line))

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
        process_file('DGlush.txt')
    except FileNotFoundError:
        print('Error: source file missing.')
