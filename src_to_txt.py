import os
import glob
import txt_to_xml


def parse_line(line):

    def find_any_char(s, c_str):
        k = 0

        while k < len(s):
            if s[k] in c_str:
                return k
            k += 1

        return -1

    line = txt_to_xml.replace_chars(line, 'ABEKMHOPCTXaeopcyx', 'АВЕКМНОРСТХаеорсух')

    nums = line[line.rfind('/') + 1:].split()
    line = line[:line.rfind('/')].split()

    j = 0
    while j < len(line):

        if len(line) > j + 1 and line[j + 1][0] == '<':
            line[j] = '%s %s' % (line[j], line[j + 1])
            del line[j + 1]

        if find_any_char(line[j], '.,:;?!') > 0:
            line.insert(j + 1, line[j][find_any_char(line[j], '.,:;?!'):])
            line[j] = line[j][:find_any_char(line[j], '.,:;?!')]

        elif line[j][-1] == '&' and len(line[j]) > 1:
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

    def get_letter_value(letter):

        return (0, 0, 1, 2, 3, 4, 5, 6, 7, 8,
                10, 20, 30, 40, 50, 70, 80, 100,
                200, 300, 400, 400, 500, 600, 800,
                900, 90, 900, 60, 700, 9, 400)['#$АВГДЕSЗНIКЛМНОПРСТUDФХWЦЧRLQFV'.find(letter)]

    nums_done = 0

    for word in wrds:
        if word == '*':
            num = nums[nums_done]
            thousand = int(num[0] == '$') * 999 + 1
            value = sum(get_letter_value(letter) for letter in num) * thousand

            yield ('%s\t%d' + '\t' * 5) % (num, value)
            nums_done += 1

        else:
            yield word


def get_txt(file, root_dir):

    inpt = open(file, mode='r', encoding='IBM866')
    os.makedirs(root_dir + '\\txt', exist_ok=True)
    os.chdir(root_dir + '\\txt')
    otpt = open(file, mode='w', encoding='utf-8')

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
