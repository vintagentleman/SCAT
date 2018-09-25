import os
import csv
import xlsxwriter
from collections import defaultdict
import obj


def main(fn, st_total, limit, offset=0):
    os.chdir(root + '\\txt')

    fo = open(fn + '.csv', mode='r', encoding='utf-8', newline='')
    reader = csv.reader(fo, delimiter='\t')
    all(next(reader) for _ in range(offset))

    book = xlsxwriter.Workbook(fn + '.xlsx')
    # ambi = book.add_format({'bg_color': 'yellow'})
    ok = book.add_format({'bg_color': 'lime'})
    st_count = 0

    while st_count < st_total:
        sheet = book.add_worksheet()
        sheet.set_column('A:A', 40)
        st_limit = limit

        for i, row in enumerate(reader):
            if len(row) == 1:
                sheet.write(i, 0, row[0])
                form = obj.Word(obj.Token(row[0]).word, fn, i).reg
                if form and form in db:
                    # Если разбор один, то помечаем его и не учитываем при подсчёте
                    if len(db[form]) == 1:
                        sheet.write(i, 0, row[0], ok)
                        sheet.write_row(i, 1, db[form][0])
                        st_limit += 1
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

            if i == st_limit:
                st_count += 1
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

    main('KrnKml', 10, 250)
