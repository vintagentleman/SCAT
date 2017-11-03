import unittest
import txt_to_xml


class TestMeta(unittest.TestCase):

    def test_replace_chars(self):
        s = 'укен'
        fr = 'неку'
        to = ('яч', 'см', 'и', 'ФЫ')

        self.assertEqual(txt_to_xml.replace_chars(s, fr, to), 'ФЫисмяч')

    def test_count_chars(self):
        s = '&ard;С<pb/>&testest;&testetst;<asd/><qwe/><qweqwe/>&r;<qqq/>Л<asd/>'

        self.assertEqual(txt_to_xml.count_chars(s), 6)
        self.assertEqual(txt_to_xml.count_chars(s, 0), 4)
        self.assertEqual(txt_to_xml.count_chars(s, 1), 5)
        self.assertEqual(txt_to_xml.count_chars(s, 2), 19)
        self.assertEqual(txt_to_xml.count_chars(s, 3), 29)
        self.assertEqual(txt_to_xml.count_chars(s, 4), 53)
        self.assertEqual(txt_to_xml.count_chars(s, 5), 60)
        self.assertRaises(IndexError, txt_to_xml.count_chars, s, 6)


class TestToken(unittest.TestCase):

    def test_punct(self):
        punct = txt_to_xml.Punct(',:', 'Test.Punct')
        self.assertEqual(str(punct), '<pc xml:id="Test.Punct">,:</pc>')

    def test_plain(self):
        token = txt_to_xml.Token('СВИН', 'Test.Plain')
        self.assertEqual(str(token), '''<w xml:id="Test.Plain">
  <orig>свин</orig>
  <reg>СВИН</reg>
  <src>СВИН</src>
</w>''')

    def test_name(self):
        token = txt_to_xml.Token('*РОМА', 'Test.Name')
        self.assertEqual(str(token), '''<name>
<w xml:id="Test.Name">
  <orig>рома</orig>
  <reg>*РОМА</reg>
  <src>*РОМА</src>
</w>
</name>''')

    def test_sic(self):
        token = txt_to_xml.Token('~РМОА', 'Test.Sic')
        self.assertEqual(str(token), '''<w xml:id="Test.Sic">
  <orig><sic>рмоа</sic></orig>
  <reg>~РМОА</reg>
  <src>~РМОА</src>
</w>''')

    def test_choice(self):
        token = txt_to_xml.Token('~РМОА <РОМА>', 'Test.Corr')
        self.assertEqual(str(token), '''<w xml:id="Test.Corr">
  <orig><choice><sic>рмоа</sic><corr>рома</corr></choice></orig>
  <reg>~РМОА &lt;РОМА&gt;</reg>
  <src>~РМОА &lt;РОМА&gt;</src>
</w>''')

    def test_old_letters(self):
        token = txt_to_xml.Token('IRWU+FSGDLQЯ', 'Test.Old')
        self.assertEqual(str(token), '''<w xml:id="Test.Old">
  <orig>їѧѡѹѣѳѕѫꙋѯѱꙗ</orig>
  <reg>ИЯОУ+ФЗУУКСПСЯ</reg>
  <src>IRWU+FSGDLQЯ</src>
</w>''')

    def test_overline_1(self):
        token = txt_to_xml.Token('НЕ(БВГДЖЗКЛМНОПРСТХЦЧШЩFАЕD+ЮRGЯИIЪЬWЫУU)ГР', 'Test.Overline_1')
        self.assertEqual(str(token), '''<w xml:id="Test.Overline_1">
  <orig>неⷠⷡⷢⷣⷤⷥⷦⷧⷨⷩⷪⷫⷬⷭⷮⷯⷰⷱⷲⷳⷴⷶⷷⷹⷺⷻⷽⷾⷼ&i8-overline;&i10-overline;꙽&yer-overline;&omega-overline;&yeri-overline;&u-overline;&ou-overline;гр</orig>
  <reg>НЕ(БВГДЖЗКЛМНОПРСТХЦЧШЩФАЕУ+ЮЯУЯИИЪЬОЫУУ)ГР</reg>
  <src>НЕ(БВГДЖЗКЛМНОПРСТХЦЧШЩFАЕD+ЮRGЯИIЪЬWЫУU)ГР</src>
</w>''')

    def test_overline_2(self):
        token = txt_to_xml.Token('Н(ЪЬ)Е(U)Г(Г+)Р', 'Test.Overline_2')
        self.assertEqual(str(token), '''<w xml:id="Test.Overline_2">
  <orig>н꙽&yer-overline;е&ou-overline;гⷢⷺр</orig>
  <reg>Н(ЪЬ)Е(У)Г(Г+)Р</reg>
  <src>Н(ЪЬ)Е(U)Г(Г+)Р</src>
</w>''')

    def test_overline_3(self):
        token = txt_to_xml.Token('W(Т)', 'Test.Overline_3')
        self.assertEqual(str(token), '''<w xml:id="Test.Overline_3">
  <orig>ѿ</orig>
  <reg>О(Т)</reg>
  <src>W(Т)</src>
</w>''')

    def test_overline_cover_1(self):
        token = txt_to_xml.Token('ЧУПА(ка)БРА', 'Test.Cover_1')
        self.assertEqual(str(token), '''<w xml:id="Test.Cover_1">
  <orig>чупа҇ⷦⷶбра</orig>
  <reg>ЧУПА(ка)БРА</reg>
  <src>ЧУПА(ка)БРА</src>
</w>''')

    def test_overline_cover_2(self):
        token = txt_to_xml.Token('ЧУПА(+а)БРА', 'Test.Cover_2')
        self.assertEqual(str(token), '''<w xml:id="Test.Cover_2">
  <orig>чупа҇ⷺⷶбра</orig>
  <reg>ЧУПА(+а)БРА</reg>
  <src>ЧУПА(+а)БРА</src>
</w>''')

    def test_overline_cover_3(self):
        token = txt_to_xml.Token('ЧУПА(u)БРА', 'Test.Cover_3')
        self.assertEqual(str(token), '''<w xml:id="Test.Cover_3">
  <orig>чупа҇&ou-overline;бра</orig>
  <reg>ЧУПА(у)БРА</reg>
  <src>ЧУПА(u)БРА</src>
</w>''')

    def test_line_break_1(self):
        token = txt_to_xml.Token('РАМ&ЗАН', 'Test.LB_1')
        self.assertTrue(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.LB_1">
  <orig>рам<lb/>зан</orig>
  <reg>РАМЗАН</reg>
  <src>РАМ&amp;ЗАН</src>
</w>''')

    def test_line_break_2(self):
        token = txt_to_xml.Token('РАМЗАН&', 'Test.LB_2')
        self.assertTrue(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.LB_2">
  <orig>рамзан</orig>
  <reg>РАМЗАН</reg>
  <src>РАМЗАН&amp;</src>
</w>''')

    def test_line_break_3(self):
        token = txt_to_xml.Token('РАМЗАН', 'Test.LB_3')
        self.assertFalse(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.LB_3">
  <orig>рамзан</orig>
  <reg>РАМЗАН</reg>
  <src>РАМЗАН</src>
</w>''')

    def test_line_break_4(self):
        token = txt_to_xml.Token('&', 'Test.LB_4')
        self.assertTrue(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.LB_4">
  <orig><lb/></orig>
  <reg></reg>
  <src>&amp;</src>
</w>''')

    def test_page_break_1(self):
        token = txt_to_xml.Token('ЧИНГИZ -33 СХАН', 'Test.PB_1')
        self.assertTrue(token.page_b)
        self.assertFalse(token.next_page_is_front)
        self.assertEqual(token.next_page_num, '33')
        self.assertEqual(str(token), '''<w xml:id="Test.PB_1">
  <orig>чинги<pb/>схан</orig>
  <reg>ЧИНГИСХАН</reg>
  <src>ЧИНГИZ -33 СХАН</src>
</w>''')

    def test_page_break_2(self):
        token = txt_to_xml.Token('ЧИНГИZ 33 СХАН', 'Test.PB_2')
        self.assertTrue(token.page_b)
        self.assertTrue(token.next_page_is_front)
        self.assertEqual(token.next_page_num, '33')
        self.assertEqual(str(token), '''<w xml:id="Test.PB_2">
  <orig>чинги<pb/>схан</orig>
  <reg>ЧИНГИСХАН</reg>
  <src>ЧИНГИZ 33 СХАН</src>
</w>''')

    def test_page_break_3(self):
        token = txt_to_xml.Token('Z -5', 'Test.PB_3')
        self.assertTrue(token.page_b)
        self.assertFalse(token.next_page_is_front)
        self.assertEqual(token.next_page_num, '5')
        self.assertEqual(str(token), '''<w xml:id="Test.PB_3">
  <orig><pb/></orig>
  <reg></reg>
  <src>Z -5</src>
</w>''')

    def test_titlo_1(self):
        token = txt_to_xml.Token('КЛБС#', 'Test.Titlo_1')
        self.assertEqual(str(token), '''<w xml:id="Test.Titlo_1">
  <orig>кл҃бс</orig>
  <reg>КЛБС#</reg>
  <src>КЛБС#</src>
</w>''')

    def test_titlo_2(self):
        token = txt_to_xml.Token('К(U)#', 'Test.Titlo_2')
        self.assertEqual(str(token), '''<w xml:id="Test.Titlo_2">
  <orig>к&ou-overline;҃</orig>
  <reg>К(У)#</reg>
  <src>К(U)#</src>
</w>''')

    def test_titlo_3(self):
        token = txt_to_xml.Token('К(U)Р#', 'Test.Titlo_3')
        self.assertEqual(str(token), '''<w xml:id="Test.Titlo_3">
  <orig>к&ou-overline;҃р</orig>
  <reg>К(У)Р#</reg>
  <src>К(U)Р#</src>
</w>''')

    def test_titlo_4(self):
        token = txt_to_xml.Token('КР#', 'Test.Titlo_4')
        self.assertEqual(str(token), '''<w xml:id="Test.Titlo_4">
  <orig>кр҃</orig>
  <reg>КР#</reg>
  <src>КР#</src>
</w>''')

    def test_num(self):
        token = txt_to_xml.Token('АI#', 'Test.Num', ['11', '', '', '', '', ''])
        self.assertEqual(str(token), '''<num value="11">
<w xml:id="Test.Num">
  <orig>аї҃</orig>
  <reg>АI#</reg>
  <src>АI#</src>
</w>
</num>''')

    def test_thousand(self):
        token = txt_to_xml.Token('$А#', 'Test.Thousand', ['1000', '', '', '', '', ''])
        self.assertEqual(str(token), '''<num value="1000">
<w xml:id="Test.Thousand">
  <orig>҂а҃</orig>
  <reg>$А#</reg>
  <src>$А#</src>
</w>
</num>''')


class TestLemma(unittest.TestCase):

    def test_plain(self):
        token = txt_to_xml.Token('Д+ЛЫ', 'Test.Plain', ['сущ', 'o', 'тв', 'мн', 'ср', ''])
        self.assertEqual(token.lemma, 'Д+ЛО')

    def test_ii(self):
        token = txt_to_xml.Token('БЛА&ГIИ#', 'Test.II', ['прил', 'тв', 'вин', 'ед', 'м', ''])
        self.assertEqual(token.lemma, 'БЛАГИИ')

        token = txt_to_xml.Token('*ИИ#', 'Test.II', ['сущ', 'o', 'род', 'ед', 'м', ''])
        self.assertEqual(token.lemma, '*ИИСУСЪ')


if __name__ == '__main__':
    unittest.main()
