import os
import re
import csv
import glob
from collections import defaultdict
import handlers
from txt_to_xml import Token


def process(f):
    reader = csv.reader(f, delimiter='\t')

    for i, items in enumerate(reader):
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
            if ':' in pc_r or ';' in pc_r:
                yield 'TR,_,_,_'
            else:
                yield 'PC,_,_,_'

        if form:
            if not items[1]:
                yield 'ZZ,_,_,_'
            elif items[1].isnumeric():
                yield 'NM,_,_,_'
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

                yield ','.join([getattr(gr, tag, '_') for tag in ('pos', 'case', 'num', 'pers')])

        if pc_r:
            if ':' in pc_r or ';' in pc_r:
                yield 'TR,_,_,_'
            else:
                yield 'PC,_,_,_'


if __name__ == '__main__':
    out = open('trigrams.csv', mode='w', encoding='utf-8', newline='')
    writer = csv.writer(out, delimiter='\t')
    os.chdir(os.getcwd() + '\\txt')
    files = glob.glob('*.csv')
    trig_dict = defaultdict(int)
    triple = list()

    for file in files:
        fo = open(file, mode='r', encoding='utf-8')
        triple.clear()

        for tagset in process(fo):
            if tagset == 'союз,_,_,_' and triple and triple[-1] == 'PC,_,_,_':
                triple.clear()

            triple.append(tagset)

            if len(triple) > 3:
                del triple[0]
            elif len(triple) < 3:
                continue

            trig_dict[';'.join(triple)] += 1

            if tagset == 'TR,_,_,_':
                triple.clear()

        fo.close()

    for pair in sorted(trig_dict.items(), key=lambda x: -x[1]):
        writer.writerow(pair[0].split(';') + [pair[1]])

    out.close()
