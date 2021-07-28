import re
from collections import Counter

from celiac import celiac_database

def create_all_info(orf_list, options):
    intro = []
    intro.append("Allermatch TM command line tool\n  version 0.1 2020\n")
    intro.append("Used settings\n"+
                "Transcription table:   %s\n" % options["table"]+
                "Minimum orf length:    %s\n" % options["length"]+
                "Minimum exact word:    %s\n" % options["word_length"]+
                "Sliding window cutoff: %s\n" % options["window_cutoff"]+
                "Celiac database(s) used:  %s\n" % get_celiac_db_name(options["celiac_database"]))
    intro.append("Query:                %s"   % options["file_name"])
    intro.append("Inputfile type:       %s\n" % options["file_input_type"])
    if options["file_input_type"] == "Single protein sequences" or options["file_input_type"] == "Multiple protein sequences":
        intro.append("%s contains %s protein sequences" % (options["file_name"], len(orf_list)))
    if options["file_input_type"] == "Single DNA sequence" or options["file_input_type"] == "Multiple DNA sequences":
        query_occurences = Counter(sublist[7] for sublist in orf_list)
        intro.append("ORFs found:")
        for query in query_occurences:
            intro.append(query+": "+str(query_occurences[query]))
    intro.append('\n')

    return intro


def create_allergen_intro(orf_list, options):
    intro = []
    intro.append("Allermatch TM command line tool\n  version 0.1 2020\n")
    intro.append("Used settings\n"+
                "Transcription table:   %s\n" % options["table"]+
                "Minimum orf length:    %s\n" % options["length"]+
                "Minimum exact word:    %s\n" % options["word_length"]+
                "Sliding window cutoff: %s\n" % options["window_cutoff"])
    intro.append("Query:                %s"   % options["file_name"])
    intro.append("Inputfile type:       %s\n" % options["file_input_type"])
    if options["file_input_type"] == "Single protein sequences" or options["file_input_type"] == "Multiple protein sequences":
        intro.append("%s contains %s protein sequences" % (options["file_name"], len(orf_list)))
    if options["file_input_type"] == "Single DNA sequence" or options["file_input_type"] == "Multiple DNA sequences":
        query_occurences = Counter(sublist[7] for sublist in orf_list)
        intro.append("ORFs found:")
        for query in query_occurences:
            intro.append(query+": "+str(query_occurences[query]))
    intro.append('\n')

    return intro


def create_celiac_intro(orf_list, options):
    intro = []
    intro.append("Allermatch TM command line tool\n  version 0.1 2020\n")
    intro.append("Used settings\n"+
                "Transcription table:      %s\n" % options["table"]+
                "Minimum orf length:       %s\n" % options["length"]+
                "Celiac database(s) used:  %s\n" % get_celiac_db_name(options["celiac_database"]))
    intro.append("Query:                %s"   % options["file_name"])
    intro.append("Inputfile type:       %s\n" % options["file_input_type"])
    if options["file_input_type"] == "Single protein sequences" or options["file_input_type"] == "Multiple protein sequences":
        intro.append("%s contains %s protein sequences" % (options["file_name"], len(orf_list)))
    if options["file_input_type"] == "Single DNA sequence" or options["file_input_type"] == "Multiple DNA sequences":
        query_occurences = Counter(sublist[7] for sublist in orf_list)
        intro.append("ORFs found:")
        for query in query_occurences:
            intro.append(query+": "+str(query_occurences[query]))
    intro.append('\n')

    return intro


def create_toxin_intro(orf_list, options):
    intro = []
    intro.append("Allermatch TM command line tool\n  version 0.1 2020\n")
    intro.append("Used settings\n"+
                "Transcription table:   %s\n" % options["table"]+
                "Minimum orf length:    %s\n" % options["length"])
    intro.append("Query:                %s"   % options["file_name"])
    intro.append("Inputfile type:       %s\n" % options["file_input_type"])
    if options["file_input_type"] == "Single protein sequences" or options["file_input_type"] == "Multiple protein sequences":
        intro.append("%s contains %s protein sequences" % (options["file_name"], len(orf_list)))
    if options["file_input_type"] == "Single DNA sequence" or options["file_input_type"] == "Multiple DNA sequences":
        query_occurences = Counter(sublist[7] for sublist in orf_list)
        intro.append("ORFs found:")
        for query in query_occurences:
            intro.append(query+": "+str(query_occurences[query]))
    intro.append('\n')

    return intro


def create_top_allergens(info, results_full):
    info.append("Top 100 full FASTA allergen hits(on e-value):\n")
    for hit, i in zip(results_full[:100], range(1,101)):
        info.append("%s. ORF: %s | ORF length: %s | Hit ID: %s | Hit length: %s \n   E-Value: %s | Overlap: %s | Identity: %s | Recalculated identity: %s\n"
                    % (i, hit.get_query_id(), hit.get_query_length(), hit.get_hit_id(), hit.get_hit_length(), hit.get_e_value(), hit.get_overlap(), hit.get_identity(), hit.get_recalculated_ident()))
        alignment = '\t'+hit.get_alignment()
        if hit.get_formatted_alignment():
            alignment = '\t'+hit.get_formatted_alignment()
        alignment = alignment.replace('\n', '\n\t')
        info.append(alignment+'\n')
    info.append("\nEnd of top 100\n-----------------------------------------------\n")

    return info

