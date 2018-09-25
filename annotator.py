import os
import sys
import csv
import xlsxwriter
from collections import defaultdict
import obj


def main(fn, offset=0, limit=sys.maxsize):
    os.chdir(root + '\\txt')

    fo = open(fn + '.csv', mode='r', encoding='utf-8')
    reader = csv.reader(fo, delimiter='\t')
    book = xlsxwriter.Workbook(fn + '.xlsx')
    # ambi = book.add_format({'bg_color': 'yellow'})
    ok = book.add_format({'bg_color': 'lime'})

    sheet = book.add_worksheet()
    sheet.set_column('A:A', 40)

    for i, row in enumerate(reader):
        if i < offset:
            continue

        if len(row) == 1:
            sheet.write(i, 0, row[0])
            form = obj.Word(obj.Token(row[0]).word, fn, i).reg
            if form and form in db:
                # Если разбор один, то помечаем его как единственный
                if len(db[form]) == 1:
                    sheet.write(i, 0, row[0], ok)
                    sheet.write_row(i, 1, db[form][0])
                # Если нет, то выделяем неоднозначные позиции
                else:
                    msd = zip(*db[form])

                    for j, col in enumerate(msd, start=1):
                        # Если конфликтов нет, то просто записываем
                        if col.count(col[0]) == len(col):
                            sheet.write(i, j, col[0])
                        # Конфликты выделяем и отображаем все опции
                        # else:
                        #     sheet.write_blank(i, j, None, ambi)
                        #     sheet.data_validation(i, j, i, j, {
                        #         'validate': 'list',
                        #         'source': list(dict.fromkeys(col)),
                        #         'show_error': False
                        #     })

        # Если колонок больше одной, то это цифирь
        else:
            sheet.write(i, 0, row[0], ok)
            sheet.write(i, 1, row[1])

        if i == limit:
            break

    fo.close()
    book.close()


if __name__ == '__main__':
    root = os.getcwd()
    os.chdir(root + '\\grm')
    db = defaultdict(list)

    for t in obj.word_gener():
        if hasattr(t, 'msd'):
            parse = [t.pos] + t.msd
            if parse not in db[t.reg]:
                db[t.reg].append(parse)

    main('KrnKml')
