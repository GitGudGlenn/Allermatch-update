import exrex
import os, tempfile, re

from .. import celiac_database
from ..objects import EpitopeMatch, PerfectMatch
from collections import defaultdict

LOC = os.getcwd()+"/CommandTool"

GLSEARCH36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/glsearch36"
FASTS36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/fasts36"
FASTA36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/fasta36"


def get_perfect_matches(ids, sequences, db_nr):
    db_tmp_file = celiac_database.specify_database(db_nr)
    db = celiac_database.import_database(db_tmp_file.name)
    hits_list = []
    hits_per_query = defaultdict(list)
    for (id, seq) in zip(ids, sequences):
        for k in db:
            subject_seq = db[k]["Sequence"].upper()
            c = seq.count(subject_seq)
            if c == 1:
                hit_start = seq.find(subject_seq)
                hits_list.append(PerfectMatch.PerfectMatch(id, seq, hit_start+1, hit_start+len(subject_seq), db[k]["Epitope id"], 
                                                            subject_seq, 1, len(subject_seq), subject_seq, ':'*len(subject_seq)))
                hits_per_query[id, k].append(subject_seq)
            if c >= 2:
                start_indexes = find_all_indexes(seq, subject_seq)
                for hit_start in start_indexes:
                    hits_list.append(PerfectMatch.PerfectMatch(id, seq, hit_start+1, hit_start+len(subject_seq), db[k]["Epitope id"], 
                                                            subject_seq, 1, len(subject_seq), subject_seq, ':'*len(subject_seq)))
                    hits_per_query[id, k].append(subject_seq)

    alignments = set_alignment(hits_list)
    tsv_values = get_tsv_values(hits_list, hits_per_query)
    return tsv_values, alignments

def get_similar_matches(ids, sequences, db_nr):
    db = celiac_database.import_database("")
    similar_matches = []
    db_tmp_file = (celiac_database.specify_database(db_nr))
    query_tmp_file, query_ids, query_lengths = save_seqs_to_tmpfile(ids, sequences)
    fasta_res = get_fasta_response3(db_tmp_file, query_tmp_file)
    for query in fasta_res.split(">>>")[1:]:
        hit_id = query.split()[0]
        for hit in query.split(">>")[1:]:
            if ">--" in hit:
                hit = hit.split(">--")[0]
            query_id = hit.split('\n')[0].split()[0]
            info = hit.split("\n\n")[0]
            alignment = hit.replace(info, '')
            bits, e_value, ident, similar, overlap, hit_range, query_range = re.search(r'bits: (.+) E.+:\s+(.+)\n.+;\s+(\d+.\d).+\((\d+\.\d).+in (\d+).+\((\d+\-\d+):(\d+\-\d+)', hit).groups()
            ident = float(ident)
            query_seqs, hit_seqs, midlines = [], [], []
            for line in alignment.split('\n'):
                if line.startswith(query_id):
                    query_seqs.append(line[20:])
                if line.startswith(hit_id):
                    hit_seqs.append(line[20:])
                if line.strip().startswith((':', '.')):
                    midlines.append(line[20:])
            query_seq = ''.join(query_seqs)
            midline = ''.join(midlines)+ ' '
            hit_seq = ''.join(hit_seqs)

            midline_start = len(midline) - len(midline.lstrip(' '))
            midline_end = len(midline) - len(midline.rstrip(' '))
            if midline_end != 0:
                midline_end = midline_end - 1
            new_query_seq = ""
            new_midline = ""
            new_hit_seq = ""
            for q, m, h in zip(query_seq[midline_start:-midline_end], midline[midline_start:-midline_end], hit_seq[midline_start:-midline_end]):
                if q != ' ' and h != ' ':
                    new_query_seq += q
                    new_midline += m
                    new_hit_seq += h

            subject_length = len(db[hit_id]["Sequence"])
            full_query_id = query_ids[query_id]
            similar_matches.append(EpitopeMatch.EpitopeMatch(full_query_id, new_query_seq, query_lengths[full_query_id], query_range.split('-')[0], query_range.split('-')[1],
                                                                hit_id, new_hit_seq, subject_length, hit_range.split('-')[0], hit_range.split('-')[1], new_midline, "na", "", bits, e_value, ident, similar, overlap))

    set_alignment2(similar_matches)

    return similar_matches

