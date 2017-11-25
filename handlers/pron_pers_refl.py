import lib
import re
from handlers import Pron


def main(token):
    gr = Pron(token)
    stem = 'NONE'

    if gr.pers != 'возвр':
        for key in lib.pron_pers:
            if re.match(key[0], gr.form) and (gr.pers, gr.case, gr.num) == key[1]:
                stem = lib.pron_pers[key]
    else:
        for key in lib.pron_refl:
            if re.match(key[0], gr.form) and gr.case == key[1]:
                stem = lib.pron_refl[key]

    return ('', stem), ''
