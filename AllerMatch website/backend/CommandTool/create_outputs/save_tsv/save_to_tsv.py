import os

from create_outputs.save_tsv import save

def save_all(orf_list, results_full, results_window, alignments_window, results_word, alignments_word, results_identical, alignments_identical, 
            results_partial, results_motif, total_hits, results_toxins, options):
    check_output_folder(options["file_name"], options["timestr"], options["search_type"])
    if orf_list != '':
        save.save_orf_file(orf_list, options["file_name"], options["timestr"], options["search_type"])
    save.save_window_file(results_window, alignments_window, options["file_name"], options["timestr"], options["search_type"])
    save.save_wordmatch_file(results_word, alignments_word, options["file_name"], options["timestr"], options["search_type"])
    save.save_allergen_full(results_full, options["file_name"], options["timestr"], options["search_type"])
    save.save_identical_celiac(results_identical, alignments_identical, options["file_name"], options["timestr"], options["search_type"])
    save.save_full_celiac(results_partial, options["file_name"], options["timestr"], options["search_type"])
    save.save_motif(results_motif, total_hits, options["file_name"], options["timestr"], options["search_type"])  
    save.save_toxin_full(results_toxins, options["file_name"], options["timestr"], options["search_type"])

def save_allergens(orf_list, results_full, results_window, alignments_window, results_word, alignments_word,
                           options):
    check_output_folder(options["file_name"], options["timestr"], options["search_type"])
    if orf_list != '':
        save.save_orf_file(orf_list, options["file_name"], options["timestr"], options["search_type"])
    save.save_window_file(results_window, alignments_window, options["file_name"], options["timestr"], options["search_type"])
    save.save_wordmatch_file(results_word, alignments_word, options["file_name"], options["timestr"], options["search_type"])
    save.save_allergen_full(results_full, options["file_name"], options["timestr"], options["search_type"])


def save_celiac(orf_list, results_identical, alignments_identical, results_partial, results_motif,
                   total_hits, options):
    check_output_folder(options["file_name"], options["timestr"], options["search_type"])
    if orf_list != '':
        save.save_orf_file(orf_list, options["file_name"], options["timestr"], options["search_type"])
    save.save_identical_celiac(results_identical, alignments_identical, options["file_name"], options["timestr"], options["search_type"])
    save.save_full_celiac(results_partial, options["file_name"], options["timestr"], options["search_type"])
    save.save_motif(results_motif, total_hits, options["file_name"], options["timestr"], options["search_type"])    


def save_toxin(orf_list, results_toxins, options):
    check_output_folder(options["file_name"], options["timestr"], options["search_type"])
    if orf_list != '':
        save.save_orf_file(orf_list, options["file_name"], options["timestr"], options["search_type"])
    save.save_toxin_full(results_toxins, options["file_name"], options["timestr"], options["search_type"])


def check_output_folder(input_file, timestr, search_type):
    """
    Checks if the output folder exists, otherwise creates it
    """
    if not os.path.exists('output/'+input_file+'_'+timestr+'_'+search_type):
        os.makedirs('output/'+input_file+'_'+timestr+'_'+search_type)