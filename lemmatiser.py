import os
import obj
# import doub_cons


class cd:
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.old_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_path)


if __name__ == '__main__':
    tokens = list()

    try:
        with cd(os.getcwd() + '\\data'):
            print('Please wait. Python is processing your data...')
            tokens = obj.main(tokens)
    except FileNotFoundError:
        print('Error: source data directory missing.')

    if tokens:
        # Отождествление дублетов с двойными согласными
        # doub_cons.main(tokens)

        # Стандартный вывод
        out = open('output.txt', mode='w', encoding='utf-8')
        err = open('errors.txt', mode='w', encoding='utf-8')

        for t in tokens:
            out.write(str(t) + '\n')

            if t.stem == 'NONE':
                err.write(str(t) + '\n')

        out.close()
        err.close()
