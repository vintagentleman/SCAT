import os
import re
import glob
import csv
import xml_modif
from obj import Token


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
        form = row[0].strip()
        tokens = []

        # Расчленяем словоформу на четыре блока (всегда обязательно наличествует по крайней мере один):
        # 1) начальные знаки препинания - это м. б. только '[' (символ начала вставки), 2) сама словоформа,
        # 3) висячие (конечные) знаки препинания и 4) висячие разрывы. Порядок именно такой: ср. '[МIРЪ.] Z 27'
        pc_l = br = pc_r = ''

        pc_l_mo = re.search('^[.,:;[]+', form)
        if pc_l_mo:
            form, pc_l = form[pc_l_mo.end():].strip(), form[:pc_l_mo.end()].strip()

        br_mo = re.search(r'[%&\\]$|Z (-?\d+)$', form)
        if br_mo:
            form, br = form[:br_mo.start()].strip(), form[br_mo.start():].strip()

        pc_r_mo = re.search('[.,:;\]]+$', form)
        if pc_r_mo:
            form, pc_r = form[:pc_r_mo.start()].strip(), form[pc_r_mo.start():].strip()

        # --- Пунктуация слева --- #
        if pc_l:
            punct = pc_l.replace('[', '')
            token = pc_l.replace('[', '<add place="margin"><c>[</c>')
            if punct:
                token = token.replace(punct, '<pc xml:id="%s.%s" force="%s">%s</pc>' % (fn, xmlid, force(punct), punct))
                xmlid += 1
            tokens.append(token)

        # --- Словоформа (с разметкой или без) --- #
        if form:
            if len(row) == 7:
                token = Token(form, fn, xmlid, [row[i].strip() for i in range(1, 7)])
            elif len(row) == 1:
                token = Token(form, fn, xmlid)
            else:
                print('Warning: corrupt data in file %s, line %d.' % (fn, i + 1))
                continue

            tokens.append(token)
            xmlid += 1

        # --- Пунктуация справа --- #
        if pc_r:
            punct = pc_r.replace(']', '')
            token = pc_r.replace(']', '<c>]</c></add>')
            if punct:
                token = token.replace(punct, '<pc xml:id="%s.%s" force="%s">%s</pc>' % (fn, xmlid, force(punct), punct))
                xmlid += 1
            tokens.append(token)

        # --- Висячие разрывы --- #
        if '&' in br:
            data['line'] += 1
            tokens += ['<lb n="%d"/>' % data['line']]

        # Если в рукописи есть колонки, то разрыв колонки обозначает переход ко второй,
        # разрыв страницы - обновление нумерации и переход к первой. Третьей не дано
        elif '\\' in br or 'Z' in br:
            if '\\' in br:
                data['col'] = 'b'
            else:
                data['page'] = br_mo.group(1)
                if 'col' in data:
                    data['col'] = 'a'

            data['line'] = 1
            tokens += ['<pb n="%s"/><lb n="1"/>' % (data['page'] + data.get('col', ''))]

        for token in tokens:
            otpt.write('    %s\n' % str(token))

        if r'%' in br:
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
    names = glob.glob('*.csv')

    for name in names:
        f = name[:-4]
        data = Token.metadata[f]
        main(f)
