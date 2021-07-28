import os, re, tempfile

from .. import database
from ..objects import Hit

def calc_full(sequences, ids, db, FASTA36_EXECUTABLE):
    """
    Start function that calls all needed function for a full FASTA36 search.

    Args:
        sequences: A list containing all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        db: A string for which reference database to use
        FASTA36_EXECUTABLE: A string with the path to the fasta36 executable

    Returns:
        hits_list: A list with Hits objects
    """
    query_lengths = get_query_lengths(sequences, ids)
    hits_list = get_hits_values(sequences, ids, db, FASTA36_EXECUTABLE, query_lengths)
    set_alignments(hits_list)
    set_recalculated_ident(hits_list)
    sorted_list = sorted(hits_list, key = lambda x: float(x.e_value))

    return hits_list, sorted_list



def get_query_lengths(sequences, ids):
    """
    
    Args:
        sequences: A list containing all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file

    Returns:
        query_lengths: A dictionary with the length of each sequence as value
    """
    query_lengths = {}
    for (seq, i) in zip(sequences, ids):
        i = i.replace('>', '')
        query_lengths[i] = len(seq)
    return query_lengths



def get_hits_values(sequences, ids, db, FASTA36_EXECUTABLE, query_lengths):
    """
    Excecutes fasta and parses the response for results

    Args:
        sequences: A list containing all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        db: A string for which reference database to use 
        FASTA36_EXECUTABLE: A string with the path to the fasta36 executable
        query_lengths: A dictionary with the length of each sequence as value

    Returns:
        hits_list: A list with Hits objects
    """
    data = database.get_db(db)
    db = database.database_loaded[db]
    hits_list = []

    for (seq, id) in zip(sequences, ids):
        tmp_file = save_seq_to_tmpfile(seq, id)
        fasta_res = get_fasta_response(tmp_file, data, FASTA36_EXECUTABLE)

        for query in fasta_res.split(">>>")[1:]:
            query_id = query.split()[0]
            for hit in query.split(">>")[1:]:
                if ">--" in hit:
                    hit = hit.split(">--")[0]
                hit_id = hit.split('\n')[0].split()[0]
                info = hit.split("\n\n")[0]
                alignment = hit.replace(info, '')
                bits, e_value, ident, similar, overlap, query_range, hit_range = re.search(r'bits: (\d+\.\d).+:\s+(.+)\n.+;\s+(\d+.\d).+\((\d+\.\d).+in (\d+).+\((\d+\-\d+):(\d+\-\d+)', hit).groups()
                query_seqs, hit_seqs, midlines = [], [], []
                for line in alignment.split('\n'):
                    if line.startswith(query_id[:12]):
                        query_seqs.append(line[20:])
                    if line.startswith(hit_id[:12]):
                        hit_seqs.append(line[20:])
                    if line.strip().startswith((':', '.')):
                        midlines.append(line[20:])
                query_seq = ''.join(query_seqs)
                midline = ''.join(midlines) + ' '
                hit_seq = ''.join(hit_seqs)

                midline_start = len(midline) - len(midline.lstrip(' '))
                midline_end = len(midline) - len(midline.rstrip(' '))
                if midline_end != 0:
                    midline_end - 1

                new_query_seq = ""
                new_midline = ""
                new_hit_seq = ""
                for q, m, h in zip(query_seq[midline_start:-midline_end], midline[midline_start:-midline_end], hit_seq[midline_start:-midline_end]):
                    if q != ' ' and h != ' ':
                        new_query_seq += q
                        new_midline += m
                        new_hit_seq += h
                
                subject_length = len(db[hit_id]["Sequence"])
                hits_list.append(Hit.Hit(id, "", new_query_seq, len(seq), query_range.split('-')[0], query_range.split('-')[1], hit_id, new_hit_seq, subject_length, hit_range.split('-')[0], hit_range.split('-')[1],
                                        new_midline, "", "", bits, e_value, ident, similar, overlap, 0.0))

    return hits_list


def get_fasta_response(tmp_file, data, FASTA36_EXECUTABLE):
    """
    Performs a FASTA36 and retrieves the output.

    Args:
        tmp_file: A tempfile(path) to use for FASTA36
        data: A string with the location to the reference database
        FASTA36_EXECUTABLE: A string with the path to the fasta36 executable 

    Returns:
        fasta_res: A string with the output from FASTA36
    """
    with open(tmp_file.name, "r") as query_file:
        commandline = FASTA36_EXECUTABLE+"  "+query_file.name+" -C 1000 "+data
        fasta_pipe = os.popen(commandline)
        fasta_res = fasta_pipe.read()

    return fasta_res



def save_seq_to_tmpfile(sequence, id):
    """
    Saves the sequences and the id's to a temporaryfile. This file will be used for
    FASTA36

    Args:
        sequences: A list containing all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file

    Returns:
        tmp: File path to the newly created file
    """
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(">query\n")
        f.write(sequence)

    return tmp

def set_alignments(hits_list):
    """
    Creates the alignment and sets it to the Hits object
    If the query sequence is longer than 70aa this function will format the alignment for better visualisation

    Args:
        hits_list: A list with Hits objects

    """
    for hit in hits_list:
        max_length = max(len(str(hit.get_query_start())), len(str(hit.get_hit_start())))
        query_start = str(hit.get_query_start()).ljust(max_length+1)
        midline_start = " ".ljust(max_length+1)
        hit_start = str(hit.get_hit_start()).ljust(max_length+1)

        if len(hit.get_query_seq()) > 80:
            chunks_query = [hit.get_query_seq()[i:i+70] for i in range(0, len(hit.get_query_seq()), 70)]
            chunks_midline = [hit.get_midline()[i:i+70] for i in range(0, len(hit.get_midline()), 70)]
            chunks_hit = [hit.get_hit_seq()[i:i+70] for i in range(0, len(hit.get_hit_seq()), 70)]
            splitted_alignment = ""
            for q, m, h in zip(chunks_query, chunks_midline, chunks_hit):
                splitted_alignment += q + '\n'
                splitted_alignment += m + '\n'
                splitted_alignment += h + '\n'
            splitted = splitted_alignment.strip().split('\n')
            formatted_alignment = ""
            formatted_alignment += query_start+splitted[0] + '\n'
            formatted_alignment += midline_start+splitted[1] + '\n'
            formatted_alignment += hit_start+splitted[2] + '\n\n'
            
            splitted[-3] = splitted[-3] + ' ' + str(hit.get_query_end())
            splitted[-1] = splitted[-1] + ' ' + str(hit.get_hit_end())

            counter = 1
            for line in splitted[3:]:
                formatted_alignment += midline_start + line + '\n'
                if counter % 3 == 0:
                    formatted_alignment += '\n'
                counter += 1

            hit.set_formatted_alignment(formatted_alignment)

        alignment = (query_start+hit.get_query_seq()+" "+str(hit.get_query_end())+"\n"+
                    midline_start+hit.get_midline()+"\n"+
                    hit_start+hit.get_hit_seq()+" "+str(hit.get_hit_end())) 
        hit.set_alignment(alignment)     


def set_recalculated_ident(hits_list):
    for hit in hits_list:
        overlap = int(hit.get_overlap())
        identity = float(hit.get_identity())
        if overlap < 80:
            recalc_ident = (identity * overlap) / 80.0
            hit.set_recalculated_ident(round(recalc_ident, 2))
        else:
            hit.set_recalculated_ident("na")