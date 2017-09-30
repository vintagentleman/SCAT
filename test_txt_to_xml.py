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
        punct = txt_to_xml.Punct(',:', 'Test.1')
        self.assertEqual(str(punct), '<pc xml:id="Test.1">,:</pc>')

    def test_plain(self):
        token = txt_to_xml.Token('СВИН', 'Test.2')
        self.assertEqual(str(token), '''<w xml:id="Test.2">
  <orig>свин</orig>
  <reg>СВИН</reg>
  <src>СВИН</src>
</w>''')

    def test_name(self):
        token = txt_to_xml.Token('*РОМА', 'Test.3')
        self.assertEqual(str(token), '''<name>
<w xml:id="Test.3">
  <orig>рома</orig>
  <reg>*РОМА</reg>
  <src>*РОМА</src>
</w>
</name>''')

    def test_sic(self):
        token = txt_to_xml.Token('~РМОА', 'Test.4')
        self.assertEqual(str(token), '''<w xml:id="Test.4">
  <orig><sic>рмоа</sic></orig>
  <reg>~РМОА</reg>
  <src>~РМОА</src>
</w>''')

    def test_old_letters(self):
        token = txt_to_xml.Token('IRWU+FSGDLQЯ', 'Test.5')
        self.assertEqual(str(token), '''<w xml:id="Test.5">
  <orig>їѧѡѹѣѳѕѫꙋѯѱꙗ</orig>
  <reg>ИЯОУ+ФЗУУКСПСЯ</reg>
  <src>IRWU+FSGDLQЯ</src>
</w>''')

    def test_overline_1(self):
        token = txt_to_xml.Token('НЕ(БВГДЖЗКЛМНОПРСТХЦЧШЩFАЕD+ЮRGЯИIЪЬWЫУU)ГР', 'Test.6')
        self.assertEqual(str(token), '''<w xml:id="Test.6">
  <orig>неⷠⷡⷢⷣⷤⷥⷦⷧⷨⷩⷪⷫⷬⷭⷮⷯⷰⷱⷲⷳⷴⷶⷷⷹⷺⷻⷽⷾⷼ&i8-overline;&i10-overline;꙽&yer-overline;&omega-overline;&yeri-overline;&u-overline;&ou-overline;гр</orig>
  <reg>НЕ(БВГДЖЗКЛМНОПРСТХЦЧШЩФАЕУ+ЮЯУЯИИЪЬОЫУУ)ГР</reg>
  <src>НЕ(БВГДЖЗКЛМНОПРСТХЦЧШЩFАЕD+ЮRGЯИIЪЬWЫУU)ГР</src>
</w>''')

    def test_overline_2(self):
        token = txt_to_xml.Token('Н(ЪЬ)Е(U)Г(Г+)Р', 'Test.7')
        self.assertEqual(str(token), '''<w xml:id="Test.7">
  <orig>н꙽&yer-overline;е&ou-overline;гⷢⷺр</orig>
  <reg>Н(ЪЬ)Е(У)Г(Г+)Р</reg>
  <src>Н(ЪЬ)Е(U)Г(Г+)Р</src>
</w>''')

    def test_overline_3(self):
        token = txt_to_xml.Token('W(Т)', 'Test.8')
        self.assertEqual(str(token), '''<w xml:id="Test.8">
  <orig>ѿ</orig>
  <reg>О(Т)</reg>
  <src>W(Т)</src>
</w>''')

    def test_overline_cover_1(self):
        token = txt_to_xml.Token('ЧУПА(ка)БРА', 'Test.9')
        self.assertEqual(str(token), '''<w xml:id="Test.9">
  <orig>чупа҇ⷦⷶбра</orig>
  <reg>ЧУПА(ка)БРА</reg>
  <src>ЧУПА(ка)БРА</src>
</w>''')

    def test_overline_cover_2(self):
        token = txt_to_xml.Token('ЧУПА(+а)БРА', 'Test.10')
        self.assertEqual(str(token), '''<w xml:id="Test.10">
  <orig>чупа҇ⷺⷶбра</orig>
  <reg>ЧУПА(+а)БРА</reg>
  <src>ЧУПА(+а)БРА</src>
</w>''')

    def test_overline_cover_3(self):
        token = txt_to_xml.Token('ЧУПА(u)БРА', 'Test.11')
        self.assertEqual(str(token), '''<w xml:id="Test.11">
  <orig>чупа҇&ou-overline;бра</orig>
  <reg>ЧУПА(у)БРА</reg>
  <src>ЧУПА(u)БРА</src>
</w>''')

    def test_line_break_1(self):
        token = txt_to_xml.Token('РАМ&ЗАН', 'Test.12')
        self.assertTrue(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.12">
  <orig>рам<lb/>зан</orig>
  <reg>РАМЗАН</reg>
  <src>РАМ&amp;ЗАН</src>
</w>''')

    def test_line_break_2(self):
        token = txt_to_xml.Token('РАМЗАН&', 'Test.13')
        self.assertTrue(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.13">
  <orig>рамзан</orig>
  <reg>РАМЗАН</reg>
  <src>РАМЗАН&amp;</src>
</w>''')

    def test_line_break_3(self):
        token = txt_to_xml.Token('РАМЗАН', 'Test.14')
        self.assertFalse(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.14">
  <orig>рамзан</orig>
  <reg>РАМЗАН</reg>
  <src>РАМЗАН</src>
</w>''')

    def test_line_break_4(self):
        token = txt_to_xml.Token('&', 'Test.15')
        self.assertTrue(token.line_b)
        self.assertEqual(str(token), '''<w xml:id="Test.15">
  <orig><lb/></orig>
  <reg></reg>
  <src>&amp;</src>
</w>''')

    def test_page_break_1(self):
        token = txt_to_xml.Token('ЧИНГИZ -33 СХАН', 'Test.16')
        self.assertTrue(token.page_b)
        self.assertFalse(token.next_page_is_front)
        self.assertEqual(token.next_page_num, '33')
        self.assertEqual(str(token), '''<w xml:id="Test.16">
  <orig>чинги<pb/>схан</orig>
  <reg>ЧИНГИСХАН</reg>
  <src>ЧИНГИZ -33 СХАН</src>
</w>''')

    def test_page_break_2(self):
        token = txt_to_xml.Token('ЧИНГИZ 33 СХАН', 'Test.17')
        self.assertTrue(token.page_b)
        self.assertTrue(token.next_page_is_front)
        self.assertEqual(token.next_page_num, '33')
        self.assertEqual(str(token), '''<w xml:id="Test.17">
  <orig>чинги<pb/>схан</orig>
  <reg>ЧИНГИСХАН</reg>
  <src>ЧИНГИZ 33 СХАН</src>
</w>''')

    def test_page_break_3(self):
        token = txt_to_xml.Token('Z -5', 'Test.18')
        self.assertTrue(token.page_b)
        self.assertFalse(token.next_page_is_front)
        self.assertEqual(token.next_page_num, '5')
        self.assertEqual(str(token), '''<w xml:id="Test.18">
  <orig><pb/></orig>
  <reg></reg>
  <src>Z -5</src>
</w>''')

    def test_titlo_1(self):
        token = txt_to_xml.Token('КЛБС#', 'Test.19')
        self.assertEqual(str(token), '''<w xml:id="Test.19">
  <orig>кл҃бс</orig>
  <reg>КЛБС#</reg>
  <src>КЛБС#</src>
</w>''')

    def test_titlo_2(self):
        token = txt_to_xml.Token('К(U)#', 'Test.20')
        self.assertEqual(str(token), '''<w xml:id="Test.20">
  <orig>к&ou-overline;҃</orig>
  <reg>К(У)#</reg>
  <src>К(U)#</src>
</w>''')

    def test_titlo_3(self):
        token = txt_to_xml.Token('К(U)Р#', 'Test.21')
        self.assertEqual(str(token), '''<w xml:id="Test.21">
  <orig>к&ou-overline;҃р</orig>
  <reg>К(У)Р#</reg>
  <src>К(U)Р#</src>
</w>''')

    def test_titlo_4(self):
        token = txt_to_xml.Token('КР#', 'Test.22')
        self.assertEqual(str(token), '''<w xml:id="Test.22">
  <orig>кр҃</orig>
  <reg>КР#</reg>
  <src>КР#</src>
</w>''')

    def test_num(self):
        token = txt_to_xml.Token('АI#', 'Test.23', ['11', '', '', '', '', ''])
        self.assertEqual(str(token), '''<num value="11">
<w xml:id="Test.23">
  <orig>аї҃</orig>
  <reg>АI#</reg>
  <src>АI#</src>
</w>
</num>''')

    def test_num_1000(self):
        token = txt_to_xml.Token('$А#', 'Test.24', ['1000', '', '', '', '', ''])
        self.assertEqual(str(token), '''<num value="1000">
<w xml:id="Test.24">
  <orig>҂а҃</orig>
  <reg>$А#</reg>
  <src>$А#</src>
</w>
</num>''')


if __name__ == '__main__':
    unittest.main()
