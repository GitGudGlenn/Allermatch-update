import re, requests
import xml.etree.ElementTree as et

PREFIX = "{http://uniprot.org/uniprot}"
UNIPROT_API_LINK = "https://www.uniprot.org/uniprot/?query=id%%3A%s&format=xml"

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


def main(uniprot_objects):
    chunks, uniprot_dict = get_uniprot_ids(uniprot_objects)
    fasta_objects_original, fasta_objects_peptides_removed = get_data(chunks, uniprot_dict)
    no_data_objects = get_diff(uniprot_objects, fasta_objects_original, uniprot_dict)
    
    
    return fasta_objects_original, fasta_objects_peptides_removed, no_data_objects
    

def get_diff(uniprot_objects, fasta_objects, uniprot_dict):
    """
    Checks for which of the query IDs there no UniProt sequence data was found for

    Args:
        uniprot_objects: A list with Allergen objects created from create_allergen_db.py
        fasta_objects: A list with FastaFile objects of proteins where data from UniProt was found for
        uniprot_dict: A dictionary with as key the query UniProt ID and as value the Allergen object created from create_allergen_db.py
    Returns:
         A list with Allergen objects of query IDs where no data from UniProt was found for
    """
    no_data_found = []
    fasta_objects_ids = []
    uniprot_objects_ids = []
    for allergen in fasta_objects:
        fasta_objects_ids.append(allergen.get_accession())
    for allergen in uniprot_objects:
        uniprot_objects_ids.append(allergen.get_uniprot_id())
    out = list(set(uniprot_objects_ids) - set(fasta_objects_ids))
    
    for allergen in out:
        no_data_found.append(uniprot_dict[allergen])
    
    return no_data_found

def get_uniprot_ids(uniprot_objects):
    """
    Retrieves all the UniProt IDs from the Allergen objects and split them in equal chunks of 250

    Args:
        uniprot_objects: A list with Allergen objects created from create_allergen_db.py
    Returns:
        chunks: A nested list with lists of UniProt IDs
        uniprot_dict: A dictionary with as key the query UniProt ID and as value the Allergen object created from create_allergen_db.py
    """
    uniprot_dict = {}
    for allergen in uniprot_objects:
        uniprot_dict[allergen.get_uniprot_id()] = allergen
   
    chunks = list(divide_chunks(list(uniprot_dict.keys()), 250))

    return chunks, uniprot_dict

def get_genename(self):
    """
    Retrieves the gene name of the XML response from UniProt

    Args:
        self: XML objects of a certain protein
    Returns:
        gene_name: A string with the gene name of the protein
    """
    gene_name = self.findtext(PREFIX+"name")

    return gene_name

def get_accession(self):
    """
    Retrieves the main accession of the XML response from UniProt

    Args:
        self: XML objects of a certain protein
    Returns:
        accession_list[0]: A string with the main accession of the protein(first in list)
    """
    accession_list = []
    accessions = self.findall(PREFIX+"accession")
    for accesion in accessions:
        accession_list.append(accesion.text)
    
    return accession_list[0]


def get_sequence(self):
    """
    Retrieves the sequence of the XML response from UniProt

    Args:
        self: XML objects of a certain protein
    Returns:
        seq_clean: A string the sequence of the protein
    """
    sequence = self.findtext(PREFIX+"sequence")
    seq_clean = re.sub("\s+", "", sequence)

    return seq_clean


def get_allergen_name(self):
    """
    Retrieves the allergen name of the XML response from UniProt

    Args:
        self: XML objects of a certain protein
    Returns:
        name: A string with the allergen name of the protein
    """
    name = self.find(PREFIX+'protein').findtext(PREFIX+'allergenName')
    if name == None:
        for dbref in self.findall(PREFIX+"dbReference"):
            if dbref.get("type") == "Allergome":
                name = dbref.find(PREFIX+"property").get("value")
    
    if name == None:
        name = "No Allergen Name"
    
    return name

def get_url(accession):
    """
    Creates a UniProt url of the protein

    Args:
        accession: A string of the accession of a certain protein
    Returns:
        url_base + accession: A string with the url to the UniProt protein page
    """
    url_base = "http://www.uniprot.org/uniprot/"

    return url_base + accession

