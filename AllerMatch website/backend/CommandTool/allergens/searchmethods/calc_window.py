import os, tempfile, re
from collections import defaultdict

from .. import database
from ..objects import Windows, Hit, Alignments

def calc_window(sequences, ids, db, cut_off, GLSEARCH36_EXECUTABLE):
    """
    Start function that calls all needed functions for a sliding window search.

    Args:
        sequences: A list containing all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        db: A string for which reference database to use
        cut_off: An integer with the minimum sliding window percent to be considered a hit

    Returns:
        tsv_values: A list with results to be shown in the tsv-file
        alignments_list: A list with Alignments objects
    """
    hits_list, windows_per_query = get_windows_values(sequences, ids, db, cut_off, GLSEARCH36_EXECUTABLE)
    if len(hits_list) >= 1:
        global_values = get_global_values(sequences, ids, hits_list, db, GLSEARCH36_EXECUTABLE)
        tsv_values = get_tsv_values(hits_list, windows_per_query, global_values, db)
        alignments_list = create_alignments(hits_list)

        while merge_alignments(alignments_list) != None:
            merged_alignments = merge_alignments(alignments_list)
            if merged_alignments != None:
                alignments_list = merged_alignments

        set_alignments(alignments_list)

        return tsv_values, alignments_list, hits_list
    else:
        return [], [], []


def calc_window_pool(pool_input):
    """
    Function used for pooling, this will start calc_window().

    Args:
        pool_input: A list containing the values needed for calc_window
                    (sequences, ids, db, cut_off, GLSEARCH36_EXECUTABLE)

    Returns:
        tsv_values: A list with results to be shown in the tsv-file
        alignments_list: A list with Alignments objects
    """
    sequences, ids, db, cut_off, GLSEARCH36_EXECUTABLE = pool_input[0], pool_input[1], pool_input[2], pool_input[3], pool_input[4]
    tsv_values, alignments_list, hits_list = calc_window(sequences, ids, db, cut_off, GLSEARCH36_EXECUTABLE)

    return tsv_values, alignments_list, hits_list

def get_windows_values(sequences, ids, db, cut_off, GLSEARCH36_EXECUTABLE):
    """
    Function that calls other script to execute the FASTA36 search.
    This will parse the output and retrieves hits from the FASTA36 searches.

    Args:
        sequences: A list containing all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        db: A string for which reference database to use
        cut_off: An integer with the minimum sliding window percent to be considered a hit

    Returns:
        hits_list: A list with Hits objects in it
        windows_per_query: A dictionary containing the windows each query has as value
    """
    data = database.get_db(db)
    db = database.database_loaded[db]
    hits_list = []
    windows_per_query = {}

    for (seq, id) in zip(sequences, ids):
        windows_objects, no_windows = create_windows(seq, id)
        windows_per_query[id] = no_windows
        for window in windows_objects:
            fasta_res = get_glsearch_response(window.to_tempfile(), data, GLSEARCH36_EXECUTABLE)
            for query in fasta_res.split(">>>")[1:]:
                for hit in query.split(">>")[1:]:
                    if ">--" in hit:
                        hit = hit.split(">--")[0]
                    
                    hit_id = hit.split('\n')[0].split()[0]
                    bits, e_value, identity, similar, overlap, query_range, hit_range = re.search(r'bits: (\d+\.\d).+:\s+(.+)\n.+;\s+(\d+.\d).+\((\d+\.\d).+in (\d+).+\((\d+\-\d+):(\d+\-\d+)', hit).groups()
                    info = hit.split("\n\n")[0]
                    alignment = hit.replace(info, '')
                    identity = float(identity)
                    overlap = float(overlap)

                    if overlap < 80.0:
                        identity = (identity * overlap) / 80.0
                    
                    if identity > cut_off:
                        query_seqs, hit_seqs, midlines = [], [], []
                        for line in alignment.split('\n'):
                            if line.startswith('query'):
                                query_seqs.append(line[20:])
                            if line.startswith(hit_id):
                                hit_seqs.append(line[20:])
                            if line.strip().startswith((':', '.')):
                                midlines.append(line[20:])
                        
                        query_seq = ''.join(query_seqs)
                        midline = ''.join(midlines)+' '*20
                        hit_seq = ''.join(hit_seqs)


                        new_query_seq = ""
                        new_midline = ""
                        new_hit_seq = ""
                        for q, m, h in zip(query_seq, midline, hit_seq):
                            if q != ' ' and h != ' ':
                                new_query_seq += q
                                new_midline += m
                                new_hit_seq += h
                        
                        subject_length = len(db[hit_id]["Sequence"])
                        query_length = len(seq)
                        hits_list.append(Hit.Hit(window.get_query_id(), window.get_query_window(), new_query_seq, query_length, window.get_query_window().split("_win")[1].split(':')[0], window.get_query_window().split("_win")[1].split(':')[1],
                                                hit_id, new_hit_seq, subject_length, hit_range.split('-')[0], hit_range.split('-')[1], new_midline, "na", "", bits, e_value, identity, similar, overlap, 0.0))

    return hits_list, windows_per_query

