import csv

from celiac import celiac_database
from toxins import tox_database

def save_orf_file(orf_list, input_file, timestr, search_type):
    """
    Saves the found ORFs to a tsv file

    Args:
        orf_list: A list containing information about the ORFs
        input_file: A string with name of the file that is used as query
        timestr: A string of the current time
    """
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/ORFs.tsv", "w") as output_file:
        tsv_output = csv.writer(output_file, delimiter="\t")
        tsv_output.writerow(["ORF", "Sequence", "Length", "Strand", "Frame", "Start", "End"])
        for result in orf_list:
            tsv_output.writerow(result)


def save_window_file(results_window, alignments, input_file, timestr, search_type):
    """
    Saves the found sliding windows hits to a tsv file

    Args:
        result_window: A list containing information about the found sliding window hits
        alignments: A list with Alignments objects
        input_file: A string with name of the file that is used as query
        timestr: A string of the current time
    """
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/allergen_window.tsv", "w") as output_file:
        output_file.write("# To see the alignments in change font to mono-style(example: Excel = Courier, LibreOffice = FreeMono\n")
        output_file.write("q_ID\th_ID\tSimi\tNo_hits\tHit_perc\tGlob_iden\tGlob_len\tAcc_ID\tSpec_name\tDesc\tSeq_DB\tAlignments\n")
        for result in results_window:
            output_file.write(result[0]+"\t"+result[1]+"\t"+str(result[2])+"\t"+str(result[3])+"\t"+str(result[4])+"\t"+str(result[5])+"\t"+str(result[6])+"\t"+result[7]+"\t"+result[8]+"\t"+result[9]+"\t"+result[10]+"\t")
            for alignment in alignments:
                if alignment.get_query_id() == result[0] and alignment.get_hit_id() == result[1]:
                    output_file.write('"'+alignment.get_alignment()+'"'+"\t")
            output_file.write("\n")


def save_wordmatch_file(results_word, alignments, input_file, timestr, search_type):
    """
    Saves the found exact word match hits to a tsv file

    Args:
        result_word: A list containing information about the found exact word hits
        alignments: A dictionary with alignments as values
        input_file: A string with name of the file that is used as query
        timestr: A string of the current time
    """
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/allergen_word.tsv", "w") as output_file:
        output_file.write("# To see the alignments in change font to mono-style(example: Excel = Courier, LibreOffice = FreeMono\n")
        output_file.write("q_ID\th_ID\tHits\tRemark\tHit_perc\tSwiss_acc\tSpec_name\tSeq_DB\tSeq_SR\tAlignments\n")
        for result in results_word:
            output_file.write(result[0]+"\t"+result[1]+"\t"+str(result[2])+"\t"+result[3]+"\t"+str(result[4])+"\t"+result[5]+"\t"+result[6]+"\t"+result[7]+"\t"+result[8]+"\t")
            for al in alignments[(result[0], result[1])]:
                output_file.write('"'+al+'"'+"\t")
            output_file.write("\n")


def save_allergen_full(results_full, input_file, timestr, search_type):
    """
    Saves the full FASTA36 response to a tsv file

    Args:
        results_full: A list containing information about the full search
        input_file: A string with name of the file that is used as query
        timestr: A string of the current time
    """
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/allergen_full_fasta.tsv", "w") as output_file:
        output_file.write("# To see the alignments in change font to mono-style(example: Excel = Courier, LibreOffice = FreeMono\n")
        output_file.write("Query ID\tQuery Length\tHit ID\tHit Length\tIdentity\tSimilarity\tAlignment Length\tBits\tE-value\tRecalc Ident\tAlignment\n")
        for hit in results_full:
            output_file.write(hit.get_query_id()+"\t"+str(hit.get_query_length())+"\t"+hit.get_hit_id()+"\t"+str(hit.get_hit_length())+"\t"+hit.get_identity()+"\t"+hit.get_similar()+"\t"+hit.get_overlap()+"\t"+
                            hit.get_bits()+"\t"+hit.get_e_value()+"\t"+str(hit.get_recalculated_ident())+"\t"+'"'+hit.get_alignment()+'"'+'\n')


def save_identical_celiac(result_identical, alignments_identical, input_file, timestr, search_type):
    db = celiac_database.import_database("")
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/celiac_identical.tsv", "w") as output_file:
        output_file.write('\t'.join(["Query_id", "Hit_id", "Number_hits", "HLADQ", "Database", "Source", "Source_id", "Alignment", '\n']))
        for result in result_identical:
            output_file.write(result[0]+'\t'+result[1]+'\t'+result[2]+'\t'+result[3]+'\t'+
                            result[4]+'\t'+result[5]+'\t'+result[6]+'\t')
            for al in alignments_identical[result[0],result[7]]:
                output_file.write('"'+al+'"'+'\t')
            output_file.write('\n')


def save_full_celiac(results_partial, input_file, timestr, search_type):
    db = celiac_database.import_database("")
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/celiac_partial.tsv", "w") as output_file:
        output_file.write('\t'.join(["Query_id", "Query_length", "Hit_id", "Hit_length", "Identity", "Similarity", "Overlap", "Bits", "E-value", "Alignments", '\n']))
        for result in results_partial:
            hit_id = result.get_hit_id()
            output_file.write('\t'.join([result.get_query_id(), str(result.get_query_length()), db[hit_id]["Name"], str(result.get_hit_length()), str(result.get_identity()), str(result.get_similar()),
                                        str(result.get_overlap()), str(result.get_bits()), str(result.get_e_value()), '"'+result.get_alignment()+'"']))
            output_file.write('\n')


def save_motif(results_motif, total_hits, input_file, timestr, search_type):
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/celiac_motif.tsv", "w") as output_file:
        output_file.write('\t'.join(["Query_id", "Motif", "Start", "End", "Risk", '\n']))
        for result in results_motif:
            output_file.write('\t'.join(result[:4])+'\t'+result[4]+'('+result[5]+'/'+total_hits+')' + '\n')


def save_toxin_full(results_toxins, input_file, timestr, search_type):
    
    with open("output/"+input_file+"_"+timestr+'_'+search_type+"/toxin_results.tsv", "w") as output_file:
        output_file.write('\t'.join(["Query_id", "Query_length", "Hit_id", "Hit_length", "Identity", "Similarity", "Overlap", "Bits", "E-value", "Alignments", '\n']))
        for result in results_toxins:
            hit_id = result.get_hit_id()
            output_file.write('\t'.join([result.get_query_id(), str(result.get_query_length()), result.get_hit_id(), str(result.get_hit_length()), str(result.get_identity()), str(result.get_similar()),
                                        str(result.get_overlap()), str(result.get_bits()), str(result.get_e_value()), '"'+result.get_alignment()+'"']))
            output_file.write('\n')