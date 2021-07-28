from Bio import SeqIO
from Bio.Seq import Seq
import itertools, re
from allergens.exceptions.exceptions import WrongInputException


def get_input_fasta_type(filepath):
    """
    Checks the type of input file. For every different type this tool has to perform
    different actions
    
    Args:
        filepath: A string with the path to the input file
    
    Returns:
        Single_DNA: If the input file contains one DNA sequence
        Single_AA: If the input file contains one protein sequence
        Multiple_DNA: If the input file contains multiple DNA sequences
        Multiple_AA: If the input file contains multiple protein sequences
    """  
    try:
        record = SeqIO.read(filepath, "fasta")
        if check_dna(str(record.seq).upper()):
            return "Single_DNA"
        elif check_aa(str(record.seq).upper()):
            return "Single_AA"
        else:
            raise WrongInputException
    except ValueError:
        sequences = []
        for record in SeqIO.parse(filepath, "fasta"):
            sequences.append(record.seq)

        if all(check_dna(str(s).upper()) for s in sequences):
            return "Multiple_DNA"
        elif all(check_aa(str(s).upper()) for s in sequences):
            return "Multiple_AA"
        else:
            raise WrongInputException


def check_dna(seq, code=re.compile(r'[^ACGTN.]').search):
    """Checks if a sequence consists of DNA-characters.
    
    Args:
        seq: Sequence, must be a string.
        code: Regex pattern.
    
    Returns:
        True: If the sequence is pure DNA.
        False: If the sequence if not (pure) DNA.

    """
    return not bool(code(seq))


def check_aa(seq, code=re.compile(r'[^ACDEFGHIKLMNPQRSTVWY.]').search):
    """Checks if a sequence consists of protein-characters.
    
    Args:
        seq: Sequence, must be a string.
        code: Regex pattern.
    
    Returns:
        True: If the sequence is pure AA.
        False: If the sequence if not (pure) AA.

    """
    return not bool(code(seq))