import unittest
from lxml import etree


class TestTransform(unittest.TestCase):

    def setUp(self):
        with open('xml_to_txm.xsl', mode='r', encoding='utf-8') as file:
            xslt = etree.XML(file.read())
            self.transform = etree.XSLT(xslt)

    # Не нашёл способа избавиться от декларации
    def test_plain(self):
        token = etree.fromstring('''<w xml:id="Test.1">
  <orig>м҇ⷭца</orig>
  <reg>М(с)ЦА</reg>
  <src>М(с)ЦА</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.1" reg="М(с)ЦА">м҇ⷭца</w>
''')

    def test_attributes(self):
        token = etree.fromstring('''<w xml:id="Test.2" ana="сущ;jo;род;ед;м" lemma="ФЕВРАЛЬ">
  <orig>ѳевралѧ</orig>
  <reg>ФЕВРАЛЯ</reg>
  <src>FЕВРАЛR</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.2" ana="сущ;jo;род;ед;м" lemma="ФЕВРАЛЬ" reg="ФЕВРАЛЯ">ѳевралѧ</w>
''')

    def test_tree_1(self):
        token = etree.fromstring('''<text>
  <div1 type="part" n="1">
    <div2 type="page" n="1">
      <div3 type="front">
        <div4 type="col" n="1">
          <l n="1">
<num value="11">
<w xml:id="Test.3">
  <orig>аї҃</orig>
  <reg>АI#</reg>
  <src>АI#</src>
</w>
</num>
          </l>
        </div4>
      </div3>
    </div2>
  </div1>
</text>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<text>
  <div1 type="part" n="1">
    <div2 type="page" n="1">
      <div3 type="front">
        <div4 type="col" n="1">
          <l n="1">
<num value="11">
<w xml:id="Test.3" reg="АI#">аї҃</w>
</num>
          </l>
        </div4>
      </div3>
    </div2>
  </div1>
</text>
''')

    def test_tree_2(self):
        token = etree.fromstring('''<w xml:id="Test.4">
  <orig>испо<lb/>лнь</orig>
  <reg>ИСПОЛНЬ</reg>
  <src>ИСПО&amp;ЛНЬ</src>
</w>''')

        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.4" reg="ИСПОЛНЬ">испо<lb/>лнь</w>
''')

    def test_choice(self):
        token = etree.fromstring('''<w xml:id="Test.5">
  <orig><choice><sic>смиремѹ<lb/>дрїе</sic><corr>смиреномѹ<lb/>дрїе</corr></choice></orig>
  <reg>~СМИРЕМУДРИЕ &lt;СМИРЕНОМУДРИЕ&gt;</reg>
  <src>~СМИРЕМU&amp;ДРIЕ &lt;СМИРЕНОМU&amp;ДРIЕ&gt;</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.5" reg="СМИРЕНОМУДРИЕ">смиреномѹ<lb/>дрїе</w>
''')

    def test_sic(self):
        token = etree.fromstring('''<w xml:id="Test.6">
  <orig><sic>бл҇ⷭве</sic></orig>
  <reg>~БЛ(с)ВЕ</reg>
  <src>~БЛ(с)ВЕ&amp;</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.6" reg="~БЛ(с)ВЕ">бл҇ⷭве</w>
''')


if __name__ == '__main__':
    unittest.main()
