import os
import csv
import glob
import obj
import xml_modif


def force(pc):
    return 'strong' if set(pc) & {':', ';'} else 'weak'


def main(fn):

    inpt = open(fn + '.csv', mode='r', encoding='utf-8')
    reader = csv.reader(inpt, delimiter='\t')
    os.chdir(root + '\\xml')
    otpt = open(fn + '.xml', mode='w+', encoding='utf-8')
    xmlid = 1

    otpt.write('''<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>%s</title>''' % data['title'])

    for pair in data['resp']:
        otpt.write('''
        <respStmt>
          <resp>%s</resp>
          <persName>%s</persName>
        </respStmt>''' % tuple(pair))

    otpt.write('''
      </titleStmt>
      <publicationStmt>
        <publisher>%s</publisher>
        <pubPlace>%s</pubPlace>
        <date>%s</date>
        <idno type="ISBN">%s</idno>
      </publicationStmt>''' % tuple(data['pub']))

    otpt.write('''
      <sourceDesc>
        <bibl>%s</bibl>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <text><body><ab>
    <pb n="%s"/><lb n="1"/>\n''' % (data['bibl'], (data['page'] + data.get('col', ''))))

    for i, row in enumerate(reader):
        t = obj.Token(row[0].strip())
        out = list()

        # Пунктуация слева
        if t.pcl:
            punct = t.pcl.replace('[', '')
            token = t.pcl.replace('[', '<add place="margin"><c>[</c>')
            if punct:
                token = token.replace(punct, '<pc xml:id="%s.%s" force="%s">%s</pc>' % (fn, xmlid, force(punct), punct))
                xmlid += 1
            out.append(token)

        # Словоформа
        if t.word:
            if len(row) == 7:
                token = obj.Word(t.word, fn, xmlid, [row[i].strip() for i in range(1, 7)])
            else:
                token = obj.Word(t.word, fn, xmlid)

            out.append(token)
            xmlid += 1

        # Пунктуация справа
        if t.pcr:
            punct = t.pcr.replace(']', '')
            token = t.pcr.replace(']', '<c>]</c></add>')
            if punct:
                token = token.replace(punct, '<pc xml:id="%s.%s" force="%s">%s</pc>' % (fn, xmlid, force(punct), punct))
                xmlid += 1
            out.append(token)

        # Висячие разрывы
        if t.br is not None:
            if '&' in t.br.group():
                data['line'] += 1
                out.append('<lb n="%d"/>' % data['line'])

            # Если в рукописи есть колонки, то разрыв колонки обозначает переход ко второй,
            # разрыв страницы - обновление нумерации и переход к первой. Третьей не бывает
            elif set(t.br.group()) & {'\\', 'Z'}:
                if '\\' in t.br.group():
                    data['col'] = 'b'
                else:
                    data['page'] = t.br.group(1)
                    if 'col' in data:
                        data['col'] = 'a'

                data['line'] = 1
                out.append('<pb n="%s"/><lb n="1"/>' % (data['page'] + data.get('ol', '')))

        for _ in out:
            otpt.write('    %s\n' % str(_))

        if t.br is not None and r'%' in t.br.group():
            otpt.write('  </ab>\n  <ab>\n')

    otpt.write('  </ab></body></text>\n</TEI>')

    # Постобработка
    otpt.seek(0)
    xml = xml_modif.PostProc(otpt).run()
    otpt.close()

    with open(fn + '.xml', mode='w', encoding='utf-8') as otpt:
        otpt.write(xml.toprettyxml(indent='  ', encoding='utf-8').decode())

    os.chdir(root + '\\txt')
    inpt.close()


if __name__ == '__main__':
    root = os.getcwd()
    os.makedirs(root + '\\xml', exist_ok=True)
    os.chdir(root + '\\txt')
    names = glob.glob('CrlNvz.csv')

    for name in names:
        f = name[:-4]
        data = obj.metadata[f]
        main(f)
