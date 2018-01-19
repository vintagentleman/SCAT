import unittest
import src_to_txt


class TestParsing(unittest.TestCase):

    def test_parse_line(self):
        result = src_to_txt.parse_line('И СЛЫША МАZ -26 НIЕМЪ СЛО(в).;& Z -22 *СКАZ -19 ЗА&ЮЩЕЕ .*. БЛГОZ 23 ВО(Л)СТВО#, И ЖИ(Т)Е, МАZ -26 НIЕМЪ/    А# Б#')
        self.assertEqual(result, (
            [
                'И',
                'СЛЫША',
                'МАZ -26 НIЕМЪ',
                'СЛО(в)',
                '.;',
                '&',
                'Z -22',
                '*СКАZ -19 ЗА&ЮЩЕЕ',
                '.',
                '*',
                '.',
                'БЛГОZ 23 ВО(Л)СТВО#',
                ',',
                'И',
                'ЖИ(Т)Е',
                ',',
                'МАZ -26 НIЕМЪ',
            ],
            [
                'А#',
                'Б#'
            ]))

        result = src_to_txt.parse_line('И СЛЫША МАZ -26 НIЕМЪ ЯКW ГЛА(с) ЗВОНRЩЬ В ТОИ ПGСТЫНI& НА РЕЦ+ *ГЛGШИЦ+./')
        self.assertEqual(result, (
            [
                'И',
                'СЛЫША',
                'МАZ -26 НIЕМЪ',
                'ЯКW',
                'ГЛА(с)',
                'ЗВОНRЩЬ',
                'В',
                'ТОИ',
                'ПGСТЫНI',
                '&',
                'НА',
                'РЕЦ+',
                '*ГЛGШИЦ+',
                '.'],
            []))

    def test_parse_edit(self):
        result = src_to_txt.parse_line('И& ~W(Т)&НИГШЕ <W(Т)& НИХ ЖЕ>, Б+ШR ВИД+ЛИ ~РАZ 449 ЗD(М)МО(М) <РАZ 449 ЗDМО(М)> БЛЖННА(г)#&/')
        self.assertEqual(result, (
            [
                'И',
                '&',
                '~W(Т)&НИГШЕ <W(Т)& НИХ ЖЕ>',
                ',',
                'Б+ШR',
                'ВИД+ЛИ',
                '~РАZ 449 ЗD(М)МО(М) <РАZ 449 ЗDМО(М)>',
                'БЛЖННА(г)#',
                '&'],
            []))


class TestNumbering(unittest.TestCase):

    def setUp(self):
        self.tab = '%s\t%d' + '\t' * 5

    def test_number(self):
        result = list(src_to_txt.process(['*', '*', '*', '*', '*'], ['А#', 'КВ#', 'ТЛГ#', 'МД#,Е', 'ФНЕ#..Е']))
        self.assertEqual(result, [
            self.tab % ('А#', 1),
            self.tab % ('КВ#', 22),
            self.tab % ('ТЛГ#', 333),
            self.tab % ('МД#,Е', 44),
            self.tab % ('ФНЕ#..Е', 555)
        ])

    def test_thousand(self):
        result = list(src_to_txt.process(['*', '*', '*', '*', '*'], ['$АВ#', '$ЗРД#', '$ДЛS#', '$SЦL#,ТНОЕ', '$FQПЕ#.МD']))
        self.assertEqual(result, [
            self.tab % ('$АВ#', 1002),
            self.tab % ('$ЗРД#', 7104),
            self.tab % ('$ДЛS#', 4036),
            self.tab % ('$SЦL#,ТНОЕ', 6960),
            self.tab % ('$FQПЕ#.МD', 9785),
        ])


if __name__ == '__main__':
    unittest.main()
