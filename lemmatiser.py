import os
import csv
import glob
from txt_to_xml import Token


def process():
    # Все файлы с разметкой в папке со входными данными
    files = glob.glob('*.csv')

    for file in files:
        f = open(file, mode='r', encoding='utf-8')

        for i, line in enumerate(f):
            # Непечатные символы где-нибудь да проскакивают - надо избавляться
            items = [item.strip() for item in line.rstrip('\n').split(sep='\t')]

            if len(items) == 7:
                yield Token(items[0], '%s.%d' % (file[:-4], i + 1), [items[i] for i in range(1, 7)])
            else:
                print('Warning: corrupt data in file %s, line %d.' % (file, i + 1))
                continue

        f.close()


if __name__ == '__main__':
    out = open('output.csv', mode='w', encoding='utf-8', newline='')
    err = open('errors.csv', mode='w', encoding='utf-8', newline='')

    try:
        os.chdir(os.getcwd() + '\\grm')
    except FileNotFoundError:
        print('Error: source data directory missing.')
    else:
        print('Please wait. Python is processing your data...')
        out_writer = csv.writer(out, delimiter='\t')
        err_writer = csv.writer(err, delimiter='\t')

        for t in process():
            if hasattr(t, 'lemma'):
                row = [t.xml_id, t.src, t.lemma, t.pos] + t.msd
                out_writer.writerow(row)

                if t.lemma == 'NONE':
                    err_writer.writerow(row)

    finally:
        err.close()
        out.close()
