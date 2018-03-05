import os
import re
import glob
import tools
from lib import letter_values


def parse_line(line):
    line = tools.replace_chars(line, 'ABEKMHOPCTXЭaeopcyx', 'АВЕКМНОРСТХ+аеорсух')
    nums = line[line.rfind('/') + 1:].split()
    line = line[:line.rfind('/')].split()

    pc = re.compile(r'[.,:;[\]]+')
    j = 0

    while j < len(line):
        # Собираем токены из множества кусков; начинаем с межстраничных разрывов
        if line[j] == 'Z':
            line[j] = '%s %s' % (line[j], line[j + 1])
            del line[j + 1]

        # Разрывы *до* ошибок, ибо бывает такое: '~АБВZ -123 ГДЖ <АБВZ -123 ГДЕ>'
        elif line[j].endswith('Z'):
            line[j] = '%s %s %s' % (line[j], line[j + 1], line[j + 2])
            del line[j + 1:j + 3]

        # Токены из множества кусков: ошибочные написания
        if len(line) > j + 1 and line[j + 1].startswith('<'):
            corr = line[j + 1]
            del line[j + 1]

            # Бывают и неоднословные
            while '>' not in corr:
                corr += ' ' + line[j + 1]
                del line[j + 1]

            line[j] = '%s %s' % (line[j], corr)

        # Отклеиваем пунктуацию слева
        mo = pc.match(line[j])
        if mo and len(mo.group()) != len(line[j]):
            line.insert(j, line[j][:mo.end()])
            j += 1
            line[j] = line[j][mo.end():]
        # Теперь справа
        mo = pc.search(line[j])
        if mo and len(mo.group()) != len(line[j]):
            line.insert(j + 1, line[j][mo.start():])
            line[j] = line[j][:mo.start()]
            j += 1

        # Висячие разрывы
        if line[j].endswith(('&', '\\')) and len(line[j]) > 1:
            line.insert(j + 1, line[j][-1])
            line[j] = line[j][:-1]

        j += 1

    return line, nums


def process(wrds, nums):
    nums_done = 0

    for word in wrds:
        if word == '*':
            num = nums[nums_done]
            if '#' not in num:
                num += '#'
            titlo = num.index('#')

            if num[0] == '$':
                value = letter_values[num[1]] * 1000 + sum(letter_values.get(letter, 0) for letter in num[2:titlo])
            else:
                value = sum(letter_values.get(letter, 0) for letter in num[0:titlo])

            yield ('%s\t%d' + '\t' * 5) % (num, value)
            nums_done += 1

        else:
            yield word


def get_txt(file):

    inpt = open(file, mode='r', encoding='IBM866')
    os.chdir(root + '\\txt')
    otpt = open(file[:-3] + 'csv', mode='w', encoding='utf-8')

    for i in inpt.readlines():
        i = parse_line(i)

        for token in process(i[0], i[1]):
            otpt.write('%s\n' % token)

    otpt.close()
    os.chdir(root + '\\src')
    inpt.close()


if __name__ == '__main__':
    root = os.getcwd()
    os.makedirs(root + '\\txt', exist_ok=True)
    os.chdir(root + '\\src')
    files = glob.glob('*.txt')

    for f in files:
        get_txt(f)
