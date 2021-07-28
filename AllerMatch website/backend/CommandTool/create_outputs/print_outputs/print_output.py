import re

from create_outputs.print_outputs import prompt_output


def create_all_output(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word,
                        results_identical, alignments_identical, results_partial, results_motif, total_hits, 
                        results_toxins, options):
    info = []
    intro = prompt_output.create_all_info(orf_list, options)

    unique_hits = set()
    for rw in results_window:
        unique_hits.add(rw[0])
    for rw in results_word:
        unique_hits.add(rw[0])
    unique_hits = list(unique_hits)
    unique_hits.sort(key=natural_keys)

    info = prompt_output.create_top_allergens(info, sorted_list)
    info = prompt_output.create_allergen_info(info, orf_list, unique_hits, results_window, alignments_window, results_word, alignments_word)

    unique_hits_celiac = set()
    for ri in results_identical:
        unique_hits_celiac.add(ri[0])
    for rm in results_motif:
        unique_hits_celiac.add(rm[0])

    unique_hits_celiac = list(unique_hits_celiac)
    sorted_celiac = sorted(results_partial, key = lambda x: float(x.e_value))
    
    info = prompt_output.create_top_celiac(info, sorted_celiac)
    info = prompt_output.create_info_celiac(info, unique_hits_celiac, results_identical, alignments_identical, results_motif, total_hits)

    sorted_toxins = sorted(results_toxins, key = lambda x: float(x.e_value))

    info = prompt_output.create_top_toxins(info, sorted_toxins)

    print_output(intro, info)

def create_allergen_output(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word,
                           options):
    info = []
    intro = prompt_output.create_allergen_intro(orf_list, options)

    unique_hits = set()
    for rw in results_window:
        unique_hits.add(rw[0])
    for rw in results_word:
        unique_hits.add(rw[0])
    unique_hits = list(unique_hits)
    unique_hits.sort(key=natural_keys)

    info = prompt_output.create_top_allergens(info, sorted_list)
    info = prompt_output.create_allergen_info(info, orf_list, unique_hits, results_window, alignments_window, results_word, alignments_word)

    print_output(intro, info)


def create_celiac_output(orf_list, results_identical, alignments_identical, results_partial, results_motif, total_hits, options):
    info = []
    intro = prompt_output.create_celiac_intro(orf_list, options)

    unique_hits_celiac = set()
    for ri in results_identical:
        unique_hits_celiac.add(ri[0])
    for rm in results_motif:
        unique_hits_celiac.add(rm[0])

    unique_hits_celiac = list(unique_hits_celiac)
    sorted_celiac = sorted(results_partial, key = lambda x: float(x.e_value))
    
    info = prompt_output.create_top_celiac(info, sorted_celiac)
    info = prompt_output.create_info_celiac(info, unique_hits_celiac, results_identical, alignments_identical, results_motif, total_hits)

    print_output(intro, info)


def create_toxin_output(orf_list, results_toxins, options):
    info = []
    intro = prompt_output.create_toxin_intro(orf_list, options)

    sorted_toxins = sorted(results_toxins, key = lambda x: float(x.e_value))

    info = prompt_output.create_top_toxins(info, sorted_toxins)

    print_output(intro, info)


def print_output(intro, info):
    for line in intro:
        print(line)
    for line in info:
        print(line)


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]
