import glob
import tools
from handlers import *


class Token(object):

    def get_form(self):
        # Тут особая история с порядковыми прилагательными типа '$ЗПF#ГО'
        if self.pos == 'числ/п' and '#' in self.base:
            # 'Упрощённое упрощение'
            return self.base.upper().replace('(', '').replace(')', '')
        else:
            # Упрощение графики и нормализация
            return tools.normalise(self.base, self.pos)

    def get_lemma(self):
        if self.pos != 'мест':

            if self.pos == 'сущ':
                return noun.main(self)
            elif self.pos in ('прил', 'прил/ср', 'числ/п'):
                return adj.main(self)
            elif self.pos == 'прил/н':
                return self.form, ''
            else:
                return num_pron_imp.main(self)

        else:

            if self.decl == 'личн':
                return pron_pers_refl.main(self)
            else:
                return num_pron_imp.main(self)

    def __init__(self, file, string, pos, decl, pers, case, num, gen, nb):
        self.file = file
        self.string = tools.rus_full(string)
        self.pos = pos
        self.decl = tools.lat_light(decl)
        self.pers = pers
        self.case = case
        self.num = num
        self.gen = gen
        self.nb = tools.rus_light(nb)

        self.base = tools.remove_punctuation(self.string, self.nb)
        self.form = self.get_form()
        self.stem, self.fl = self.get_lemma()
        self.lemma = self.stem + self.fl

    def __repr__(self):
        return ('%s' + '\t%s' * 9) % (self.file, self.string, self.lemma,
                                      self.pos, self.decl, self.pers, self.case, self.num, self.gen, self.nb)


def main(tokens):
    # Все файлы с разметкой в папке со входными данными
    files = glob.glob('*.txt')

    for file in files:
        f = open(file, mode='r', encoding='utf-8')
        n = file.replace('.txt', '')

        for i, line in enumerate(f):
            # Условие на корректность входных данных
            if line.count('\t') == 6:
                # Непечатные символы где-нибудь да проскакивают - нужно избавляться
                l_items = line.rstrip('\n').split(sep='\t')
                l = [item.strip() for item in l_items]

                if l[1].startswith(('сущ', 'прил', 'числ')):
                    tokens.append(Token(n, l[0], l[1], l[2], '', l[3], l[4], l[5], l[6]))

                elif l[1] == 'мест':
                    if l[2] == 'личн':
                        if l[3] == 'возвр':
                            tokens.append(Token(n, l[0], l[1], l[2], l[3], l[4], '', '', ''))
                        else:
                            tokens.append(Token(n, l[0], l[1], l[2], l[3], l[4], l[5], '', ''))
                    else:
                        tokens.append(Token(n, l[0], l[1], l[2], '', l[3], l[4], l[5], l[6]))

            else:
                print('Warning: corrupt data in file %s, line %d.' % (file, i + 1))

        f.close()

    return tokens
