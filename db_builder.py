import os
import glob
import shelve
import lib
from txt_to_xml import Token


def build_infl_db():
    db = shelve.open('infl')

    for par in (lib.nom_infl, lib.pron_infl):
        for gr in par:
            infl = par[gr]

            # Часть речи для типизации использовать *нельзя*
            data = db.setdefault(infl, [])
            data.append((gr[0], gr[3]))
            db[infl] = data

    db.close()


def build_stem_db():
    os.chdir(os.getcwd() + '\\data')
    files = glob.glob('*.txt')
    db = shelve.open('stem')

    for file in files:
        f = open(file, mode='r', encoding='utf-8')

        for i, line in enumerate(f):
            items = [item.strip() for item in line.rstrip('\n').split(sep='\t')]

            if len(items) == 7:
                t = Token(items[0], file[:-4], [items[i] for i in range(1, 7)])
            else:
                print('Warning: corrupt data in file %s, line %d.' % (file, i + 1))
                continue

            if hasattr(t, 'stem') and t.ana[0].startswith(('сущ', 'прил', 'числ')) and t.stem[1] != 'NONE':
                for var in t.stem:
                    data = db.setdefault(var, {})
                    data[(t.ana[1], t.ana[4])] = t.lemma
                    db[var] = data

        f.close()
    db.close()


'''
def build_spec_db():
    db = shelve.open('spec')

    for par in (lib.pron_pers, lib.pron_refl, lib.pron_interr):
        for key in par:
            db[key[0]] = par[key]

    for par in (lib.noun_spec, lib.num_spec):
        for key in par:
            db[key] = par[key]

    db.close()
'''
