import lib
import re
from handlers import Pron


def main(token):
    gr = Pron(token)
    stem = 'NONE'

    if gr.pers != 'возвр':
        if (gr.pers, gr.case, gr.num) in lib.pron_pers:
            if re.match(lib.pron_pers[(gr.pers, gr.case, gr.num)][0], gr.form):
                stem = lib.pron_pers[(gr.pers, gr.case, gr.num)][1]
            elif gr.form == 'М`':
                stem = 'АЗЪ'
            elif gr.form == 'Т`':
                stem = 'ТЫ'
    else:
        if gr.case in lib.pron_refl:
            if re.match(lib.pron_refl[gr.case][0], gr.form):
                stem = lib.pron_refl[gr.case][1]
            elif gr.form == 'С`':
                stem = 'СЕБЕ'

    return ('', stem), ''
