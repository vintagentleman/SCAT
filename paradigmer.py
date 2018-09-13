import os
import csv
import glob
import itertools
import xlsxwriter
from collections import defaultdict
from txt_to_xml import Token
from handlers import Nom, Pron


def token_gener():
    files = glob.glob('*.csv')

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
    root = os.getcwd()
    os.chdir(root + '\\grm')

    # --- Заполнение и сортировка базы данных --- #
    db = dict()

    for t in token_gener():
        if hasattr(t, 'lemma') and t.pos.startswith(('сущ', 'прил', 'числ', 'мест')):
            if t.lemma not in db:
                db[t.lemma] = defaultdict(int)

            gr = Pron(t) if t.pos == 'мест' and t.msd[0] == 'личн' else Nom(t)
            db[t.lemma][(gr.case, gr.num)] += 1

    os.chdir(root)
    # Сортировка по 1) числу заполненных позиций в парадигме, 2) абсолютной частоте, 3) алфавиту
    db_sort = sorted(db.items(), key=lambda x: (len(x[1]), sum(x[1].values()), x[0]), reverse=True)

    # --- Генерация таблицы --- #
    book = xlsxwriter.Workbook('paradigms.xlsx')
    total_format = book.add_format({'align': 'right'})
    num_format = book.add_format({'align': 'center'})

    for n, group in itertools.groupby(db_sort, lambda y: len(y[1])):
        # Вкладки именуются по числу заполненных парадигматических позиций
        sheet = book.add_worksheet(str(n))
        row = 1

        for lemma, data in group:
            sheet.write('A%d' % row, lemma)
            sheet.set_column('A:A', 20)

            sheet.add_table('B%d:E%d' % (row, row + 7), options={
                'data': [
                    [
                        case,
                        data.get((case, 'ед')),
                        data.get((case, 'дв')),
                        data.get((case, 'мн'))
                    ] for case in ('им', 'род', 'дат', 'вин', 'тв', 'мест', 'зв')
                ],
                'autofilter': False,
                'style': 'Table Style Medium 15',
                'first_column': True,
                'columns': [
                    {'header': str(sum(data.values())), 'header_format': total_format},
                    {'header': 'ед', 'header_format': num_format},
                    {'header': 'дв', 'header_format': num_format},
                    {'header': 'мн', 'header_format': num_format}
                ]
            })

            row += 9

    book.close()
