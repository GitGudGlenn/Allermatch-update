import requests, re, pickle, os
import xml.etree.ElementTree as et

from datetime import date
from pathlib import Path

UNIPROT_URL = "https://www.uniprot.org/uniprot/?query=taxonomy%3A%22Metazoa+[33208]%22+and+(keyword%3Atoxin+OR+annotation%3A(type%3A%22tissue+specificity%22+venom))+AND+reviewed%3Ayes&columns=entry name,protein names,id,organism,sequence,feature(CHAIN)&format=xml"
PREFIX = "{http://uniprot.org/uniprot}"


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

    def __init__(self, id: str, db: str, source_db: str, accession: str, url: str, 
                scientific_name: str, common_name: str, protein_name: str, sequence: str, 
                sequence_length: str, mature_sequence: str, mature_sequence_length: str, message: str):
        self.id = id
        self.db = db
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
        return(">"+'\t'.join([self.id, self.db, self.source_db, self.accession, self.url, 
                            self.scientific_name, self.common_name, self.protein_name, self.sequence_length])+'\n'+self.sequence)
    
    def to_mature_sequence_fasta(self):
        return(">"+'\t'.join([self.id, self.db, self.source_db, self.accession, self.url, 
                            self.scientific_name, self.common_name, self.protein_name, self.mature_sequence_length])+'\n'+self.mature_sequence)



def main():
    datestr = date.today().strftime("%b-%Y")
    uniprot_request = get_request()
    fasta_objects_original, fasta_objects_peptides_removed = get_data(uniprot_request)
    save_to_fasta(fasta_objects_original, fasta_objects_peptides_removed, datestr)

def get_request():
    """
    Performs a GET request from the UniProt toxin database

    Returns:
        uniprot_request: A XML-format string with info about the toxins
    """
    uniprot_request = requests.get(UNIPROT_URL)

    return uniprot_request.text

def get_data(uniprot_request):
    """
    Start point for collecting data from the uniprot_request XML-string.

    Args:
        uniprot_request: A XML-format string with info about the toxins

    Returns:
        fasta_objects_original: A list containing FastaFile objects of toxin with their original sequence
        fasta_objects_peptides_remoced: A list containing FastaFile objects of toxins with their mature sequence
    """
    fasta_objects_original = []
    fasta_objects_peptides_removed = []
    tree = et.fromstring(uniprot_request)
    for item in tree.getiterator(PREFIX+"uniprot"):
        for protein in item.findall(PREFIX+"entry"):
            gene_name = get_genename(protein)
            accession = get_accession(protein)
            url = get_uniprot_link(accession)
            sequence = get_sequence(protein)
            scientific_name, common_name = get_organism(protein)
            protein_name = get_protein_name(protein)
            mature_sequences = get_mature_sequences(protein, sequence, protein_name)
            
            fasta_objects_original.append(FastaFile(gene_name, "UniProt", "UniProt", accession, url, scientific_name, common_name, protein_name, sequence, str(len(sequence)), "", "", ""))
            if len(mature_sequences) > 1:
                n = 1
                for (desc, seq) in mature_sequences.items():
                    fasta_objects_peptides_removed.append(FastaFile(gene_name+'_'+str(n), "UniProt", "UniProt", accession, url, scientific_name, common_name, desc, "", "", seq, str(len(seq)), ""))
                    n += 1
            elif len(mature_sequences) == 1:
                for (desc, seq) in mature_sequences.items():
                    fasta_objects_peptides_removed.append(FastaFile(gene_name, "UniProt", "UniProt", accession, url, scientific_name, common_name, desc, "", "", seq, str(len(seq)), ""))
            else:
                fasta_objects_peptides_removed.append(FastaFile(gene_name+'_'+str(n), "UniProt", "UniProt", accession, url, scientific_name, common_name, protein_name, "", "", sequence, str(len(sequence)), ""))
    
    return fasta_objects_original, fasta_objects_peptides_removed


def get_genename(self):
    """
    Retrieves the single gene name from the XML

    Args:
        self: The UniProt XML protein format

    Returns:
        gene_name: A string of the gene name
    """
    gene_name = self.findtext(PREFIX+"name")

    return gene_name   

def get_accession(self):
    """
    Retrieves the single accession from the XML

    Args:
        self: The UniProt XML protein format

    Returns:
        accession_list[0]: The first(primary) accession of the protein
    """
    accession_list = []
    accessions = self.findall(PREFIX+"accession")
    for accesion in accessions:
        accession_list.append(accesion.text)
    
    return accession_list[0]

def get_sequence(self):
    """
    Retrieves the single protein sequence from the XML

    Args:
        self: The UniProt XML protein format

    Returns:
        seq_clean: A string of the protein sequence
    """
    sequence = self.findtext(PREFIX+"sequence")
    seq_clean = re.sub("\s+", "", sequence)

    return seq_clean

