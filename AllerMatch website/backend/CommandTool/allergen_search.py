import os, time
import click
from Bio import SeqIO

from allergens import pooling
from allergens.searchmethods import calc_full, calc_window, calc_word
from scripts import input_type, orf_search, scripts
from create_outputs.create_pdfs import create_pdf
from create_outputs.print_outputs import print_output
from create_outputs.save_tsv import save_to_tsv

LOC = os.getcwd()+"/CommandTool"
FASTA36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/fasta36"


@click.command()
@click.option('--input_file', '-i', help="The full path to the input file", required=True)
@click.option('--table', '-t', help="Which transcription table to use", type=int, default=1, show_default=True, required=False)
@click.option('--length', '-l', help="minimum protein length to be an ORF", type=int, default=8, show_default=True, required=False)
@click.option('--orf', '-o', help="Search ORFs between start codon and stop codon(instead between stops)", is_flag=True, default=True, show_default=True, required=False)
@click.option('--word', '-w', help="Minimum exact word match length", type=int, default=6, show_default=True, required=False)
@click.option('--window_cutoff', '-c', help="Minimum identity for the 80-aa sliding window", type=int, default=35, show_default=True, required=False)
@click.option('--propeptides', '-p', help="Search in the original sequences(not with the signal- and propeptides removed)", is_flag=True, default=False, show_default=True, required=False)
def allergen_search(input_file, table, length, orf, word, window_cutoff, propeptides):
    file_name = input_file.split('/')[-1].split('.')[0]
    file_input_type = input_type.get_input_fasta_type(input_file)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    options = scripts.create_option_dict(table= table, length= length, orf_type= orf, word= word, window_cutoff= window_cutoff, peptides_removed=propeptides, input_file= input_file, 
                                        file_name= file_name, file_input_type= file_input_type, timestr= timestr, search_type= "allergen_search")

    if file_input_type == "Single_DNA":
        start_single_DNA(options)
    elif file_input_type == "Single_AA":
        start_single_AA(options)
    elif file_input_type == "Multiple_DNA":
        start_multiple_DNA(options)
    elif file_input_type == "Multiple_AA":
        start_multiple_AA(options)

def start_single_DNA(options):
    """
    Start point for when the input file is a one single DNA sequence FASTA file

    Args:
        options: A Dictionary with options received from the user from the command line
    """
    record = SeqIO.read(options["input_file_path"], "fasta")
    orf_list = orf_search.find_orfs([record.seq], [record.id], options["table"], options["length"], options["orf_type"])
    sequences, ids = orf_search.get_seqs_ids_from_orflist(orf_list)

    # No pooling
    #results_window, alignments_window, hits_list = calc_window.calc_window(sequences, ids, options["peptides_removed"], options["cutoff"], GLSEARCH36_EXECUTABLE)
    #results_word, alignments_word = calc_word.calc_wordmatch(sequences, ids, options["peptides_removed"], options["word"])
    results_full, sorted_list = calc_full.calc_full(sequences, ids, options["peptides_removed"], FASTA36_EXECUTABLE) 

    # Pooling
    results_window, alignments_window, hits_list = pooling.get_pool_window(sequences, ids, options)
    results_word, alignments_word = pooling.get_pool_word(sequences, ids, options)  

    save_to_tsv.save_allergens(orf_list, results_full, results_window, alignments_window, results_word, alignments_word, options)
    create_pdf.create_allergen_pdf(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word, options)
    print_output.create_allergen_output(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word, options)

def start_single_AA(options):
    """
    Start point for when the input file is a one single protein sequence FASTA file

    Args:
        options: A Dictionary with options received from the user from the command line
    """
    sequences = []
    ids = []

    record = SeqIO.read(options["input_file_path"], "fasta")
    sequences.append(str(record.seq))
    ids.append(">"+str(record.id))
    
    # No pooling TODO test all possible search methods
    #results_window, alignments_window, hits_list = calc_window.calc_window(sequences, ids, options["peptides_removed"], options["cutoff"], GLSEARCH36_EXECUTABLE)
    #results_word, alignments_word = calc_word.calc_wordmatch(sequences, ids, options["peptides_removed"], options["word"])
    results_full, sorted_list = calc_full.calc_full(sequences, ids, options["peptides_removed"], FASTA36_EXECUTABLE) 

    # Pooling
    results_window, alignments_window, hits_list = pooling.get_pool_window(sequences, ids, options)
    results_word, alignments_word = pooling.get_pool_word(sequences, ids, options) 

    save_to_tsv.save_allergens('', results_full, results_window, alignments_window, results_word, alignments_word, options)
    create_pdf.create_allergen_pdf('', sorted_list, results_window, alignments_window, results_word, alignments_word, options)
    print_output.create_allergen_output('', sorted_list, results_window, alignments_window, results_word, alignments_word, options)
    


def start_multiple_DNA(options):
    """
    Start point for when the input FASTA file contains multiple DNA sequences

    Args:
        options: A Dictionary with options received from the user from the command line
    """
    sequences = []
    ids = []

    for record in SeqIO.parse(options["input_file_path"], "fasta"):
        sequences.append(record.seq)
        ids.append(record.id)

    orf_list = orf_search.find_orfs(sequences, ids, options["table"], options["length"], options["orf_type"])
    sequences, ids = orf_search.get_seqs_ids_from_orflist(orf_list)

    # No pooling
    #results_window, alignments_window, hits_list = calc_window.calc_window(sequences, ids, options["peptides_removed"], options["cutoff"], GLSEARCH36_EXECUTABLE)
    #results_word, alignments_word = calc_word.calc_wordmatch(sequences, ids, options["peptides_removed"], options["word"])
    results_full, sorted_list = calc_full.calc_full(sequences, ids, options["peptides_removed"], FASTA36_EXECUTABLE) 

    # Pooling
    results_window, alignments_window, hits_list = pooling.get_pool_window(sequences, ids, options)
    results_word, alignments_word = pooling.get_pool_word(sequences, ids, options) 

    save_to_tsv.save_allergens(orf_list, results_full, results_window, alignments_window, results_word, alignments_word, options)
    create_pdf.create_allergen_pdf(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word, options)
    print_output.create_allergen_output(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word, options)


def start_multiple_AA(options):
    """
    Start point for when the input FASTA file contains multiple proteins sequences

    Args:
        options: A Dictionary with options received from the user from the command line
    """
    sequences = []
    ids = []
    for record in SeqIO.parse(options["input_file_path"], "fasta"):
        sequences.append(str(record.seq))
        ids.append(str(record.id))

    # No pooling
    #results_window, alignments_window, hits_list = calc_window.calc_window(sequences, ids, options["peptides_removed"], options["window_cutoff"], GLSEARCH36_EXECUTABLE)
    #results_word, alignments_word = calc_word.calc_wordmatch(sequences, ids, options["peptides_removed"], options["word_length"])
    results_full, sorted_list = calc_full.calc_full(sequences, ids, options["peptides_removed"], FASTA36_EXECUTABLE) 

    # Pooling
    results_window, alignments_window, hits_list = pooling.get_pool_window(sequences, ids, options)
    results_word, alignments_word = pooling.get_pool_word(sequences, ids, options)   
   
    save_to_tsv.save_allergens('', results_full, results_window, alignments_window, results_word, alignments_word, options)
    create_pdf.create_allergen_pdf('', sorted_list, results_window, alignments_window, results_word, alignments_word, options)
    print_output.create_allergen_output('', sorted_list, results_window, alignments_window, results_word, alignments_word, options)


if __name__ == "__main__":
    allergen_search()