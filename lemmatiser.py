import os
import csv
import glob
from txt_to_xml import Token


def token_gener(pattern='*.csv'):
    files = glob.glob(pattern)

    for fn in files:
        with open(fn, mode='r', encoding='utf-8') as fo:
            reader = csv.reader(fo, delimiter='\t')

            for i, row in enumerate(reader):
                yield Token(
                    row[0].strip(),
                    '%s.%d' % (fn[:-4], i + 1),
                    [row[j].strip() for j in range(1, 7)]
                )


if __name__ == '__main__':
    out = open('output.csv', mode='w', encoding='utf-8', newline='')
    err = open('errors.csv', mode='w', encoding='utf-8', newline='')
    out_writer = csv.writer(out, delimiter='\t')
    err_writer = csv.writer(err, delimiter='\t')

    os.chdir(os.getcwd() + '\\grm')

    for t in token_gener():
        if hasattr(t, 'lemma'):
            row = [t.xml_id, t.src, t.lemma, t.pos] + t.msd
            out_writer.writerow(row)

            if t.lemma == 'NONE':
                err_writer.writerow(row)

    err.close()
    out.close()
