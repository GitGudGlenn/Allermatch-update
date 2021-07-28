import string, os, pickle

LOC = os.getcwd()+"/CommandTool"

with open(LOC+'/toxins/data/current_db.pickle', 'rb') as handle:
    curr_db = pickle.load(handle)
curr_db_path = curr_db["current_db"]

database_files = {True: LOC + curr_db_path + "/ToxinDB_original_sequences.fasta",
                False: LOC + curr_db_path + "/ToxinDB_propeptides_removed.fasta"}

def recify(l,s):
    return {
        "Allergen id"          : l[0], "Database Name"       : l[1],
        "Allergen Name"	       : l[2], "Accession id"         : l[3],
        "Hyperlink"            : l[4], "Species name"        : l[5],
        "English name"         : l[6], "Remark" : l[7],
        "Size mature protein"  : l[8], "Sequence"             : s }

def importDatabase(db):
    _db = {}
    f = open(db,'r')
    lines = f.read().splitlines()
    f.close()

    head = ''; seq = ''; firstSeq = 1
    for line in lines:
        if not line: continue
        if (line[0] == '>') and (firstSeq):
            head = line[1:].split("\t"); seq = ''
            firstSeq = 0
        elif line[0] != '>':
            seq += line
        elif (line[0] == '>') and (not firstSeq):
            _db[head[0]] = recify(head,seq)
            head = line[1:].split("\t"); seq = ''

    #last record
    _db[head[0]] = recify(head,seq)

    return _db

def get_db(db):
    return database_files[db]

def load_pickle(file):
    with open(file, 'rb') as handle:
        data = pickle.load(handle)
    return data

database_loaded = {}
for k in database_files.keys():
    database_loaded[k] = importDatabase(database_files[k])