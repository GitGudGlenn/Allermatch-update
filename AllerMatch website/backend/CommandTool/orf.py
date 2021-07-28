from Bio import SeqIO
from Bio.Seq import Seq

record = SeqIO.read("/home/your/Documents/stage/sequences/GM037889.1.fasta", "fasta")
record2 = SeqIO.read("/home/your/Documents/stage/sequences/Wheat_blue_dwarf.fasta", "fasta")
table = 11
min_pro_len = 8

def find_orfs_with_nucl(seq, id, trans_table, min_protein_length):
    """
    Finds ORF(Open Reading Frames) from the input file

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
    seq_len = len(seq)
    orf_counter = 1
    for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
        for frame in range(3):
            sequence = str(nuc[frame:])
            trailing_n = len(sequence) % 3
            sequence = Seq(sequence + 'N' * (3 - trailing_n))
            trans = str(sequence.translate(trans_table))
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
                            answer.append((">ORF"+str(orf_counter), trans[aa_start+met_pos:aa_end], len(trans[aa_start+met_pos:aa_end]), strand, frame+1, start, end, id))
                            orf_counter += 1
                aa_start = aa_end + 1
    return answer

def find_orfs_with_trans(seqs, ids, trans_table, min_protein_length):
    answer = []
    orf_counter = 1
    for(seq,i) in zip(seqs, ids):
        seq_len = len(seq)
        for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
            for frame in range(3):
                trans = str(nuc[frame:].translate(trans_table))
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
                        answer.append((">ORF"+str(orf_counter), trans[aa_start:aa_end], len(trans[aa_start:aa_end]), strand, frame+1, start, end, id))
                        orf_counter += 1
                    aa_start = aa_end + 1
    return answer


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
                trans = str(sequence.translate(trans_table))
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
                        answer.append((">ORF"+str(orf_counter), trans[aa_start:aa_end].replace('X',''), len(trans[aa_start:aa_end]), strand, frame+1, start, end, id))
                        orf_counter += 1
                    aa_start = aa_end + 1
    return answer


def find_orfs_between_stops2(seqs, ids, trans_table, min_protein_length):
    answer = []
    orf_counter = 1
    for(seq,i) in zip(seqs, ids):
        seq_len = len(seq)
        for strand, nuc in [(+1, seq), (-1, seq.reverse_complement())]:
            for frame in range(3):
                trans = str(nuc[frame:].translate(trans_table))
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
                        answer.append((">ORF"+str(orf_counter), trans[aa_start:aa_end], len(trans[aa_start:aa_end]), strand, frame+1, start, end, id))
                        orf_counter += 1
                    aa_start = aa_end + 1
    return answer


orf_list = find_orfs_between_stops([record.seq], [record.id], table, min_pro_len)
orf_list1 = find_orfs_between_stops2([record.seq], [record.id], table, min_pro_len)

print(len(orf_list))
print(len(orf_list1))

for orf, orf1 in zip(orf_list, orf_list1):
    if orf[1] != orf1[1]:
        print(orf[1])
        print(orf1[1])
        print("+++++")






# orf_list1 = find_orfs_with_nucl(record.seq, record.id, table, min_pro_len)


# orf_list = find_orfs_with_trans([record.seq, record2.seq],[record.id, record2.id], table, min_pro_len)


# for orf in orf_list1[:2]:
#     print(orf[0], orf[2], orf[3], orf[4], orf[5])
#     print(orf[1])

# for orf in orf_list[:2]:
#     print(orf[0], orf[2], orf[3], orf[4], orf[5])
#     print(orf[1])

# print(len(orf_list1))
# print(len(orf_list))