import os, time
import click
from Bio import SeqIO

from scripts import input_type, orf_search, scripts
from toxins import toxin_fasta_search
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
@click.option('--propeptides', '-p', help="Search in the original sequences(not with the signal- and propeptides removed)", is_flag=True, default=False, show_default=True, required=False)
def toxin_search(input_file, table, length, orf, peptides):
    file_name = input_file.split('/')[-1].split('.')[0]
    file_input_type = input_type.get_input_fasta_type(input_file)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    options = scripts.create_option_dict(table= table, length= length, orf_type= orf, peptides_removed=propeptides, input_file= input_file, file_name= file_name, 
                                        file_input_type= file_input_type, timestr= timestr, search_type= "toxic_search")

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
        options: A Dictionary with options received from the user from the command line#TODO
    """
    record = SeqIO.read(options["input_file_path"], "fasta")
    orf_list = orf_search.find_orfs([record.seq], [record.id], options["table"], options["length"], options["orf_type"])
    sequences, ids = orf_search.get_seqs_ids_from_orflist(orf_list) 

    results_toxins = toxin_fasta_search.get_similar_matches(ids, sequences, options, FASTA36_EXECUTABLE)

    save_to_tsv.save_toxin(orf_list, results_toxins, options)
    create_pdf.create_toxin_pdf(orf_list, results_toxins, options)
    print_output.create_toxin_output(orf_list, results_toxins, options)


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
    
    results_toxins = toxin_fasta_search.get_similar_matches(ids, sequences, options, FASTA36_EXECUTABLE)

    save_to_tsv.save_toxin('', results_toxins, options)
    create_pdf.create_toxin_pdf('', results_toxins, options)
    print_output.create_toxin_output('', results_toxins, options)


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

    results_toxins = toxin_fasta_search.get_similar_matches(ids, sequences, options, FASTA36_EXECUTABLE)#TODO

    save_to_tsv.save_toxin(orf_list, results_toxins, options)
    create_pdf.create_toxin_pdf(orf_list, results_toxins, options)
    print_output.create_toxin_output(orf_list, results_toxins, options)


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

    results_toxins = toxin_fasta_search.get_similar_matches(ids, sequences, options, FASTA36_EXECUTABLE)    
    
    save_to_tsv.save_toxin('', results_toxins, options)
    create_pdf.create_toxin_pdf('', results_toxins, options)
    print_output.create_toxin_output('', results_toxins, options)
    

if __name__ == "__main__":
    toxin_search()