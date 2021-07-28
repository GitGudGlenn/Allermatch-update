from Bio import Entrez

Entrez.email = "Your.Name.Here@example.org"

class FastaFile:
    id = ""
    db = ""
    allergen_name = ""
    source_db = ""
    accession = ""
    url = ""
    scientific_name = ""
    common_name = ""
    protein_name = ""
    sequence = ""
    sequence_length = ""
    mature_sequence = ""
    mature_sequence_length = ""
    message = ""

    def __init__(self, id: str, db: str, allergen_name: str, source_db: str, accession: str, url: str, 
                scientific_name: str, common_name: str, protein_name: str, sequence: str, 
                sequence_length: str, mature_sequence: str, mature_sequence_length: str, message: str):
        self.id = id
        self.db = db
        self.allergen_name = allergen_name
        self.source_db = source_db
        self.accession = accession
        self.url = url
        self.scientific_name = scientific_name
        self.common_name = common_name
        self.protein_name = protein_name
        self.sequence = sequence
        self.sequence_length = sequence_length
        self.mature_sequence = mature_sequence
        self.mature_sequence_length = mature_sequence_length
        self.message = message

    def set_message(self, value):
        self.message = value
    
    def get_accession(self):
        return self.accession
    
    def get_sequence(self):
        return self.mature_sequence

    def to_sequence_fasta(self):
        return(">"+'\t'.join([self.id, self.db, self.allergen_name, self.source_db, self.accession, self.url, 
                            self.scientific_name, self.common_name, self.protein_name, self.sequence_length])+'\n'+self.sequence)
    
    def to_mature_sequence_fasta(self):
        return(">"+'\t'.join([self.id, self.db, self.allergen_name, self.source_db, self.accession, self.url, 
                            self.scientific_name, self.common_name, self.protein_name, self.mature_sequence_length])+'\n'+self.mature_sequence)


def main(genbank_objects):
    genbank_ids, genbank_dict = get_genbank_ids(genbank_objects)
    fasta_objects_original, fasta_objects_peptides_removed = get_entrez_data(genbank_ids, genbank_dict)
    no_data_objects = diff(genbank_objects, fasta_objects_original, genbank_dict)
    
    return fasta_objects_original, fasta_objects_peptides_removed, no_data_objects


def diff(genbank_objects, fasta_objects, genbank_dict):
    no_data_found = []
    fasta_objects_ids = []
    genbank_objects_ids = []
    for allergen in fasta_objects:
        fasta_objects_ids.append(allergen.get_accession())
    for allergen in genbank_objects:
        genbank_objects_ids.append(allergen.get_genbank_prot())
    out = list(set(genbank_objects_ids) - set(fasta_objects_ids))

    for allergen in out:
        no_data_found.append(genbank_dict[allergen])
    
    return no_data_found


def get_genbank_ids(genbank_objects):
    genbank_dict = {}
    for allergen in genbank_objects:
        genbank_dict[allergen.get_genbank_prot()] = allergen
    
    genbank_ids = list(genbank_dict.keys())

    return genbank_ids, genbank_dict

def get_gi_number(self):
    other_ids = self["GBSeq_other-seqids"]
    try:
        for id in other_ids:
            if id.startswith('gi'):
                gi_number = id.split('|')[1]
        
        return gi_number
    except:
        return "No GI number"

def get_gene_name(self):
    gene_name = self["GBSeq_locus"]
    
    return gene_name

def get_accessions(self):
    primary_accession = self["GBSeq_primary-accession"]
    accession_version = self["GBSeq_accession-version"]

    return primary_accession, accession_version

def get_url(self):
    url = "https://www.ncbi.nlm.nih.gov/protein/%s" % self["GBSeq_primary-accession"]

    return url

def get_organisms(self):
    scientific_organism = self["GBSeq_organism"]
    if  '(' in self["GBSeq_source"]:
        common_name = self["GBSeq_source"].split("(")[1].replace(')', '')
    else:
        common_name = self["GBSeq_source"]

    return scientific_organism, common_name

def get_remark(self):
    remark = self["GBSeq_definition"].split('[')[0]
    
    return remark

def get_sequence(self):
    sequence = self["GBSeq_sequence"]
    
    return sequence

def get_mature_sequence(self, sequence):
    feature_dict = {}
    n = 1
    for feature in self["GBSeq_feature-table"]:
        position_dict = feature["GBFeature_intervals"][0]
        try:
            start = int(position_dict["GBInterval_from"])
            end = int(position_dict["GBInterval_to"])
            feature_type_dict = feature["GBFeature_quals"][0]
            feature_name_dict = feature["GBFeature_quals"][1]
            feature_type = feature_type_dict["GBQualifier_value"]
            if feature_type == "Processed active peptide":
                feature_name = feature_name_dict["GBQualifier_value"].split(' ')[0]
                feature_dict[feature_name+str(n)] = sequence[start-1:end]
                n += 1
        except:
            continue
    
    final_dict = {}
    for (key,value) in feature_dict.items():
        tmp_list = list(feature_dict.values())
        tmp_list.remove(value)
        tmp_string = ' '.join(tmp_list)
        if value not in tmp_string:
            final_dict[key] = value
    
    return final_dict


def get_entrez_data(id_list, genbank_dict):
    fasta_objects_original = []
    fasta_objects_peptides_removed = []
    handle = Entrez.efetch(db="protein", id=' '.join(id_list), retmode="xml")
    records = Entrez.read(handle)
    for record in records:
        gene_name = get_gene_name(record)
        gi_number = get_gi_number(record)
        accession, accession_version = get_accessions(record)
        url = get_url(record)
        scientific_name, common_name = get_organisms(record)
        remark = get_remark(record)
        sequence = get_sequence(record)
        seq_type = record["GBSeq_moltype"]
        if seq_type != "AA":
            continue
        mature_sequences = get_mature_sequence(record, sequence)
        genbank_allergen = genbank_dict[accession]

        fasta_objects_original.append(FastaFile(gene_name, "GenBank", gi_number, genbank_allergen.get_source_db(), accession, url, scientific_name, common_name, remark, sequence, str(len(sequence)),"","", ""))
        if len(mature_sequences) > 1:
            n = 1
            for (desc, seq) in mature_sequences.items():
                fasta_objects_peptides_removed.append(FastaFile(gene_name+'_'+str(n), "GenBank", gi_number, genbank_allergen.get_source_db(), accession, url, scientific_name, common_name, desc[:-1], "", "", seq, str(len(seq)), ""))
                n += 1
        elif len(mature_sequences) == 1:
            for (desc, seq) in mature_sequences.items():
                fasta_objects_peptides_removed.append(FastaFile(gene_name, "GenBank", gi_number, genbank_allergen.get_source_db(), accession, url, scientific_name, common_name, remark, "", "", seq, str(len(seq)), ""))
        else:
            fasta_objects_peptides_removed.append(FastaFile(gene_name, "GenBank", gi_number, genbank_allergen.get_source_db(), accession, url, scientific_name, common_name, remark, "", "", sequence, str(len(sequence)), ""))


    return fasta_objects_original, fasta_objects_peptides_removed
