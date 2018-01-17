import os
import re
import glob
import tools
from lib import letter_values


def parse_line(line):
    line = tools.replace_chars(line, 'ABEKMHOPCTXЭaeopcyx', 'АВЕКМНОРСТХ+аеорсух')

    nums = line[line.rfind('/') + 1:].split()
    line = line[:line.rfind('/')].split()

    j = 0
    while j < len(line):

        if len(line) > j + 1 and line[j + 1][0] == '<':
            corr = line[j + 1]
            del line[j + 1]

            while '>' not in corr:
                corr += ' ' + line[j + 1]
                del line[j + 1]

            line[j] = '%s %s' % (line[j], corr)

        punct = re.search('[.,:;?!]', line[j])
        if punct and punct.start() > 0:
            line.insert(j + 1, line[j][punct.start():])
            line[j] = line[j][:punct.start()]

        elif line[j][-1] in ('&', '\\') and len(line[j]) > 1:
            line.insert(j + 1, line[j][-1])
            line[j] = line[j][:-1]

        if line[j] == 'Z':
            line[j] = '%s %s' % (line[j], line[j + 1])
            del line[j + 1]

        elif line[j][-1] == 'Z':
            line[j] = '%s %s %s' % (line[j], line[j + 1], line[j + 2])
            del line[j + 1:j + 3]
            j -= 1

        j += 1

    return line, nums


def process(wrds, nums):
    nums_done = 0

    for word in wrds:
        if word == '*':
            num = nums[nums_done]
            titlo = num.index('#')

            if num[0] == '$':
                value = letter_values[num[1]] * 1000 + sum(letter_values.get(letter, 0) for letter in num[2:titlo])
            else:
                value = sum(letter_values.get(letter, 0) for letter in num[0:titlo])

            yield ('%s\t%d' + '\t' * 5) % (num, value)
            nums_done += 1

        else:
            yield word


def get_txt(file, root_dir):

    inpt = open(file, mode='r', encoding='IBM866')
    os.makedirs(root_dir + '\\txt', exist_ok=True)
    os.chdir(root_dir + '\\txt')
    otpt = open(file[:-3] + 'csv', mode='w', encoding='utf-8')

    for i in inpt.readlines():
        i = parse_line(i)

        for token in process(i[0], i[1]):
            otpt.write('%s\n' % token)

    otpt.close()
    os.chdir(root_dir + '\\src')
    inpt.close()


if __name__ == '__main__':
    try:
        root = os.getcwd()
        os.chdir(root + '\\src')

        print('Please wait. Python is processing your data...')
        files = glob.glob('*.txt')

        for f in files:
            get_txt(f, root)

    except FileNotFoundError:
        print('Error: source data directory missing.')
