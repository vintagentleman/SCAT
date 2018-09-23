import os
import re
import glob
import tools
import obj
from lib import letter_values


def parse_line(line):
    line = tools.replace_chars(line, 'ABEKMHOPCTXЭaeopcyx', 'АВЕКМНОРСТХ+аеорсух')
    nums = line[line.rfind('/') + 1:].split()
    toks = line[:line.rfind('/')].split()
    i = 0

    # Сборка токенов из множества кусков
    while i < len(toks):
        # Межстраничные разрывы
        if toks[i] == 'Z':
            toks[i] = ' '.join([toks[i], toks[i + 1]])
            del toks[i + 1]

        # Разрывы *до* ошибок: ср. '~АБВZ -123 ГДЖ <АБВZ -123 ГДЕ>'
        elif toks[i].endswith('Z'):
            toks[i] = ' '.join([toks[i], toks[i + 1], toks[i + 2]])
            del toks[i + 1:i + 3]

        # Ошибочные написания
        if len(toks) > i + 1 and toks[i + 1].startswith('<'):
            corr = toks[i + 1]
            del toks[i + 1]

            # Бывают и множественные
            while '>' not in corr:
                corr += ' ' + toks[i + 1]
                del toks[i + 1]

            toks[i] = ' '.join([toks[i], corr])

        # Висячая пунктуация справа и мелкие разрывы
        if len(toks) > i + 1 and re.match(r'[.,:;\]&\\]+', toks[i + 1]):
            toks[i] += toks[i + 1]
            del toks[i + 1]

        i += 1

    return [obj.Token(t) for t in toks], nums


def line_gener(toks, nums):
    nums_done = 0

    for t in toks:
        if t.word == '*':
            num = nums[nums_done]

            # Не быть титла не может
            if '#' not in num:
                num += '#'
            titlo = num.index('#')

            if num[0] == '$':
                value = letter_values[num[1]] * 1000 + sum(letter_values.get(letter, 0) for letter in num[2:titlo])
            else:
                value = sum(letter_values.get(letter, 0) for letter in num[0:titlo])

            yield ('%s\t%d' + '\t' * 5) % (str(t).replace('*', num), value)
            nums_done += 1

        else:
            yield str(t)


if __name__ == '__main__':
    root = os.getcwd()
    os.makedirs(root + '\\txt', exist_ok=True)
    os.chdir(root + '\\src')
    names = glob.glob('*.txt')

    for name in names:
        inpt = open(name, mode='r', encoding='IBM866')
        os.chdir(root + '\\txt')

        with open(name[:-3] + 'csv', mode='w', encoding='utf-8') as otpt:
            for l in inpt.readlines():
                p = parse_line(l)

                for _ in line_gener(p[0], p[1]):
                    otpt.write('%s\n' % _)

        os.chdir(root + '\\src')
        inpt.close()