def save_seqs_to_tmpfile(ids, sequences):
    tmp = tempfile.NamedTemporaryFile()
    query_lengths = {}
    query_ids = {}
    counter = 1
    with open(tmp.name, 'w') as f:
        for (id, seq) in zip(ids, sequences):
            f.write('>query'+str(counter)+'\n')
            f.write(seq+'\n')
            query_ids['query'+str(counter)] = id
            query_lengths[id] = len(seq)
            counter += 1
    
    return tmp, query_ids, query_lengths

def get_fasta_response3(db_tmp_file, query_tmp_file, settings=" -C 1000 "):
    """
    Performs a GLSEARCH36 and retrieves the output.

    Args:
        tmp_file: A tempfile(path) to use for FASTA36
        data: A string with the location to the reference database
        setting: A string for adjustments in the search

    Returns:
        fasta_res: A string with the output from FASTA36
    """
    commandline = FASTA36_EXECUTABLE+" "+db_tmp_file.name+settings+query_tmp_file.name
    fasta_pipe = os.popen(commandline)
    fasta_res = fasta_pipe.read()

    return fasta_res


def get_similar_matches2(ids, sequences, db_nr):
    db = celiac_database.import_database("")
    similar_matches = []
    db_tmp_file = (celiac_database.specify_database(db_nr))
    for (id, seq) in zip(ids, sequences):
        tmp_file = save_seq_to_tmpfile(seq, id)
        fasta_res = get_fasta_response(tmp_file, db_tmp_file.name)
        for query in fasta_res.split(">>>")[1:]:
            query_id = query.split()[0]
            for hit in query.split(">>")[1:]:
                if ">--" in hit:
                    hit = hit.split(">--")[0]
                hit_id = hit.split('\n')[0].split()[0]
                info = hit.split("\n\n")[0]
                alignment = hit.replace(info, '')
                bits, e_value, ident, similar, overlap, query_range, hit_range = re.search(r'bits: (\d+\.\d).+:\s+(.+)\n.+;\s+(\d+.\d).+\((\d+\.\d).+in (\d+).+\((\d+\-\d+):(\d+\-\d+)', hit).groups()
                ident = float(ident)
                query_seqs, hit_seqs, midlines = [], [], []
                for line in alignment.split('\n'):
                    if line.startswith(query_id):
                        query_seqs.append(line[20:])
                    if line.startswith(hit_id):
                        hit_seqs.append(line[20:])
                    if line.strip().startswith((':', '.')):
                        midlines.append(line[20:])
                query_seq = ''.join(query_seqs)
                midline = ''.join(midlines)+ ' '
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
                similar_matches.append(EpitopeMatch.EpitopeMatch(id, new_query_seq, len(seq), query_range.split('-')[0], query_range.split('-')[1],
                                                                    hit_id, new_hit_seq, subject_length, hit_range.split('-')[0], hit_range.split('-')[1], new_midline, "na", "", bits, e_value, ident, similar, overlap))
    
    sorted_list = sorted(similar_matches, key = lambda x: float(x.e_value))
    set_alignment2(sorted_list)

    return similar_matches


def get_motif_matches(ids, sequences):
    categorized_motifs, total_hits = categorize_motifs()
    results = []
    for (id, seq) in zip(ids, sequences):
        for m in (re.finditer("[EQ][LQFSE]P[YFAVQ]", seq)):
            start = m.start()
            end = m.end()
            motif = seq[start:end]
            risk_factor = categorized_motifs[motif][0]
            occurence_motifs = str(categorized_motifs[motif][1])
            occurence_perc = str(categorized_motifs[motif][2])
            alignment = create_motif_alignment(motif, start, end)

            results.append((id, motif, str(start), str(end), risk_factor, occurence_motifs, occurence_perc, alignment))

    return results, str(total_hits)


