import os, tempfile, re
from collections import defaultdict

from toxins import tox_database
from toxins.objects import Hit

LOC = os.getcwd()+"/CommandTool"


def get_similar_matches(ids, sequences, options, FASTA36_EXECUTABLE):
    similar_matches = []
    data = tox_database.get_db(options["peptides_removed"])
    db = tox_database.database_loaded[options["peptides_removed"]]
    for (seq, id) in zip(sequences, ids):
        tmp_file = save_seq_to_tmpfile(seq,id)
        fasta_res = get_fasta_response(tmp_file,data, FASTA36_EXECUTABLE)
        
        for query in fasta_res.split(">>>")[1:]:
            for hit in query.split(">>")[1:]:
                if ">--" in hit:
                    hit = hit.split(">--")[0]
                hit_id = hit.split('\n')[0].split()[0]
                info = hit.split("\n\n")[0]
                alignment = hit.replace(info, '')
                bits, e_value, ident, similar, overlap, query_range, hit_range = re.search(r'bits: (\d+\.\d).+:\s+(.+)\n.+;\s+(\d+.\d).+\((\d+\.\d).+in (\d+).+\((\d+\-\d+):(\d+\-\d+)', hit).groups()
                query_seqs, hit_seqs, midlines = [], [], []
                for line in alignment.split('\n'):
                    if line.startswith("query"):
                        query_seqs.append(line[20:])
                    if line.startswith(hit_id[:12]):
                        hit_seqs.append(line[20:])
                    if line.strip().startswith((':', '.')):
                        midlines.append(line[20:])
                query_seq = ''.join(query_seqs) + ' '
                midline = ''.join(midlines) + ' '
                hit_seq = ''.join(hit_seqs) + ' '

                midline_start = len(midline) - len(midline.lstrip(' '))
                midline_end = len(midline) - len(midline.rstrip(' '))
                
                new_query_seq = ""
                new_midline = ""
                new_hit_seq = ""
                for q, m, h in zip(query_seq[midline_start:-midline_end], midline[midline_start:-midline_end], hit_seq[midline_start:-midline_end]):
                    if q != ' ' and h != ' ':
                        new_query_seq += q
                        new_midline += m
                        new_hit_seq += h
                
                similar_matches.append(Hit.Hit(id, new_query_seq, len(seq), query_range.split('-')[0], query_range.split('-')[1], 
                                                hit_id, new_hit_seq, db[hit_id]["Size mature protein"], hit_range.split('-')[0], hit_range.split('-')[1], new_midline, "", "", bits, e_value, ident, similar, overlap))

    set_alignments(similar_matches)
    
    return similar_matches

    
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

def set_alignment2(hits_list):
    alignments_per_hit = defaultdict(list)
    for hit in hits_list:
        max_length = max(len(str(hit.get_query_start())), len(str(hit.get_hit_start())))
        query_start = str(hit.get_query_start()).ljust(max_length+1)
        midline_start = ' '.ljust(max_length+1)
        hit_start = str(hit.get_hit_start()).ljust(max_length+1)

        alignment = (query_start+hit.get_query_seq()+" "+str(hit.get_query_end())+"\n"+
                    midline_start+hit.get_midline()+"\n"+
                    hit_start+hit.get_hit_seq()+" "+str(hit.get_hit_end()))
        
        hit.set_alignment(alignment)

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