def get_organism(self):
    """
    Retrieves the scientific and common name of the XML response from UniProt

    Args:
        self: XML objects of a certain protein
    Returns:
        scientific_name: A string with the scientific organism name of the protein
        common_name: A string with the common organism name of the protein
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


def get_protein_name(self):
    """
    Retrieves the protein name of the XML response from UniProt

    Args:
        self: XML objects of a certain protein
    Returns:
        name: A string with the protein name of the protein
    """
    try:
        name = self.find(PREFIX+'protein').find(PREFIX+'recommendedName').findtext(PREFIX+'fullName')
    except:
        name = self.find(PREFIX+'protein').find(PREFIX+'submittedName').findtext(PREFIX+'fullName')
    return name


def get_mature_sequences(self, sequence, protein_name):
    """
    First checks if a protein has signal- or propeptides, removes them if they are present
    Checks if the mature sequences have an overlop, only keeps the 'bigger' mature sequence

    Args:
        self: XML objects of a certain protein
        sequence: A string of the sequence of a certain protein
        protein_name: A string with the protein name of a certain protein
    Returns:
        final_dict: A dictionary with as key the name of the mature sequence, and as value the sequence
    """
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
                


# def get_mature_sequence(self, sequence):
#     feature_dict = {}
#     n = 1
#     nn = 1
#     features = self.findall(PREFIX+'feature')
#     for feature in features:
#         if len(list(feature.find(PREFIX+"location").iter())) >= 3:
#             try:
#                 begin = int(feature.find(PREFIX+"location").find(PREFIX+"begin").get("position"))
#                 end = int(feature.find(PREFIX+"location").find(PREFIX+"end").get("position"))
#                 feature_type = feature.get("type")
#                 if feature_type == "signal peptide":
#                     feature_type = feature_type+str(n)
#                     n += 1
#                     feature_dict[feature_type] = (begin, end)
#                 if feature_type == "propeptide":
#                     feature_type = feature_type+str(nn)
#                     nn += 1
#                     feature_dict[feature_type] = (begin, end)
#             except:
#                 pass

#     print(feature_dict)
#     for k in feature_dict:
#         region = feature_dict[k]
#         s_list = list(sequence)
#         for i in range(region[0]-1, region[1]):
#             s_list[i] = "X"
#         sequence = ''.join(s_list)
#     templist = sequence.split('X')
#     new_list = list(filter(None, templist))
#     print(new_list)
#     mature_sequence = sequence.replace('X','')

#     return mature_sequence
    

def get_data(chunks, uniprot_dict):
    """
    Startpoint for calling all the XML parsing functions
    Creates FastaFile objects of protein from UniProt

    Args:
        chunks: A nested list with equal chunks(250 sequences per chunk) of the all the sequences
        uniprot_dict: A dictionary with as key the query UniProt ID and as value the Allergen object created from create_allergen_db.py
    Returns:
        fasta_objects_original: A list with FastaFile objects of protein from UniProt with their original sequence 
        fasta_objects_peptides_removed: A list with FastaFile objects of protein from UniProt with their mature sequence
    """
    fasta_objects_original = []
    fasta_objects_peptides_removed = []
    for chunk in chunks:
        page = requests.get(UNIPROT_API_LINK % '+OR+id%3A'.join(chunk))
        tree = et.fromstring(page.text)
        for item in tree.getiterator(PREFIX+"uniprot"):
            proteins = item.findall(PREFIX+'entry')
            for protein in item.findall(PREFIX+"entry"):
                gene_name = get_genename(protein)
                #print(gene_name)
                accession = get_accession(protein)
                #print(accession)
                allergen_name = get_allergen_name(protein)
                #print(allergen_name)
                url = get_url(accession)
                sequence = get_sequence(protein)
                scientific_name, common_name = get_organism(protein)
                protein_name = get_protein_name(protein)
                #print(protein_name)
                mature_sequences = get_mature_sequences(protein, sequence, protein_name)
                #print(mature_sequences)
                uniprot_allergen = uniprot_dict[accession]
                #print(mature_sequences)
                

                fasta_objects_original.append(FastaFile(gene_name, "UniProt", allergen_name, uniprot_allergen.get_source_db(), accession, url, scientific_name, common_name, protein_name, sequence, str(len(sequence)), "", "", ""))
                if len(mature_sequences) > 1:
                    n = 1
                    for (desc, seq) in mature_sequences.items():
                        fasta_objects_peptides_removed.append(FastaFile(gene_name+'_'+str(n), "UniProt", allergen_name, uniprot_allergen.get_source_db(), accession, url, scientific_name, common_name, desc[:-1], "", "", seq, str(len(seq)), ""))
                        n += 1
                elif len(mature_sequences) == 1:
                    for (desc, seq) in mature_sequences.items():
                        fasta_objects_peptides_removed.append(FastaFile(gene_name, "UniProt", allergen_name, uniprot_allergen.get_source_db(), accession, url, scientific_name, common_name, protein_name, "", "", seq, str(len(seq)), ""))
                else:
                    fasta_objects_peptides_removed.append(FastaFile(gene_name, "UniProt", allergen_name, uniprot_allergen.get_source_db(), accession, url, scientific_name, common_name, protein_name, "", "", sequence, str(len(sequence)), ""))

                
                # if len(mature_sequences) > 1:
                #     n = 1
                #     for (key,value) in mature_sequences.items():
                #         #print(gene_name+'_'+str(n), "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name, key[:-1], value, len(value))
                #         fasta_objects_peptides_removed.append(FastaFile(gene_name+'_'+str(n), "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name, key[:-1], sequence, str(len(sequence)), value, str(len(value)), ""))
                #         n += 1          
                # elif len(mature_sequences) == 1:
                #     for (key, value) in mature_sequences.items():
                #         #print(gene_name, "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name, key[:-1], value, len(value))
                #         fasta_objects_peptides_removed.append(FastaFile(gene_name, "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name, protein_name, sequence, str(len(sequence)), value, str(len(value)), ""))
                #     #print("___", gene_name, "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name)
                # else:
                #     fasta_objects_peptides_removed.append(FastaFile(gene_name, "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name, protein_name, sequence, str(len(sequence)), sequence, str(len(sequence)), ""))
                #     #print(gene_name, "UniProt", allergen_name, "uniprot_allergen.get_source_db()", accession, url, scientific_name, common_name, protein_name, sequence, str(len(sequence)), sequence, str(len(sequence)), "")

                #mature_sequence = get_mature_sequence(protein, sequence)
                #print("___")
                

                #fasta_objects.append(FastaFile(gene_name, "UniProt", allergen_name, uniprot_allergen.get_source_db(), accession, url, scientific_name, common_name, protein_name, sequence, str(len(sequence)), mature_sequence, str(len(mature_sequence)), ""))
    
    return fasta_objects_original, fasta_objects_peptides_removed

#test = get_data([["E0WDA3", "P85261", "Q07932", "Q9XFM4"],["",""]], "")
#test = get_data([["Q9XFM4","Q5MIT9"],["",""]], "")

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n]