def create_windows(seq, id):
    """
    Funtion that saves the windows to Windows objects

    Args:
        seq: A string containing a query-sequence
        id: A string containing the query-id

    Returns:
        windows_objects: A list containing Windows objects
        window_count: A integer for the amount of 80aa sliding windows there are in the sequence
    """
    windows = [seq[i:i+80] for i in range(len(seq)-79)]
    windows_objects = []
    window_counter = 1

    if windows:
        for w in windows:
            if id.startswith(">"):
                windows_objects.append(Windows.Windows(id, id+"_win"+str(window_counter)+":"+str(window_counter+80),w))
            else:
                windows_objects.append(Windows.Windows(id, ">"+id+"_win"+str(window_counter)+":"+str(window_counter+80),w))
            window_counter += 1
    else:
        if id.startswith('>'):
            windows_objects.append(Windows.Windows(id, id+"_win1:"+str(len(seq)), seq))
        else:
            windows_objects.append(Windows.Windows(id, '>'+id+"_win1:"+str(len(seq)), seq))
        window_counter += 1

    return windows_objects, window_counter - 1

def get_glsearch_response(tmp_file, data, GLSEARCH36_EXECUTABLE, settings=" -C 1000 "):
    """
    Performs a GLSEARCH36 and retrieves the output.

    Args:
        tmp_file: A tempfile(path) to use for FASTA36
        data: A string with the location to the reference database
        setting: A string for adjustments in the search

    Returns:
        fasta_res: A string with the output from FASTA36
    """
    with open(tmp_file.name, "r") as query_file:
        commandline = GLSEARCH36_EXECUTABLE+" "+query_file.name+settings+data
        fasta_pipe = os.popen(commandline)
        fasta_res = fasta_pipe.read()

    return fasta_res


def get_global_glsearch_response(tmp_file, data, GLSEARCH36_EXECUTABLE, settings=" -C 1000 "):
    """
    Performs a GLSEARCH36 and retrieves the output. #TODO change pydoc

    Args:
        tmp_file: A tempfile(path) to use for FASTA36
        data: A string with the location to the reference database
        setting: A string for adjustments in the search

    Returns:
        fasta_res: A string with the output from FASTA36
    """
    with open(tmp_file.name, "r") as query_file:
        commandline = GLSEARCH36_EXECUTABLE+" "+query_file.name+settings+data.name
        fasta_pipe = os.popen(commandline)
        fasta_res = fasta_pipe.read()

    return fasta_res


def get_global_values(sequences, ids, hits_list, db, GLSEARCH36_EXECUTABLE):
    """
    Perfoms a GLSEARCH36 of the whole sequence, and collects the global identity and length

    Args:
        sequences: A list containing the query-sequences
        ids: A list containing the query-ids
        db: A string for which reference database to use 

    Returns:
        global_values: A dicitonary containing the global identity and length
    """
    data = database.get_db(db)
    db = database.database_loaded[db]
    global_values = {}

    database_ids = []
    database_sequences = []
    hit_ids = set()
    for hit in hits_list:
        hit_ids.add(hit.get_hit_id())
    for database_id in hit_ids:
        database_ids.append(db[database_id]["Allergen id"])
        database_sequences.append(db[database_id]["Sequence"])

    global_tmpfile = save_global_to_tmpfile(sequences, ids)
    small_database = save_global_to_tmpfile(database_sequences, database_ids)
    fasta_res = get_global_glsearch_response(global_tmpfile, small_database, GLSEARCH36_EXECUTABLE)

    for query in fasta_res.split(">>>")[1:]:
        query_id = query.split()[0]
        for hit in query.split(">>")[1:]:
            if ">--" in hit:
                hit = hit.split(">--")[0]
            identity, idlen = re.search(r' ([0-9\.]+)\% *identity \(.+?\) in (\d*) aa overlap',
                                        hit).groups()
            identity = float(identity)
            idlen = int(idlen)
            hit_id = hit.split('\n')[0].split()[0]

            global_values[(query_id, hit_id)] = (identity, idlen)
    
    return global_values

def save_global_to_tmpfile(sequences, ids):
    """
    Saves the whole query-sequences to a tempfile, this will be used for a global GLSEARCH36

    Args:
        sequences: A list containing the query-sequences
        ids: A list containing the query-ids

    Returns:
        tmp: A tempfile(path) with the whole sequences
    """
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        for (seq, i) in zip (sequences, ids):
            if i.startswith(">"):
                f.write(i+"\n")
            else:
                f.write(">"+i+"\n")
            f.write(seq+"\n")
    return tmp


