import os
import re
import csv
import glob
from collections import Counter
from nltk.util import ngrams
import handlers
from txt_to_xml import Token


def process(f):
    reader = csv.reader(f, delimiter='\t')

    for j, items in enumerate(reader):
        form = items[0].strip()

        # Делаем разбиение (по тому же принципу, что и XML)
        pc_l = br = pc_r = ''

        pc_l_mo = re.search('^[.,:;[\]]+', form)
        if pc_l_mo:
            form, pc_l = form[pc_l_mo.end():].strip(), form[:pc_l_mo.end()].strip()

        br_mo = re.search(r'[%&\\]$|Z (-?\d+)$', form)
        if br_mo:
            form, br = form[:br_mo.start()].strip(), form[br_mo.start():].strip()

        pc_r_mo = re.search('[.,:;[\]]+$', form)
        if pc_r_mo:
            form, pc_r = form[:pc_r_mo.start()].strip(), form[pc_r_mo.start():].strip()

        if pc_l:
            yield 'PC,_,_,_'

        if form:
            if not items[1]:
                yield 'ZZ,_,_,_'
            elif items[1].isnumeric():
                yield 'NM,_,_,_'
            else:
                t = Token(form, '%s_%d' % (file[:-4], j + 1), [items[j] for j in range(1, 7)])

                if t.pos != 'мест':
                    if t.pos in ('сущ', 'прил', 'прил/ср', 'числ', 'числ/п'):
                        gr = handlers.Nom(t)
                    elif t.pos in ('гл', 'гл/в'):
                        gr = handlers.Verb(t)
                    elif t.pos in ('прич', 'прич/в'):
                        gr = handlers.Part(t)
                    else:
                        gr = handlers.Gram(t)
                else:
                    if t.ana[1] == 'личн':
                        gr = handlers.Pron(t)
                    else:
                        gr = handlers.Nom(t)

                yield ','.join([getattr(gr, tag, '_') for tag in ('pos', 'case', 'num', 'pers')])

        if pc_r:
            yield 'PC,_,_,_'


if __name__ == '__main__':
    out = open('trigrams.csv', mode='w', encoding='utf-8', newline='')
    writer = csv.writer(out, delimiter='\t')
    os.chdir(os.getcwd() + '\\txt')
    files = glob.glob('*.csv')
    trig_dict = Counter()

    for file in files:
        fo = open(file, mode='r', encoding='utf-8')
        tokens = list(process(fo))

        for trig in ngrams(tokens, 3):
            trig_dict[trig] += 1

        fo.close()

    freq = rank = counter = 0
    for i, pair in enumerate(trig_dict.most_common()):
        # Если частота изменилась, пересчитываем её встречаемость (в первый раз - всегда)
        if pair[1] != freq:
            counter = list(trig_dict.values()).count(pair[1])

        # Если частота - гапакс, то ранг считается просто: порядковый номер + поправка
        if counter == 1:
            rank = i + 1
        # Если нет *и* частота новая (т. е. первая в диапазоне равных), то считаем
        # по-сложному. В противном случае не пересчитываем - ранг остаётся прежний
        elif pair[1] != freq:
            rank = i + 1 + (counter - 1) / 2
            if rank.is_integer():
                rank = int(rank)

        writer.writerow([rank] + list(pair[0]) + [pair[1]])
        freq = pair[1]

    out.close()