def create_allergen_info(info, orf_list, unique_hits, results_window, alignments_window, results_word, alignments_word):
    for hit in unique_hits:
        for orf in orf_list:
            if hit == orf[0]:
                info.append(">>%s | %saa | Strand: %s | Frame: %s | Range: (%s:%s)\n" % (orf[0], orf[2], orf[3], orf[4], orf[5], orf[6]))
        if hit in [rw[0] for rw in results_window]:
            info.append("Sliding window results:\n")
        for rw in results_window:
            if hit == rw[0]:
                info.append(">- %s | %s | %s | %s" % (rw[1], rw[7], rw[8], rw[9]))
                info.append("   Best hit identity: %s | Number of sliding window(s): %s, Hit perc: %s\n" % (rw[2], rw[3], rw[4]))
                for al in alignments_window:
                    if al.get_query_id() == hit and al.get_hit_id() == rw[1]:
                        info.append("\n\tAlignment containing %s window(s):" % str(al.get_no_slices()))
                        for key in al.get_window_identities():
                            info.append("\t(%s) %s%% identity" % (key, al.get_window_identities()[key]))
                        alignment = '\t'+al.get_alignment()
                        if al.get_formatted_alignment():
                            alignment = '\t'+al.get_formatted_alignment()
                        alignment = alignment.replace('\n', '\n\t')
                        info.append(alignment+'\n')
        if hit in [rw[0] for rw in results_word]:
            info.append("Exact word results:\n")
        for rw in results_word:
            if hit == rw[0]:
                info.append(">- %s | %s | %s | %s" % (rw[1], rw[5], rw[3], rw[6]))
                info.append("   Number of exact word(s): %s | Hit perc: %s\n" %(rw[2], rw[4]))
                for al in alignments_word[(hit, rw[1])]:
                    al = '\t'+al
                    al = al.replace('\n', '\n\t') 
                    info.append(al+"\n") 
        info.append('\n')
    return info


def create_top_celiac(info, sorted_celiac):
    db = celiac_database.import_database("")
    info.append("Top 100 full FASTA toxin hits(on e-value):\n")
    for hit, i in zip(sorted_celiac, range(1,101)):
        info.append("%s. ID: %s | ID length: %s | Hit ID: %s | Hit length: %s \n   Database: %s | Source: %s | Source_id(s): %s\n   E-Value: %s | Overlap: %s | Identity: %s | Similarity: %s\n"
                    % (i, hit.get_query_id(), hit.get_query_length(), db[hit.get_hit_id()]["Name"], hit.get_hit_length(),
                    db[hit.get_hit_id()]["Database"], db[hit.get_hit_id()]["Source"], db[hit.get_hit_id()]["Source_id"],
                    hit.get_e_value(), hit.get_overlap(), hit.get_identity(), hit.get_similar()))
        alignment = '\t'+hit.get_alignment()
        alignment = alignment.replace('\n', '\n\t')
        info.append(alignment+'\n')
    info.append("\nEnd of top 100\n-----------------------------------------------\n")
    
    return info

def create_info_celiac(info, unique_hits_celiac, results_identical, alignments_identical, results_motif, total_hits):
    for hit in unique_hits_celiac:
        info.append(">>%s \n" % hit)
        info.append("Identical Celiac epitope results:\n")
        for ri in results_identical:
            if ri[0] == hit:
                info.append(">- %s | %s " % (ri[1], ri[3]))
                info.append("   Number of hits: %s | Database: %s | %s_id(s): %s\n" % (ri[2], ri[4], ri[5], ri[6]))
                for al in alignments_identical[(hit, ri[7])]:
                    al = '\t'+al
                    al = al.replace('\n', '\n\t') 
                    info.append(al+"\n") 
        info.append("Motif results:\n")
        for rm in results_motif:
            if rm[0] == hit:
                info.append(">- %s | Start: %s | End: %s | Occurence: %s(%s/%s)\n" % (rm[1], rm[2], rm[3], rm[4], rm[5], total_hits))
                al = '\t'+rm[7]
                al = al.replace('\n', '\n\t')
                info.append(al+'\n')
    
    return info

def create_top_toxins(info, sorted_toxins):
    info.append("Top 100 full FASTA celiac hits(on e-value):\n")
    for hit, i in zip(sorted_toxins[:100], range(1,101)):
        info.append("%s. ORF: %s | ORF length: %s | Hit ID: %s | Hit length: %s \n   E-Value: %s | Overlap: %s | Identity: %s\n"
                    % (i, hit.get_query_id(), hit.get_query_length(), hit.get_hit_id(), hit.get_hit_length(), hit.get_e_value(), hit.get_overlap(), hit.get_identity()))
        alignment = '\t'+hit.get_alignment()
        if hit.get_formatted_alignment():
            alignment = '\t'+hit.get_formatted_alignment()
        alignment = alignment.replace('\n', '\n\t')
        info.append(alignment+'\n')
    info.append("\nEnd of top 100\n-----------------------------------------------\n")

    return info


def get_celiac_db_name(db_nr):
    if db_nr == 0:
        return "Sollid + ProPrepper + AllergenOnline"
    elif db_nr == 1:
        return "Sollid"
    elif db_nr == 2:
        return "ProPepper"
    elif db_nr == 3:
        return "AllergenOnline"
    elif db_nr == 4:
        return "Sollid + ProPepper"
    elif db_nr == 5:
        return "Sollid + AllergenOnline"
    elif db_nr == 6:
        return "AllergenOnline + ProPepper"
            