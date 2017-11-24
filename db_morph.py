import re
import shelve
from txt_to_xml import Token


class Analyser(object):

    def __init__(self, stem_db='stem', infl_db='infl'):
        self.stem_db = shelve.open(stem_db)
        self.infl_db = shelve.open(infl_db)

    def __del__(self):
        self.stem_db.close()
        self.infl_db.close()

    def lemmatise(self, s):
        result = set()

        # Максимальную длину флексии покамест условно примем равной пяти
        # Вычислял бы эксплицитно, не составляй базу регулярные выражения
        # Проходим до 0, а не -1, поскольку нулевой флексии не бывает
        for i in range(5, 0, -1):
            stem = s[:-i]
            infl = s[-i:]

            # Условие 1: основа непустая и есть в базе основ
            if stem and stem in self.stem_db:
                for regex in self.infl_db:
                    # Условие 2: флексия есть в базе основ
                    if re.match('(%s)$' % regex, infl):
                        common = set(self.stem_db[stem]) & set(self.infl_db[regex])
                        # Условие 3: есть общие типы
                        for cat in common:
                            result.add(self.stem_db[stem][cat])

        return result


def process(file):
    inpt = open(file, mode='r', encoding='utf-8')
    print('Please wait. Python is processing your data...')

    morph = Analyser()
    otpt = open('%s_lem.txt' % file[:-4], mode='w', encoding='utf-8')

    for i, line in enumerate(inpt):
        # Пунктуацию не трогаем
        if not re.match(r'(Z (-?)(\d+))|[&.,:\\;?!%]', line):
            # Размеченную цифирь не трогаем
            if line.count('\t') == 0:
                t = Token(line[:-1], file[:-4])
                lem = morph.lemmatise(t.reg)

                if lem:
                    otpt.write('%s\t%s\n' % (t.src, str(lem)))

    inpt.close()
    otpt.close()


if __name__ == '__main__':
    try:
        process('GrPelsh.txt')
    except FileNotFoundError:
        print('Error: file not found.')
