from random import *
from macros import *

def single_point_xover(pheno_1, pheno_2):
    cut_point = randint(1, FULL_ENCODING_SIZE * NUMBER_OF_PAPERS - 1)
    cut_section_1, cut_section_2 = pheno_1[0:cut_point], pheno_2[0:cut_point]

    child_1 = pheno_1.replace(cut_section_1, cut_section_2)
    child_2 = pheno_2.replace(cut_section_2, cut_section_1)

    return child_1, child_2
