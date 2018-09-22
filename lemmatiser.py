import os
import csv
from obj import token_gener


if __name__ == '__main__':
    out = open('output.csv', mode='w', encoding='utf-8', newline='')
    err = open('errors.csv', mode='w', encoding='utf-8', newline='')
    out_writer = csv.writer(out, delimiter='\t')
    err_writer = csv.writer(err, delimiter='\t')

    os.chdir(os.getcwd() + '\\grm')

    for t in token_gener():
        if hasattr(t, 'lemma'):
            row = [t.xmlid, t.src, t.lemma, t.pos] + t.msd
            out_writer.writerow(row)

            if t.lemma == 'NONE':
                err_writer.writerow(row)

    err.close()
    out.close()
