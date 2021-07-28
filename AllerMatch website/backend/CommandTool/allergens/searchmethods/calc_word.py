import os, tempfile, re

from .. import database
from ..objects import Words
from collections import defaultdict


def calc_wordmatch(sequences, ids, db_loc, word_length):
    """
    Start function that calls all needed functions for a exact word match search.

    Args:
        sequences: A list contatining all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        db_loc: A string for which reference database to use
        word_length: An integer with the minimum exact word match to be considered a hit

    Returns:
        tsv_values: A list with results to be shown in the tsv-file
        alignments: A dictionary containing the alignments as values.
    """
    hits_list, words_per_query, db = get_word_hits(sequences, ids, db_loc, word_length)
    tsv_values = get_tsv_values(hits_list, words_per_query, db, word_length)
    
    while merge_hits(hits_list) != None:
        merged_hits = merge_hits(hits_list)
        if merged_hits != None:
            hits_list = merged_hits
    
    alignments = get_alignments(hits_list)
    
    return tsv_values, alignments


def calc_wordmatch_pool(pool_input):
    """
    Function used for pooling, this will start calc_wordmatch().

    Args:
        pool_input: A list containing the values needed for calc_wordmatch()
                    (sequences, ids, db_loc, word_length)

    Returns:
        tsv_values: A list with results to be shown in the tsv-file
        alignments: A dictionary containing the alignments as values.
    """
    sequences, ids, db_loc, word_length = pool_input[0], pool_input[1], pool_input[2], pool_input[3]
    tsv_values, alignments = calc_wordmatch(sequences, ids, db_loc, word_length)

    return tsv_values, alignments


def get_word_hits(sequences, ids, db_loc, word_length):
    """
    Function that looks for exact word matches between the query-seq and the reference db

    Args:
        sequences: A list contatining all the dna sequences from the fasta-file
        ids: A list containing all the id's from the fasta-file
        db_loc: A string for which reference database to use
        word_length: An integer with the minimum exact word match to be considered a hit

    Returns:
        hits_list: A list with Words objects
        words_per_query: A defaultdict containing the exact word match hits as values
        db: A dictionary with values from the reference database
    """
    db = database.database_loaded[db_loc]
    hits_list = []
    words_per_query = defaultdict(list)
    for (seq, i) in zip(sequences, ids):
        for pos in range(0, len(seq)-word_length+1):
            word = seq[pos:pos+word_length].lower()
            for k in db.keys():
                sq = db[k]['Sequence'].lower()
                c = sq.count(word)
                if c == 1:
                    words_per_query[(i, k)].append(word)
                    hit_start = sq.find(word)
                    hits_list.append(Words.Words(i, seq, pos, pos+word_length, k, sq, hit_start, hit_start+word_length, word, ':'*word_length))
                if c >= 2:
                    start_indexes = find_all_indexes(sq, word)
                    words_per_query[(i, k)].append(word)
                    for hit_start in start_indexes:
                        hits_list.append(Words.Words(i, seq, pos, pos+word_length, k, sq, hit_start, hit_start+word_length, word, ':'*word_length))

    return hits_list, words_per_query, db


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


def get_tsv_values(hits_list, words_per_query, db, word_length):
    """
    Function that retrieves the tsv-values from hits.

    Args:
        hits_list: A list with Words objects
        words_per_query: A defaultdict containing the exact word match hits as values
        db: A dictionary with values from the reference database
        word_length: An integer with the minimum exact word match to be considered a hit

    Returns:
        tsv_values: A list containing values to be shown in the tsv-file
    """
    tsv_values = []
    for w in words_per_query:
        query_id = w[0]
        hit_id = w[1]
        hits = len(words_per_query[w])
        for hit in hits_list:
            if hit.get_query_id() == query_id:
                query_seq = hit.get_query_seq()

        description =   db[hit_id]['Remark'] ##Remark
        perc_hit =   float(hits) / float(len(query_seq) - word_length + 1) * 100
        hyperlink = db[hit_id]["Hyperlink"]
        swissacc =  db[hit_id]["Accession id"]
        spec_name =  db[hit_id]['Species name']
        seq_db = db[hit_id]["Database Name"]
        seq_sr = db[hit_id]["Source db"]

        tsv_values.append((query_id, hit_id, hits, description, round(perc_hit, 2), swissacc, spec_name, seq_db, seq_sr, hyperlink))

    return tsv_values


def merge_hits(hits_list):
    """
    Merges the alignments from hits_list. Based on identical query_seq, hit_id and hit_end should be 1 apart 
    This function is called multiple times untill no merge can be applied

    Args:
        hits_list: A list with Words objects

    Returns:
        hits_list: A list with Words objects
    """
    for hit in hits_list:
        for hit2 in hits_list:
            if hit.get_query_id() == hit2.get_query_id() and hit.get_hit_id() == hit2.get_hit_id() and hit.get_query_end() == hit2.get_query_end() -1 and hit.get_hit_end() == hit2.get_hit_end() -1:
                new_match_seq = hit.get_match_seq() + hit2.get_match_seq()[-1:]

                new_word = Words.Words(hit.get_query_id(), hit.get_query_seq(), hit.get_query_start(), 
                            hit2.get_query_end(), hit.get_hit_id(), hit.get_hit_seq(), hit.get_hit_start(), 
                            hit2.get_hit_end(), new_match_seq, ':'*len(new_match_seq))
                
                for i in range(len(hits_list)-1):
                    if hits_list[i] == hit:
                        hits_list.insert(i, new_word)
                        hits_list.remove(hit)
                        hits_list.remove(hit2)

                return hits_list 

def get_alignments(hits_list):
    """
    Function that creates the alignments from the hits.

    Args:
        hits_list: A list with Words objects

    Returns:
        alignments_per_hit: A defaultdict containing the alignments as values
    """
    alignments_per_hit = defaultdict(list)
    for hit in hits_list:
        max_length = max(len(str(hit.get_query_start())), len(str(hit.get_hit_start())))
        query_start = str(hit.get_query_start()).ljust(max_length+1)
        midline_start = " ".ljust(max_length+1)
        hit_start = str(hit.get_hit_start()).ljust(max_length+1)

        alignment = (query_start+hit.get_match_seq()+" "+str(hit.get_query_end())+"\n"+
                    midline_start+hit.get_match_midline()+"\n"+
                    hit_start+hit.get_match_seq()+" "+str(hit.get_hit_end()))
        
        alignments_per_hit[(hit.get_query_id(), hit.get_hit_id())].append(alignment)
    
    return alignments_per_hit
