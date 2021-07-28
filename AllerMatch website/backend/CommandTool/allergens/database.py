import string, os, pickle

LOC = os.getcwd()+"/CommandTool"

with open(LOC+'/allergens/data/db/current_db.pickle', 'rb') as handle:
    curr_db = pickle.load(handle)
curr_db_path = curr_db["current_db"]

database_files = {
    True             : LOC + '/' + curr_db_path + '/AllergenDB_original_sequences.fasta',
    False            : LOC + '/' + curr_db_path + '/AllergenDB_propeptides_removed.fasta'}

#standard functions
def recify(l,s):
    return {
        "Allergen id"          : l[0], "Database Name"       : l[1],
        "Allergen Name"	: l[2], "Source db"           : l[3],
        "Accession id"         : l[4], "Hyperlink"           : l[5],
        "Species name"         : l[6], "English name"        : l[7],
        "Remark"               : l[8], "Size mature protein" : l[9],
        "Sequence"             : s }

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