def categorize_motifs():
    db = celiac_database.import_database("")
    ss = ""
    for k in db:
        ss += db[k]["Sequence"]+'\n'
    total_hits = len(re.findall("(?=([EQ][LQFSE]P[YFAVQ]))", ss))
    all_motifs = exrex.generate("(?=([EQ][LQFSE]P[YFAVQ]))")
    categorized_motifs = {}

    for motif in all_motifs:
        categorized_motifs[motif] = (len(re.findall(motif, ss)), round(len(re.findall(motif, ss)) / total_hits * 100, 2))

    for k in categorized_motifs:
        if categorized_motifs[k][1] == 0.0:
            categorized_motifs[k] = ("Low", categorized_motifs[k][0], categorized_motifs[k][1])
        elif categorized_motifs[k][1] < 2.0:
            categorized_motifs[k] = ("Medium", categorized_motifs[k][0], categorized_motifs[k][1])
        else:
            categorized_motifs[k] = ("High", categorized_motifs[k][0], categorized_motifs[k][1])
    
    return categorized_motifs, total_hits
    
def create_motif_alignment(motif, start, end):
      length = len(str(start))
      query_start = str(start).ljust(length+1)
      midline_start = ' '.ljust(length+1)

      return (query_start+motif+' '+str(end)+'\n'+
            midline_start+':'*len(motif)+'\n'+
            midline_start+motif)
        


def find_all_indexes(hit_seq, word):
    """
    If a certain word has multiple hits in the same hit-sequence, this function get all the 
    indices.

    Args:
        hit_seq: A string containg the reference sequence
        word: A string with the word that has multiple hit in the reference sequence

    Returns:
        tsv_values: A list containing values to be shown in the tsv-file
    """
    l1 = []
    length = len(hit_seq)
    index = 0
    while index < length:
        i = hit_seq.find(word, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1


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
        if id.startswith('>'):
            f.write('>query\n')#TODO
        else:
            f.write('>query\n')
        f.write(sequence+'\n')
    
    return tmp


def get_fasta_response(tmp_file, data, settings=" -C 1000 "):
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
        commandline = FASTA36_EXECUTABLE+" "+query_file.name+settings+data.name
        fasta_pipe = os.popen(commandline)
        fasta_res = fasta_pipe.read()

    return fasta_res


def set_alignment(hits_list):
    alignments_per_hit = defaultdict(list)
    for hit in hits_list:
        max_length = max(len(str(hit.get_query_start())), len(str(hit.get_hit_start())))
        query_start = str(hit.get_query_start()).ljust(max_length+1)
        midline_start = ' '.ljust(max_length+1)
        hit_start = str(hit.get_hit_start()).ljust(max_length+1)

        alignment = (query_start+hit.get_match_seq()+" "+str(hit.get_query_end())+"\n"+
                    midline_start+hit.get_match_midline()+"\n"+
                    hit_start+hit.get_match_seq()+" "+str(hit.get_hit_end()))
        
        alignments_per_hit[(hit.get_query_id(), hit.get_hit_id())].append(alignment)
    
    return alignments_per_hit


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
    

def get_tsv_values(hits_list, hits_per_query):
    tsv_values = []
    db = celiac_database.import_database("")
    for hpq in hits_per_query:
        query_id = hpq[0]
        hit_id = hpq[1]
        hits = str(len(hits_per_query[hpq]))
        name = db[hit_id]["Name"]
        hladq = db[hit_id]["HLADQ"]
        datab = db[hit_id]["Database"]
        source = db[hit_id]["Source"]
        source_ids = db[hit_id]["Source_id"]
        if '-' in source_ids:
            source_ids = "na"

        tsv_values.append((query_id, name, hits, hladq, datab, source, source_ids, hit_id))
    return tsv_values
