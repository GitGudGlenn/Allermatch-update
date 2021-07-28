def create_option_dict(table = '', length = '', orf_type = '', word = '', window_cutoff = '', peptides_removed = '', celiac_database = ''
                        , input_file = '', file_name = '', file_input_type = '', timestr = '', search_type = ''):
    """
    Creates a dictionary with the settings/data used for a particular search.

    Args:
        table: Integer of which transcription table to use
        length: Integer for the minumum value to be a ORF
        orf_type: Boolean of searching between stop codons or between start and a stop codon
        word: Integer for the minimum n-mer exact word match
        window_cutoff: Integer for the minimum threshold for the sliding window
        peptides_removed: Booleans between searching in the original fasta files or the fasta file with signal- and propeptides removed
        celiac_database: Integer which database to use(see readme)
        input_file: String with the path to the input file
        file_name: String of the name of the input file
        file_input_type: String of the type of input file(DNA/AA)
        time_str: String of the current date
        search_type: String of which module was run
    Returns:
        opt_dict: A dictionary with all the info of a particular search
    """
    opt_dict = {
        "table": table, "length": length, "orf_type": orf_type,
        "word_length": word, "window_cutoff": window_cutoff,
        "peptides_removed": peptides_removed, "celiac_database": celiac_database, 
        "input_file_path": input_file, "file_name": file_name, 
        "file_input_type": file_input_type, "timestr": timestr, "search_type": search_type
    }
    return opt_dict