def get_tsv_values(hits_list, windows_per_query, global_values, db):
    """
    Retrieves the values needed to be shown in the tsv-file

    Args:
        hits_list: A list containg Hits objects
        windows_per_query: A dictionary containing the windows each query has as value 
        global_values: A dicitonary containing the global identity and length
        db: A string for which reference database to use 

    Returns:
        results: A list with results to be shown in the tsv-file
    """
    db = database.database_loaded[db]
    results = []
    identities_per_query = defaultdict(list)
    for hit in hits_list:
        identities_per_query[hit.get_query_id(), hit.get_hit_id()].append(hit.get_identity())
    
    for query in identities_per_query:
        query_id = query[0]
        hit_id = query[1]
        best_hit_perc = max(identities_per_query[query])
        no_hits = len(identities_per_query[query])
        perc_hits = round(float(no_hits)/windows_per_query[query_id] * 100, 2)
        acc_id = db[hit_id]["Accession id"]
        spec_name = db[hit_id]["Species name"]
        description = db[hit_id]["Remark"]
        seq_db = db[hit_id]["Database Name"]
        hyperlink = db[hit_id]["Hyperlink"]
        glob_iden = global_values[(query_id.replace('>', ''), hit_id)][0]
        glob_len = global_values[(query_id.replace('>', ''), hit_id)][1]
        results.append((query_id, hit_id, best_hit_perc, no_hits, perc_hits, glob_iden, glob_len, acc_id, spec_name, description, seq_db, hyperlink))
    
    return results


def create_alignments(hits_list):
    """
    Creates a list with Alignment objects

    Args:
        hits_list: A list containing Hits objects 

    Returns:
        alignments_list: A list with Alignments objects
    """
    alignments_list = []
    for hit in hits_list: 
        ranges = str(hit.get_query_start())+':'+str(hit.get_query_end())+'-'+str(hit.get_hit_start())+':'+str(hit.get_hit_end())    

        alignments_list.append(Alignments.Alignments(hit.get_query_id(), hit.get_query_window(), hit.get_query_seq(), hit.get_query_start(),
                                hit.get_query_end(), hit.get_hit_id(), hit.get_hit_seq(), hit.get_hit_start(), hit.get_hit_end(), hit.get_midline(),
                                "", "", 1, {ranges: hit.get_identity()}))
    return alignments_list

def merge_alignments(hits_list):
    """
    Merges the alignments from hits_list. Based on identical query_seq, hit_id and hit_end should be 1 apart 
    This function is called multiple times untill no merge can be applied

    Args:
        hits_list: A list containing Hits objects 

    Returns:
        hits_list: A list containing Hits objects
    """
    for hit in hits_list:
        for hit2 in hits_list:
            if hit.get_query_id() == hit2.get_query_id() and hit.get_hit_id() == hit2.get_hit_id() and int(hit.get_query_end()) == int(hit2.get_query_end()) - 1:
                length = len(hit2.get_query_seq()[:-1])
                length_hit = len(hit2.get_hit_seq()[:-1])
                if hit.get_query_seq()[-length:] == hit2.get_query_seq()[:-1] and hit.get_hit_seq()[-length_hit:] == hit2.get_hit_seq()[:-1]:
                    new_query_window = hit.get_query_window().split(":")[0] + ":" + hit2.get_query_window().split(":")[1]
                    new_dict = {**hit.get_window_identities(), **hit2.get_window_identities()}
                    
                    new_query_seq = hit.get_query_seq() + hit2.get_query_seq()[-1:]
                    new_hit_seq = hit.get_hit_seq() + hit2.get_hit_seq()[-1:]
                    new_midline = hit.get_midline() + hit2.get_midline()[-1:]

                    new_alignment = Alignments.Alignments(hit.get_query_id(), new_query_window, new_query_seq, hit.get_query_start(),
                                                        hit2.get_query_end(), hit.get_hit_id(), new_hit_seq, hit.get_hit_start(), hit2.get_hit_end(),
                                                        new_midline, "", "", hit.get_no_slices()+1, new_dict)

                    for i in range(len(hits_list)-1):
                        if hits_list[i] == hit:
                            hits_list.insert(i, new_alignment)
                            hits_list.remove(hit)
                            hits_list.remove(hit2)

                    return hits_list

def set_alignments(hits_list):
    """
    Creates the alignments from Hits values and sets the alignment to the object
    If the query sequence is longer than 70aa this function will format the alignment for better visualisation

    Args:
        hits_list: A list containing Hits objects
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