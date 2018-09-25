import os
import itertools
import xlsxwriter
from collections import defaultdict
import obj


if __name__ == '__main__':
    root = os.getcwd()
    os.chdir(root + '\\grm')

    # --- Заполнение и сортировка базы данных --- #
    db = dict()

    for t in obj.word_gener():
        if hasattr(t, 'lemma') and t.pos.startswith(('сущ', 'прил', 'числ', 'мест')):
            if t.lemma not in db:
                db[t.lemma] = defaultdict(int)

            gr = obj.Pron(t) if t.pos == 'мест' and t.msd[0] == 'личн' else obj.Nom(t)
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
        sheet.set_column('A:A', 20)
        row = 1

        for lemma, data in group:
            sheet.write('A%d' % row, lemma)

            sheet.add_table('B%d:E%d' % (row, row + 7), options={
                'data': [
                    list(
                        itertools.chain([case], [data.get((case, num)) for num in ('ед', 'дв', 'мн')])
                    ) for case in ('им', 'род', 'дат', 'вин', 'тв', 'мест', 'зв')
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
