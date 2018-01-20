import os
import re
import csv
import glob
from collections import defaultdict
import handlers
from txt_to_xml import Token


def process(f):

    def split_block(mo, s):
        if mo:
            return s[:mo.start()].strip(), s[mo.start():].strip()

        return s, ''

    def setdef(obj, name):
        try:
            return getattr(obj, name)
        except AttributeError:
            return '_'

    for i, line in enumerate(f):
        items = [item.strip() for item in line.split(sep='\t')]
        form = items[0]

        # Делаем разбиение (по тому же принципу, что и для XML)
        br_mo = re.search(r'[%&\\]$|Z (-?\d+)$', form)
        form, br = split_block(br_mo, form)
        pc_mo = re.search('[.,:;?!]+$', form)
        form, pc = split_block(pc_mo, form)

        if form:
            if not items[1]:
                yield 'ZZ,_,_,_,_'
            elif items[1].isnumeric():
                yield 'NM,_,_,_,_'
            else:
                t = Token(form, '%s_%d' % (file[:-4], i + 1), [items[j] for j in range(1, 7)])

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

                # Тегсет: 1) часть речи, 2) падеж, 3) число, 4) род, 5) лицо
                yield ','.join([setdef(gr, tag) for tag in ('pos', 'case', 'num', 'gen', 'pers')])

        if pc:
            yield 'PC,_,_,_,_'
        # if br:
        #     yield 'BR,_,_,_,_'


if __name__ == '__main__':
    out = open('trigrams.csv', mode='w', encoding='utf-8', newline='')
    writer = csv.writer(out, delimiter='\t')
    os.chdir(os.getcwd() + '\\txt')
    files = glob.glob('*.csv')
    trig_dict = defaultdict(int)

    for file in files:
        fo = open(file, mode='r', encoding='utf-8')
        triple = list()

        for tagset in process(fo):
            triple.append(tagset)

            if len(triple) < 3:
                continue
            elif len(triple) > 3:
                triple = triple[1:]

            trig_dict[';'.join(triple)] += 1

        fo.close()

    for pair in sorted(trig_dict.items(), key=lambda x: -x[1]):
        writer.writerow(pair[0].split(';') + [pair[1]])

    out.close()
