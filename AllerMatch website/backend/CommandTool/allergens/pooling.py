import os

from multiprocessing import Pool
from collections import defaultdict
from allergens.searchmethods import calc_window, calc_word

LOC = os.getcwd()+"/CommandTool"

FASTA36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/fasta36"
GLSEARCH36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/glsearch36"


def get_pool_window(sequences, ids, options):
    """
    Start function for pooling of the calc_window() function.

    Args:
        sequences: A list contatining all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        cut_off: An integer with the minimum sliding window percent to be considered a hit 

    Returns:
        tsv_values: A list with results to be shown in the tsv-file
        alignments_list: A list with Alignments objects
    """
    pool_input = []
    for s, i in zip(sequences, ids):
        pool_input.append([[s], [i], options["peptides_removed"], options["window_cutoff"], GLSEARCH36_EXECUTABLE])

    p = Pool()
    result = p.map(calc_window.calc_window_pool, pool_input)
    p.close()
    p.join()

    tsv_values = [x[0] for x in result if x[0]]
    alignments = [x[1] for x in result if x[0]]
    hits_list = [x[2] for x in result if x[0]]

    if tsv_values:
        return tsv_values[0], alignments[0], hits_list[0]
    return [], [], []

def get_pool_word(sequences, ids, options):
    """
    Start function for pooling of the calc_wordmatch() function.

    Args:
        sequences: A list contatining all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        ord_length: An integer with the minimum exact word match to be considered a hit 

    Returns:
        tsv_values: A list with results to be shown in the tsv-file
        alignments_list: A list with Alignments objects
    """
    pool_input = []
    for s, i in zip(sequences, ids):
        pool_input.append([[s], [i], options["peptides_removed"], options["word_length"]])

    p = Pool()
    result = p.map(calc_word.calc_wordmatch_pool, pool_input)
    p.close()
    p.join()

    tsv_values = [x[0] for x in result if x[0]]
    tsv_values = [item for sublist in tsv_values for item in sublist]

    alignments = defaultdict(list)
    for r in result:
        for align_dict in r[1]:
            alignments[align_dict] = r[1][align_dict]
    

    return tsv_values, alignments