import unittest
import src_to_txt


class TestParsing(unittest.TestCase):

    def test_parse_line(self):
        result = src_to_txt.parse_line('И СЛЫША МАZ -26 НIЕМЪ СЛО(в).;& Z -22 *СКАZ -19 ЗА&ЮЩЕЕ '
                                       '* БЛГОZ 23 ВО(Л)СТВО#, И ЖИ(Т)Е, МАZ -26 НIЕМЪ/	А# Б#')

        self.assertEqual(result, (['И', 'СЛЫША', 'МАZ -26 НIЕМЪ', 'СЛО(в)', '.;', '&', 'Z -22', '*СКАZ -19 ЗА&ЮЩЕЕ',
                                   '*', 'БЛГОZ 23 ВО(Л)СТВО#', ',', 'И', 'ЖИ(Т)Е', ',', 'МАZ -26 НIЕМЪ'], ['А#', 'Б#']))

        result = src_to_txt.parse_line('И СЛЫША МАZ -26 НIЕМЪ ЯКW ГЛА(с) ЗВОНRЩЬ '
                                       'В ТОИ ПGСТЫНI& НА РЕЦ+ *ГЛGШИЦ+./')

        self.assertEqual(result, (['И', 'СЛЫША', 'МАZ -26 НIЕМЪ', 'ЯКW', 'ГЛА(с)', 'ЗВОНRЩЬ',
                                   'В', 'ТОИ', 'ПGСТЫНI', '&', 'НА', 'РЕЦ+', '*ГЛGШИЦ+', '.'], []))


class TestNumbering(unittest.TestCase):

    def test_letter_value(self):
        result = list(src_to_txt.process(['*', '*', '*', '*', '*'], ['$А#', 'ТАI#', 'ТЛ#', 'ТЛГ#', 'F#']))
        self.assertEqual(result, [
            ('%s\t%d' + '\t' * 5) % ('$А#', 1000),
            ('%s\t%d' + '\t' * 5) % ('ТАI#', 311),
            ('%s\t%d' + '\t' * 5) % ('ТЛ#', 330),
            ('%s\t%d' + '\t' * 5) % ('ТЛГ#', 333),
            ('%s\t%d' + '\t' * 5) % ('F#', 9)
        ])


if __name__ == '__main__':
    unittest.main()
