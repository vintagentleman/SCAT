import unittest
from lxml import etree


class TestTransform(unittest.TestCase):

    def setUp(self):
        with open('xml_to_txm.xsl', mode='r', encoding='utf-8') as file:
            xslt = etree.XML(file.read())
            self.transform = etree.XSLT(xslt)

    def test_plain(self):
        token = etree.fromstring('''<w xml:id="Test.1">
  <orig>м҇ⷭца</orig>
  <reg>М(с)ЦА</reg>
  <src>М(с)ЦА</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.1" src="М(с)ЦА" reg="М(с)ЦА">м҇ⷭца</w>
''')

    def test_punct(self):
        token = etree.fromstring('<pc xml:id="Test.8">;</pc>')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<pc xml:id="Test.8">;</pc>
''')

    def test_attributes(self):
        token = etree.fromstring('''<w xml:id="Test.2" ana="сущ;jo;род;ед;м" lemma="ФЕВРАЛЬ">
  <orig>ѳевралѧ</orig>
  <reg>ФЕВРАЛЯ</reg>
  <src>FЕВРАЛR</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.2" ana="сущ;jo;род;ед;м" lemma="ФЕВРАЛЬ" src="FЕВРАЛR" reg="ФЕВРАЛЯ">ѳевралѧ</w>
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
          
<num value="11">
<w xml:id="Test.3" src="АI#" reg="АI#">аї҃</w>
</num>
          <lb n="1"/>
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
<w xml:id="Test.4" src="ИСПО&amp;ЛНЬ" reg="ИСПОЛНЬ">исполнь</w>
''')

    def test_tree_3(self):
        token = etree.fromstring('''<w xml:id="Test.5">
  <orig>прави<pb/>тель</orig>
  <reg>ПРАВИТЕЛЬ</reg>
  <src>ПРАВИZ 59 ТЕЛЬ</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.5" src="ПРАВИZ 59 ТЕЛЬ" reg="ПРАВИТЕЛЬ">правитель</w>
''')

    def test_choice(self):
        token = etree.fromstring('''<w xml:id="Test.6">
  <orig><choice><sic>смиремѹ<lb/>дрїе</sic><corr>смиреномѹ<lb/>дрїе</corr></choice></orig>
  <reg>~СМИРЕМУДРИЕ &lt;СМИРЕНОМУДРИЕ&gt;</reg>
  <src>~СМИРЕМU&amp;ДРIЕ &lt;СМИРЕНОМU&amp;ДРIЕ&gt;</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.6" src="~СМИРЕМU&amp;ДРIЕ &lt;СМИРЕНОМU&amp;ДРIЕ&gt;" reg="~СМИРЕМУДРИЕ &lt;СМИРЕНОМУДРИЕ&gt;">смиреномѹдрїе</w>
''')

    def test_sic(self):
        token = etree.fromstring('''<w xml:id="Test.7">
  <orig><sic>бл҇ⷭве</sic></orig>
  <reg>~БЛ(с)ВЕ</reg>
  <src>~БЛ(с)ВЕ&amp;</src>
</w>''')
        self.assertEqual(str(self.transform(token)), '''<?xml version="1.0"?>
<w xml:id="Test.7" src="~БЛ(с)ВЕ&amp;" reg="~БЛ(с)ВЕ">бл҇ⷭве</w>
''')

if __name__ == '__main__':
    unittest.main()
