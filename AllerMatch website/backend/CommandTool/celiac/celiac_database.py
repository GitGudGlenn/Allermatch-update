import string, os, pickle, tempfile, itertools
from pathlib import Path


def get_current_db_path():
    script_dir = Path(os.path.dirname(__file__))
    rel_path = "celiac/data/current_db.pickle"
    script_dir = str(script_dir.parent)
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(abs_file_path, 'rb') as file:
        data = pickle.load(file)
    
    return script_dir+data["Current_DB"] 

def recify(l,s):
    return {
        "Epitope id": l[0], "Name": l[1],
        "HLADQ": l[2], "Database": l[3],
        "Source": l[4], "Source_id": l[5],
        "Sequence": s }

def import_database(db_path):
    db = {}
    if db_path == "":
        db_path = get_current_db_path()
    db_file = open(db_path, 'r')
    lines = db_file.read()
    
    head = ''; seq = ''; firstSeq = 1
    for line in lines.split('\n'):
        if not line: continue
        if (line[0] == '>') and (firstSeq):
            head = line[1:].split("\t"); seq = ''
            firstSeq = 0
        elif line[0] != '>':
            seq += line
        elif (line[0] == '>') and (not firstSeq):
            db[head[0]] = recify(head,seq)
            head = line[1:].split("\t"); seq = ''

    db[head[0]] = recify(head,seq)
    
    return db

def specify_database(db_nr):
    db_path = get_current_db_path()
    tmp_db_file = tempfile.NamedTemporaryFile()

    with open(tmp_db_file.name, 'w') as f:
        with open(db_path, 'r') as file:
            for head,seq in itertools.zip_longest(*[file]*2):
                head_db = head.split('\t')[3]
                if db_nr == 0:
                    f.write(head.strip()+'\n')
                    f.write(seq.strip()+'\n')
                elif db_nr == 1:
                    if head_db == "Sollid":
                        f.write(head.strip()+'\n')
                        f.write(seq.strip()+'\n')
                elif db_nr == 2:
                    if head_db == "ProPepper":
                        f.write(head.strip()+'\n')
                        f.write(seq.strip()+'\n')
                elif db_nr == 3:
                    if head_db == "AllergenOnline":
                        f.write(head.strip()+'\n')
                        f.write(seq.strip()+'\n')
                elif db_nr == 4:
                    if head_db == "Sollid" or head_db == "ProPepper":
                        f.write(head.strip()+'\n')
                        f.write(seq.strip()+'\n')
                elif db_nr == 5:
                    if head_db == "Sollid" or head_db == "AllergenOnline":
                        f.write(head.strip()+'\n')
                        f.write(seq.strip()+'\n')
                elif db_nr == 6:
                    if head_db == "AllergenOnline" or head_db == "ProPepper":
                        f.write(head.strip()+'\n')
                        f.write(seq.strip()+'\n')
    
    return tmp_db_file