def get_organism(self):
    """
    Retrieves the organism's names from the XML

    Args:
        self: The UniProt XML protein format

    Returns:
        scientific_name: A string with the scientific name(organism) of the protein
        common_name: A string the the english name of the protein
    """
    organism_dict = {}
    organisms = self.find(PREFIX+'organism').findall(PREFIX+"name")
    for organism in organisms:
        organism_dict[organism.attrib["type"]] = organism.text
    try:
        scientific_name = organism_dict["scientific"]
    except:
        scientific_name = "No Scientific Name"
    try:
        common_name = organism_dict["common"]
    except:
        common_name = "No Common name"
    
    return scientific_name, common_name


def get_uniprot_link(accesion):
    """
    Creates the uniprot url link to the uniprot page of the protein

    Args:
        accession: A string with the accession of the protein

    Returns:
        uniprot link of the protein
    """
    return "https://www.uniprot.org/uniprot/%s" % accesion


def get_protein_name(self):
    """
    Retrieves the single protein name(description) from the XML

    Args:
        self: The UniProt XML protein format

    Returns:
        name: A string with the proteins name(description)
    """
    try:
        name = self.find(PREFIX+'protein').find(PREFIX+'recommendedName').findtext(PREFIX+'fullName')
    except:
        name = self.find(PREFIX+'protein').find(PREFIX+'submittedName').findtext(PREFIX+'fullName')
    return name


def get_mature_sequences(self, sequence, protein_name):
    """
    Checks if the protein has mature sequences. Checks whether the protein has signal- or propeptides and removes it.
    If a protein has multiple mature chains that overlap, this function will only get the big overlapping chain

    Args:
        self: The UniProt XML protein format
        sequence: A string of the protein sequence
        protein_name: A string of the protein_name

    Returns:
        final_dict = A dictionary with the description of a chain as key, and the sequence as key
    """
    feature_dict = {}
    peptide_dict = {}
    n = 1
    features = self.findall(PREFIX+'feature')
    for feature in features:
        if len(list(feature.find(PREFIX+"location").iter())) >= 3:
            try:
                begin = int(feature.find(PREFIX+"location").find(PREFIX+"begin").get("position"))
                end = int(feature.find(PREFIX+"location").find(PREFIX+"end").get("position"))
                feature_type = feature.get("type")
                if feature_type == "chain":
                    chain_name = feature.get("description")
                    if chain_name == None:
                        chain_name = protein_name
                    peptide_dict[chain_name+str(n)] = sequence[begin-1:end]
                    n += 1
                elif feature_type == "peptide":
                    peptide_name = feature.get("description")
                    peptide_dict[peptide_name+str(n)] = sequence[begin-1:end]
                    n += 1
            except:
                pass

    final_dict = {}
    for (key, value) in peptide_dict.items():
        tmp_list = list(peptide_dict.values())
        tmp_list.remove(value)
        tmp_string = ' '.join(tmp_list)
        if value not in tmp_string:
            final_dict[key] = value

    return final_dict


def save_to_fasta(fasta_objects_original, fasta_objects_peptides_removed, datestr):
    """
    Creates a new folder of the current month(if it doesn't exist yet)
    Create two output file:
        ToxinDB_original_sequences: A .fasta file with the original sequence from each toxin protein
        ToxinDB_propeptides_remoces: A .fasta file with the mature sequences from each toxin protein

    Args:
        fasta_objects_original: A list containing FastaFile objects of toxin with their original sequence
        fasta_objects_peptides_remoced: A list containing FastaFile objects of toxins with their mature sequence
        datestr: A string of the current date

    """
    check_output_folder(datestr)
    script_dir = Path(os.path.dirname(__file__))
    rel_path = "data/db/ToxinDB_"+datestr+"/ToxinDB_original_sequences.fasta"
    rel_path2 = "data/db/ToxinDB_"+datestr+"/ToxinDB_propeptides_removed.fasta"
    script_dir = str(script_dir.parent)
    abs_file_path = os.path.join(script_dir, rel_path)
    abs_file_path2 = os.path.join(script_dir, rel_path2)

    with open(abs_file_path, 'w') as output_file:
        for toxin in fasta_objects_original:
            output_file.write(toxin.to_sequence_fasta()+'\n')
    
    with open(abs_file_path2, 'w') as output_file:
        for toxin in fasta_objects_peptides_removed:
            output_file.write(toxin.to_mature_sequence_fasta()+'\n')
    
    curr_db = {"current_db": "/toxins/data/db/ToxinDB_"+datestr, "update_date": date.today().strftime("%m/%d/%Y")}
    with open("toxins/data/current_db.pickle", 'wb') as handle:
        pickle.dump(curr_db, handle, protocol=pickle.HIGHEST_PROTOCOL)


def check_output_folder(datestr):
    """
    Checks if the output folder exists, otherwise creates it
    """
    if not os.path.exists('toxins/data/db/ToxinDB_'+datestr):
        os.makedirs('toxins/data/db/ToxinDB_'+datestr)



def to_pickle(filename, value):
    with open(filename, 'wb') as handle:
        pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()