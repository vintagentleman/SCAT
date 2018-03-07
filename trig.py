import os
import re
import csv
import glob
from collections import Counter
from nltk.util import ngrams
import handlers
from txt_to_xml import Token


def process(items):
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
            t = Token(form, file[:-4], [items[j] for j in range(1, 7)])

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
    otpt = open('trigrams.csv', mode='w', encoding='utf-8', newline='')
    writer = csv.writer(otpt, delimiter='\t')
    os.chdir(os.getcwd() + '\\txt')
    files = glob.glob('*.csv')

    trig_dict = Counter()
    freq = rank = counter = 0

    # Сборка словаря триграмм
    for file in files:
        inpt = open(file, mode='r', encoding='utf-8')
        reader = csv.reader(inpt, delimiter='\t')
        tokens = list()

        for line in reader:
            tokens.extend(list(process(line)))

        for trig in ngrams(tokens, 3):
            trig_dict[trig] += 1

        inpt.close()

    for i, pair in enumerate(trig_dict.most_common()):
        # Если частота изменилась, пересчитываем её встречаемость (в первый раз - всегда)
        if pair[1] != freq:
            counter = list(trig_dict.values()).count(pair[1])

        # Если частота - гапакс, то ранг считается просто: порядковый номер + поправка
        if counter == 1:
            rank = float(i + 1)
        # Если нет *и* частота новая (т. е. первая в диапазоне равных), то считаем
        # по-сложному. В противном случае не пересчитываем - ранг остаётся прежний
        elif pair[1] != freq:
            rank = i + 1 + (counter - 1) / 2

        writer.writerow(list(pair[0]) + [pair[1], rank])
        freq = pair[1]

    otpt.close()
