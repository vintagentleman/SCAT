import os
import glob
from xml.dom import minidom
from xml.dom.minidom import Node


def remove_blanks(node):
    # Источник: https://stackoverflow.com/a/16919069

    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            remove_blanks(x)


def process(fn):

    def pack_next(node):
        next_node = node.nextSibling

        if next_node.tagName in ('pc', 'num'):
            if next_node.tagName == 'pc':
                next_node.tagName = 'c'
                node.appendChild(next_node)
            else:
                node.appendChild(next_node.firstChild)
                # Удаление лишних тегов <num> из дерева и списка
                node.parentNode.removeChild(next_node)
                num_all.remove(next_node)
            pack_next(node)

    fo = open(fn, mode='r', encoding='utf-8')

    # Загрузка XML-документа в DOM и очистка от пустых текстовых узлов
    xml = minidom.parse(fo)
    remove_blanks(xml)
    xml.normalize()

    # Список всех изначальных тегов <num>
    num_all = xml.getElementsByTagName('num')

    for num in num_all:
        # Упаковка <pc> в препозиции
        prev_node = num.previousSibling
        # TODO Добавить условие на содержимое узла: упаковывать надо только точку и запятую
        if prev_node.tagName == 'pc':
            # Смена типа узла с маркированного на нейтральный
            prev_node.tagName = 'c'
            num.insertBefore(prev_node, num.firstChild)
        # Последовательная упаковка <pc> и <num> в постпозиции
        pack_next(num)

        # Суммирование значений
        total = sum([int(node.getAttribute('reg')) for node in num.getElementsByTagName('w')])
        num.setAttribute('value', str(total))

    fo.close()
    with open(fn, mode='w', encoding='utf-8') as fo:
        fo.write(xml.toprettyxml(indent='  ', encoding='utf-8').decode())


if __name__ == '__main__':
    os.chdir(os.getcwd() + '\\xml')
    files = glob.glob('*.xml')

    for file in files:
        process(file)
