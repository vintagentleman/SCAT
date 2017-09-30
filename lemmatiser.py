import os
import glob
from txt_to_xml import Token


if __name__ == '__main__':
    out = open('output.txt', mode='w', encoding='utf-8')
    err = open('errors.txt', mode='w', encoding='utf-8')

    try:
        os.chdir(os.getcwd() + '\\data')
        print('Please wait. Python is processing your data...')

        # Все файлы с разметкой в папке со входными данными
        files = glob.glob('*.txt')

        for file in files:

            f = open(file, mode='r', encoding='utf-8')
            name = file.replace('.txt', '')

            for i, line in enumerate(f):
                # Непечатные символы где-нибудь да проскакивают - надо избавляться
                items = [item.strip() for item in line.rstrip('\n').split(sep='\t')]

                if len(items) == 7:
                    t = Token(items[0], name, [items[i] for i in range(1, 7)])
                else:
                    print('Warning: corrupt data in file %s, line %d.' % (file, i + 1))
                    continue

                # Вот и всё колдовство
                if hasattr(t, 'stem'):
                    out.write('\t'.join([t.token_id, t.src, t.lemma] + t.ana) + '\n')

                    if t.stem == 'NONE':
                        err.write('\t'.join([t.token_id, t.src, t.lemma] + t.ana) + '\n')

            f.close()

    except FileNotFoundError:
        print('Error: source data directory missing.')

    finally:
        err.close()
        out.close()
