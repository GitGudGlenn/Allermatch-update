from Bio import SeqIO
from Bio.Seq import Seq

def find_orfs(seqs, ids, trans_table, min_protein_length, orf_type):
    if orf_type:
        return find_orfs_between_stops(seqs, ids, trans_table, min_protein_length)
    else:
        return find_orfs_between_start_stop(seqs, ids, trans_table, min_protein_length)


def find_orfs_between_stops(seqs, ids, trans_table, min_protein_length):
    answer = []
    orf_counter = 1
    for(seq,i) in zip(seqs, ids):
        seq_len = len(seq)
        for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
            for frame in range(3):
                sequence = str(nuc[frame:])
                trailing_n = len(sequence) % 3
                sequence = Seq(sequence + 'N' * (3 - trailing_n))
                trans = str(sequence.translate(trans_table)).replace('X','')
                trans_len = len(trans)
                aa_start = 0
                aa_end = 0
                while aa_start < trans_len:
                    aa_end = trans.find("*", aa_start)
                    if aa_end == -1:
                        aa_end = trans_len
                    if aa_end - aa_start >= min_protein_length:
                        if strand == 1:
                            start = frame + aa_start * 3
                            end = min(seq_len, frame + aa_end * 3 + 3)
                        else:
                            start = seq_len - frame - aa_end * 3 - 3
                            end = seq_len - frame - aa_start * 3
                        answer.append((">ORF_"+str(orf_counter), trans[aa_start:aa_end], len(trans[aa_start:aa_end]), strand, frame+1, start+1, end+1, id))
                        orf_counter += 1
                    aa_start = aa_end + 1
    return answer


def find_orfs_between_start_stop(seqs, ids, trans_table, min_protein_length):
    """
    Finds ORF(Open Reading Frames) from the input file when there are multiple DNA
    sequences.

    Args:
        seq: A string with the DNA sequence in which ORFs will be found
        trans_table: A integer which tells which transcription table to use
        min_protein_length: A integer which tells the minimum protein length to be considered a ORF

    Returns:
        answer: A list containing ORFs with their:
            (newly generated) ID:
            Sequence:
            Length:
            Strand:  1 or -1
            Frame:   1, 2 or 3
            Start:   
            Ends:
    """
    answer = []
    orf_counter = 1
    for (seq, i) in zip(seqs, ids):
        seq_len = len(seq)
        for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
            for frame in range(3):
                sequence = str(nuc[frame:])
                trailing_n = len(sequence) % 3
                sequence = Seq(sequence + 'N' * (3 - trailing_n))
                trans = str(sequence.translate(trans_table)).replace('X','')
                trans_len = len(trans)
                aa_start = 0
                aa_end = 0
                while aa_start < trans_len:
                    aa_end = trans.find("*", aa_start)
                    if aa_end == -1:
                        aa_end = trans_len
                    if aa_end - aa_start >= min_protein_length:
                        met_pos = trans[aa_start:aa_end].find("M")
                        if strand == 1:
                            start = frame + aa_start * 3 +(met_pos*3+1)
                            end = min(seq_len, frame + aa_end * 3 + 3)
                        else:
                            start = seq_len - (trans.find(trans[aa_start+met_pos:aa_end]) * 3 + frame)
                            end =  start - (len(trans[aa_start+met_pos:aa_end] * 3)) -2
                        if met_pos >= 0:
                            if len(trans[aa_start+met_pos:aa_end]) >= min_protein_length:
                                answer.append((">ORF_"+str(orf_counter), trans[aa_start+met_pos:aa_end], len(trans[aa_start+met_pos:aa_end]), strand, frame+1, start, end, i))
                                orf_counter += 1
                    aa_start = aa_end + 1
        orf_counter = 1
    return answer


def get_seqs_ids_from_orflist(orf_list):
    """
    Extracts the sequence and the id from the ORF list an puts it in two different lists
    
    Args:
        orf_list: A list containing ORFs
    
    Returns:
        sequences: A list containing the sequences
        ids: A list containing the IDs
    """
    sequences = []
    ids = []
    for orf in orf_list:
        sequences.append(orf[1])
        ids.append(orf[0])
    
    return sequences, ids