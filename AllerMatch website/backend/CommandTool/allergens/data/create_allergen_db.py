import requests, re, os, pickle, tempfile, sys
import urllib.parse, urllib.request
import xml.etree.ElementTree as et
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from Bio import SeqIO
from datetime import date
from matplotlib_venn import venn3, venn3_circles

import get_uniprot_data
import get_ncbi_data
import ncbi_blast

LOC = os.getcwd()+"/CommandTool"

GLSEARCH36_EXECUTABLE = LOC+"/fasta-36.3.8h/bin/glsearch36"

UNIPROT_ALLERGEN_LINK = "https://www.uniprot.org/docs/allergen"
UNIPROT_ID_MAPPING_LINK = 'https://www.uniprot.org/uploadlists/'
WHO_IUIS_ALLERGEN_LINK = "http://www.allergen.org/search.php?allergenname=&allergensource=&TaxSource=&TaxOrder=&foodallerg=all&bioname=&browse=Browse"
ALLERGEN_BASE_LINK = "http://www.allergen.org/"
NCBI_LINK = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
UNIPROT_API_LINK = "https://www.uniprot.org/uniprot/?"

class Allergens:
    allergen_name = ""
    genbank_nucl = ""
    genbank_prot = ""
    uniprot_id = ""
    url_link = ""
    message = ""
    source_db = ""

    def __init__(self, allergen_name: str, genbank_nucl: str, genbank_prot: str, uniprot_id: str, url_link: str, message: str, source_db: str):
        self.allergen_name = allergen_name
        self.genbank_nucl = genbank_nucl
        self.genbank_prot = genbank_prot
        self.uniprot_id = uniprot_id
        self.url_link = url_link
        self.message = message
        self.source_db = source_db
    
    def get_allergen_name(self):
        return self.allergen_name

    def get_genbank_nucl(self):
        return self.genbank_nucl
    
    def set_genbank_nucl(self, value):
        self.genbank_nucl = value

    def get_genbank_prot(self):
        return self.genbank_prot
    
    def set_genbank_prot(self, value):
        self.genbank_prot = value

    def get_uniprot_id(self):
        return self.uniprot_id
    
    def set_uniprot_id(self, value):
        self.uniprot_id = value

    def get_url_link(self):
        return self.url_link
    
    def get_message(self):
        return self.message
    
    def set_message(self, value):
        self.message = value

    def get_source_db(self):
        return self.source_db

    def to_dict(self):
        info = {
            "id": self.allergen_name,
            "genbank_nucl": self.genbank_nucl,
            "genbank_prot": self.genbank_prot,
            "uniprot_id": self.uniprot_id,
            "URL": self.url_link,
            "message": self.message,
            "source": self.source_db
        }
        return info

def main():
    compare_path = input("Enter full path to current COMPARE DB fasta file: ")
    blast_bool = yes_no("BLAST leftovers(IDs with no external reference IDs found)? (this will take a long time) (y/n)")
    datestr = date.today().strftime("%b-%Y")

    check_output_folder(datestr)
    uniprot_objects = get_uniprot_ids()
    compare_ids, compare_dict = get_compare_ids(compare_path)
    compare_objects, compare_leftovers = expand_compare_ids(compare_ids, compare_dict)
    whoiuis_objects = get_who_iuis()
    whoiuis_objects, whoiuis_leftovers = expand_whoiuis_ids(whoiuis_objects)
    
    allergen_objects = uniprot_objects + compare_objects + whoiuis_objects
    
    uniprot_objects, genbankprot_objects, genbanknucl_objects = remove_dupps(allergen_objects)
    leftovers = compare_leftovers + whoiuis_leftovers + genbanknucl_objects
    
    print("\nGetting sequence data from UniProt...")
    fasta_original_uniprot_objects, fasta_prepeptides_removed_uniprot_objects, uniprot_no_data = get_uniprot_data.main(uniprot_objects)
    print("Retrieved UniProt fasta data: %i\nNo data found for:            %i" % (len(fasta_original_uniprot_objects), len(uniprot_no_data)))

    print("\nGetting sequence data from NCBI...")
    fasta_original_genbank_objects, fasta_propeptides_removed_genbank_objects, genbank_no_data = get_ncbi_data.main(genbankprot_objects)  
    print("Retrieved Genbank fasta data: %i\nNo data found for:            %i" % (len(fasta_original_genbank_objects), len(genbank_no_data)))

    to_fastafile(fasta_original_uniprot_objects, fasta_prepeptides_removed_uniprot_objects, fasta_original_genbank_objects, fasta_propeptides_removed_genbank_objects, datestr)
    set_current_db(datestr)

    if blast_bool:
        compare_hit_dict, leftovers = remove_fragments_of_larger_sequences(leftovers, compare_path, datestr)
        fasta_objects_original, fasta_objects_peptides_removed, uniprot_nodata, genbank_objects_original, genbank_objects_peptides_removed, genbank_nodata, leftovers = blast_leftovers(leftovers, compare_path, 
                                                                                                                                                                        fasta_original_uniprot_objects, fasta_original_genbank_objects, datestr)
        
        # add objects from BLAST to the previous objects
        fasta_original_uniprot_objects = append_list(fasta_original_uniprot_objects, fasta_objects_original)
        fasta_prepeptides_removed_uniprot_objects = append_list(fasta_prepeptides_removed_uniprot_objects, fasta_objects_peptides_removed)
        uniprot_no_data = append_list(uniprot_no_data, uniprot_nodata)
        
        fasta_original_genbank_objects = append_list(fasta_original_genbank_objects, genbank_objects_original)
        fasta_propeptides_removed_genbank_objects = append_list(fasta_propeptides_removed_genbank_objects, genbank_objects_peptides_removed)
        genbank_no_data = append_list(genbank_no_data, genbank_nodata)
    
    create_issues_table(leftovers, uniprot_no_data, genbank_no_data, datestr)
    create_venn_diagram(allergen_objects, uniprot_no_data, genbank_no_data, fasta_original_uniprot_objects, fasta_prepeptides_removed_uniprot_objects, fasta_original_genbank_objects, fasta_propeptides_removed_genbank_objects, datestr)

    size_db = len(fasta_original_uniprot_objects) + len(fasta_original_genbank_objects)#TODO it's bigger
    print("\nCreated AllermatchDB.\nTotal size: sequences%i\nIt is set as the current database for allergen_search.\nDatabase location: allergens/data/db/AllermatchDB_%s" % (size_db, datestr))


def to_pickle(filename, value): #TODO delete
    with open(filename, 'wb') as handle:
        pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(file):
    with open(file, 'rb') as handle:
        data = pickle.load(handle)
    return data

def get_uniprot_ids():
    """
    Webscrapes all IDs from UniProt allergens page(https://www.uniprot.org/docs/allergen)
    Creates Allergen objects from each ID

    Returns:
        A list with Allergen objects of allergens from UniProt allergens page
    """
    print("Webscraping UniProt IDs from https://www.uniprot.org/docs/allergen ...")
    uniprot_objects = []
    page = requests.get(UNIPROT_ALLERGEN_LINK)
    page = page.text.split("____________________________________________________________")[1]
    curr_gene = ""
    for line in page.split('\n'):
        allergen_name = re.findall(r"([a-zA-Z]{3,4} [a-z]{1,2} \w*)", line)
        if len(allergen_name) >= 1:
            curr_gene = allergen_name[0]
        
        ids = re.findall(r"<a href='\/uniprot\/(.*?)'>", line)

        for uniprot_id in ids:
            uniprot_objects.append(Allergens(curr_gene, "", "", uniprot_id, "", "", "Uniprot"))
    
    print("Found %i UniProt IDs\n" %len(uniprot_objects))

    return uniprot_objects


def get_compare_ids(compare_path):
    """
    Retrieves IDs from the COMPARE DB.

    Args:
        compare_path: A string with the path to the COMPARE DB
    Returns:
        compare_ids: A list with IDs from the COMPARE DB
        compare_dict: A dictionary with as key the ID and as value the allergen name
    """
    compare_dict = {}
    for record in SeqIO.parse(compare_path, "fasta"):
        gen_id = record.id.split('.')[0]
        allergen_name = re.findall(r"([a-zA-Z]{3,4} [a-z]{1,2} \w*)", record.description)
        if len(allergen_name) >= 1:
            curr_gene = allergen_name[0]
            compare_dict[gen_id] = curr_gene
        else:
            compare_dict[gen_id] = ""
    
    compare_ids = compare_dict.keys()
    print("Total COMPARE IDs found:                 %i" % len(compare_ids))

    return compare_ids, compare_dict

def expand_compare_ids(compare_ids, compare_dict):
    """
    Create Allergen objects from the IDs from COMPARE DB
    Checks for each gene ID if they are a UniProt ID, GenBank protein ID or a GenBank nucleotide ID.
    If possible, converts the GenBank IDs to UniProt IDs

    Args:
        compare_ids: A list with IDs from the COMPARE DB
        compare_dict: A dictionary with as key the ID and as value the allergen name
    Returns:
        compare_objects: A list with Allergen objects of allergens from COMPARE
        leftover_objects: A list with Allergen objects of entries where no external reference DB was found for
    """
    print("Converting COMPARE ids to UniProt IDs...")
    compare_objects = []
    leftover_objects = []

    # Finds originally uniprot ids
    uniprot_ids, uniprot_converted = post_uniprot_request("ACC+ID", "ACC", compare_ids)
    leftover = remove_from_list(compare_ids, uniprot_converted)
    for (id, converted) in zip(uniprot_ids, uniprot_converted):
        if id == converted:
            compare_objects.append(Allergens(compare_dict[id], "", "", converted, "", "Orignal uniprot ID", "COMPARE"))
        else:
            compare_objects.append(Allergens(compare_dict[id], "", "", converted, "", "Uniprot ID updated", "COMPARE"))
    print("Original UniProt IDs found:              %i" % len(uniprot_ids))

    # Finds GenBank protein ids and converts them to Uniprot
    genbank_prot_ids, genbank_prot_converted = post_uniprot_request("EMBL", "ACC", leftover)
    leftover = remove_from_list(leftover, genbank_prot_ids)
    for (id, converted) in zip(genbank_prot_ids, genbank_prot_converted):
        if not converted.startswith("UPI"):
            compare_objects.append(Allergens(compare_dict[id], "", id, converted, "", "Converted (GenBank Protein > Uniprot", "COMPARE"))
        else:
            leftover.append(id)
            #leftover_objects.append(Allergens(id, "", "", converted, "", "Converted to UniProt ID but is from UniParc", "COMPARE"))
    print("Converted Genbank protein > UniProt:     %i" % len(genbank_prot_ids))

    # Finds GenBank nucleotide ids and converts them to Uniprot
    genbank_nucl_ids, genbank_nucl_converted = post_uniprot_request("EMBL_ID", "ACC", leftover)
    leftover = remove_from_list(leftover, genbank_nucl_ids)
    for (id, converted) in zip(genbank_nucl_ids, genbank_nucl_converted):
        compare_objects.append(Allergens(compare_dict[id], id, "", converted, "", "Converted (GenBank Nucleotide > Uniprot", "COMPARE"))
    print("Converted Genbank nucleotide > UniProt:  %i" % len(genbank_nucl_ids))
    
    # Finds GenBank protein ids which did not have found a UniProt id earlier
    entrez_protein_ids = eutils_api_request("protein", leftover)
    leftover = remove_from_list(leftover, entrez_protein_ids)
    for id in entrez_protein_ids:
        compare_objects.append(Allergens(compare_dict[id], "", id, "", "", "Original GenBank protein ID(No Uniprot Found)", "COMPARE"))
    print("Genbank protein IDs(no UniProt found):   %i" % len(entrez_protein_ids))

    # Finds GenBank nucleotide ids which did not have found a UniProt id earlier
    entrez_nucleotide_ids = eutils_api_request("nuccore", leftover)
    leftover = remove_from_list(leftover, entrez_nucleotide_ids)
    for id in entrez_nucleotide_ids:
        compare_objects.append(Allergens(compare_dict[id], id, "", "", "", "Original GenBank nucleotide ID(No Uniprot Found)", "COMPARE"))
    print("Genbank nucleotide IDs(no UniProt found):   %i" % len(entrez_nucleotide_ids))
    
    for id in leftover:
        leftover_objects.append(Allergens(id, "", "", "", "", "No DB ID found", "COMPARE"))
    print("IDs leftover(in issues sheet):           %i\n" % len(leftover_objects))

    return compare_objects, leftover_objects


def get_who_iuis():
    """
    Webscrapes all pages from WHO/IUIS (http://www.allergen.org/) and collects the IDs
    Makes Allergens objects of the pages.

    Returns:
        who_iuis_objects: A list with Allergens objects created from WHO/IUIS
    """
    print("Webscraping IDS from http://www.allergen.org/ ...")
    page_who_iuis = requests.get(WHO_IUIS_ALLERGEN_LINK)
    soup = BeautifulSoup(page_who_iuis.text, 'html.parser')
    links = []
    for tr in soup.find_all('tr')[4:]:
        tds = tr.find_all('td')
        link = re.findall(r'<a href="(.*?)"', str(tds[1]))
        links.append(link[0])

    who_iuis_objects = []
    for link in links:
        page = requests.get(ALLERGEN_BASE_LINK + link)
        soup = BeautifulSoup(page.text, "html.parser")
        for table in soup.find_all('table', {'id' : "isotable"}):
            for tr in table.find_all('tr')[1:]:
                tds = tr.find_all('td')
                ids = []
                for td in tds:
                    ids.append(td.text.replace(u'\xa0', u''))
                allergen_name = ids[0].strip()
                genbank_nucl = ids[1].split(' ')[0].split('.')[0]
                genbank_prot = ids[2].split(' ')[0].split('.')[0]
                uniprot = ids[3].split(' ')[0].split('.')[0]
                who_iuis_objects.append(Allergens(allergen_name, genbank_nucl, genbank_prot, uniprot, link, "", "WHO/IUIS"))
    
    print("Total WHO/IUIS IDs found:                 %i" % len(who_iuis_objects))

    return who_iuis_objects


def expand_whoiuis_ids(whoiuis_objects):
    """
    Checks for each of the IDs from WHO/IUIS if they have an UniProt ID. If so, convert it to a UniProt ID.
    Also checks if a GenBank ID from WHO/IUIS is exisitng in the NCBI database.
    Also checks for wrongly placed IDs by WHO/IUIS and adjusts them

    Args:
        whoiuis_objects: A list with Allergens objects coming from WHO/IUIS
    Returns:
        whoiuis_objects: A list with Allergens objects and added/adjusted IDs
        nothin_found_objects: A list with Allergens objects of which no external reference DB was found for
    """
    uniprot_dict = {}
    genbankprot_dict = {}
    genbanknucl_dict = {}
    nothing_found_objects = []
    for allergen in whoiuis_objects:
        if allergen.get_uniprot_id() == '':
            if allergen.get_genbank_prot() != '':
                genbankprot_dict[allergen.get_genbank_prot()] = allergen
            elif allergen.get_genbank_nucl() != '':
                genbanknucl_dict[allergen.get_genbank_nucl()] = allergen
            else:
                nothing_found_objects.append(allergen)
        else:
            uniprot_dict[allergen.get_uniprot_id()] = allergen

    uniprot_ids = uniprot_dict.keys()
    up_not_found_objects = []
    up_ids, up_to_up = post_uniprot_request("ACC+ID", "ACC", uniprot_ids)
    up_leftover = remove_from_list(uniprot_ids, up_ids)
    for (id, converted) in zip(up_ids, up_to_up):
        if id == converted:
            uniprot_dict[id].set_message("Original UniProt ID")
        else:
            uniprot_dict[id].set_message("Uniprot ID updated")
            uniprot_dict[id].set_uniprot_id(converted)
    for allergen in whoiuis_objects:
        if allergen.get_uniprot_id() in up_leftover:
            if allergen.get_genbank_prot() != '':
                genbankprot_dict[allergen.get_genbank_prot()] = allergen
            elif allergen.get_genbank_nucl() != '':
                genbanknucl_dict[allergen.get_genbank_nucl()] = allergen
            else:
                allergen.set_message("UniProt ID not found")
                up_not_found_objects.append(allergen)
    print("Original UniProt IDs found:               %i" % len(up_ids))
    
    genbankprot_ids = genbankprot_dict.keys()
    gbp_ids, gbp_to_up = post_uniprot_request("EMBL", "ACC", genbankprot_ids)
    print("Converted Genbank protein > UniProt:      %i" % len(gbp_ids))
    gbp_leftover = remove_from_list(genbankprot_ids, gbp_ids)
    wrong_gbn_to_up_ids, wrong_gbn_to_up = post_uniprot_request("EMBL_ID", "ACC", gbp_leftover) # For entries where a nucleotide id is at protein position
    gbp_leftover = remove_from_list(gbp_leftover, wrong_gbn_to_up_ids)
    wrong_up_ids, wrong_up_to_up = post_uniprot_request("ACC+ID", "ACC", gbp_leftover) # For entries where a Uniprot ID is at protein position
    gbp_leftover = remove_from_list(gbp_leftover, wrong_up_to_up)
    original_gbp_ids = eutils_api_request("protein", gbp_leftover)
    print("Genbank protein IDs(no UniProt found):    %i" % len(original_gbp_ids))
    gbp_leftover = remove_from_list(gbp_leftover, original_gbp_ids)
    wrong_gbn_ids = eutils_api_request("nuccore", gbp_leftover)# Wrong placed ID's by WHO/IUIS
    gbp_leftover = remove_from_list(gbp_leftover, wrong_gbn_ids)
    
    for allergen in whoiuis_objects:
        gen_id = allergen.get_genbank_prot()
        if gen_id in gbp_ids:
            allergen.set_uniprot_id(gbp_to_up[gbp_ids.index(gen_id)])
            allergen.set_message("Converted GenBank protein > UniProt")
        elif gen_id in wrong_gbn_ids:
            allergen.set_uniprot_id(wrong_gbn_to_up[wrong_gbn_ids.index(gen_id)])
            allergen.set_message("Converted GenBank nucleotide > UniProt(Nucleotide id at protein position)")
        elif gen_id in wrong_up_ids:
            allergen.set_uniprot_id(wrong_up_to_up[wrong_up_ids.index(gen_id)])
            allergen.set_message("UniProt ID at protein positions, fault by WHO/IUIS(changed)")
        elif gen_id in original_gbp_ids:
            allergen.set_message("Original GenBank ID(No UniProt found)")
        elif gen_id in wrong_gbn_ids:
            allergen.set_genbank_nucl(gen_id)
            allergen.set_message("Nucleotide ID at protein position, fault by WHO/IUIS(changed)")
        elif gen_id in gbp_leftover:
            nothing_found_objects.append(allergen)

    genbanknucl_ids = genbanknucl_dict.keys()
    gbn_ids, gbn_to_up = post_uniprot_request("EMBL_ID", "ACC", genbanknucl_ids)
    gbn_leftover = remove_from_list(genbanknucl_ids, gbn_ids)
    print("Converted Genbank nucleotide > UniProt:   %i" % len(gbn_ids))
    wrong_gbp_to_up_ids, wrong_gbp_to_up = post_uniprot_request("EMBL", "ACC", gbn_leftover) # For entries where a protein id is at nucleotide position
    gbn_leftover = remove_from_list(gbn_leftover, wrong_gbp_to_up_ids)
    wrong_up_ids2, wrong_up_to_up2 = post_uniprot_request("ACC+ID", "ACC", gbn_leftover) # For entries where a UniProt ID is at nucleotide position
    gbn_leftover = remove_from_list(gbn_leftover, wrong_up_ids2)
    original_gbn_ids = eutils_api_request("nuccore", gbn_leftover)
    gbn_leftover = remove_from_list(gbn_leftover, original_gbn_ids)
    print("Genbank nucleotide IDs(no UniProt found): %i" % len(original_gbn_ids))
    wrong_gbp_ids = eutils_api_request("protein", gbn_leftover) # Wrong placed ID's by WHO/IUIS
    gbn_leftover = remove_from_list(gbn_leftover, wrong_gbp_ids)

    for allergen in whoiuis_objects:
        gen_id = allergen.get_genbank_nucl()
        if gen_id in gbn_ids:
            allergen.set_uniprot_id(gbn_to_up[gbn_ids.index(gen_id)])
            allergen.set_message("Converted GenBank nucleotide > UniProt")
        elif gen_id in wrong_gbp_to_up_ids:
            allergen.set_uniprot_id(wrong_gbp_to_up[wrong_gbp_to_up_ids.index(gen_id)])
            allergen.set_message("Converted GenBank protein > UniProt(protein id at nucleotide position)")
        elif gen_id in wrong_up_ids2:
            allergen.set_uniprot_id(wrong_up_to_up2[wrong_up_ids2.index(gen_id)])
            allergen.set_message("UniProt ID at nucleotide position, fault by WHO/IUIS(changed)")
        elif gen_id in original_gbn_ids:
            allergen.set_message("Original GenBank nucleotide ID(No Uniprot Found)")
        elif gen_id in wrong_gbp_ids:
            allergen.set_genbank_prot(gen_id)
            allergen.set_message("Protein ID at nucleotide position, fault by WHO/IUIS(changed)")
        elif gen_id in gbn_leftover:
            nothing_found_objects.append(allergen)
            allergen.set_message("No external DB ID found")
    
    print("\nErrors found in allergen.org(all adjusted):")
    print("Genbank nucleotide at protein position:                     %i" % len(wrong_gbn_to_up_ids))
    print("Uniprot ID at Genbank protein position:                     %i" % len(wrong_up_ids))
    print("Genbank nucleotide at protein position(No Uniprot ID found):%i" % len(wrong_gbn_ids))
    print("Genbank protein ID at nucleotide position:                  %i" % len(wrong_gbp_to_up_ids))
    print("UniProt ID at nucleotide position:                          %i" % len(wrong_up_ids2))
    print("Genbank protein at nucleotide position(No Uniprot ID found):%i" % len(wrong_gbp_ids))
    print("IDs leftover(in issues sheet):                              %i" % len(nothing_found_objects))


    return whoiuis_objects, nothing_found_objects


def remove_dupps(allergen_objects):
    """
    Removes dupplicates from all allergens(UniProt, WHO/IUIS, COMPARE)
    It removes them in the order:
        1. UniProt
        2. WHO/IUIS
        3. COMPARE

    Args:
        allergen_objects: A list with Allergen objects of all genes
    Returns:
        uniprot_ids: A list with UniProt Allergen objects 
        genbankprot_ids: A list with GenBank protein Allergen objects
        genbanknucl_ids: A list with GenBank nucleotide Allergen objects
    """
    print("\nRemoving dupplicates...")
    uniprot_objects = []
    genbankprot_objects = []
    genbanknucl_objects = []
    for allergen in allergen_objects:
        if allergen.get_uniprot_id() != '':
            uniprot_objects.append(allergen)
        elif allergen.get_genbank_prot() != '':
            genbankprot_objects.append(allergen)
        elif allergen.get_genbank_nucl() != '':
            genbanknucl_objects.append(allergen)

    new_objects_uniprot = {}
    for allergen in uniprot_objects:
        if allergen.get_source_db() == "Uniprot":
            new_objects_uniprot[allergen.get_uniprot_id()] = allergen
    for allergen in uniprot_objects:
        if allergen.get_source_db() == "WHO/IUIS":
            if allergen.get_uniprot_id() not in new_objects_uniprot:
                new_objects_uniprot[allergen.get_uniprot_id()] = allergen
    for allergen in uniprot_objects:
        if allergen.get_source_db() == "COMPARE":
            if allergen.get_uniprot_id() not in new_objects_uniprot:
                new_objects_uniprot[allergen.get_uniprot_id()] = allergen
    
    new_objects_genbankprot = {}
    for allergen in genbankprot_objects:
        if allergen.get_source_db() == "WHO/IUIS":
            if allergen.get_genbank_prot() not in new_objects_genbankprot:
                new_objects_genbankprot[allergen.get_genbank_prot()] = allergen
    for allergen in genbankprot_objects:
        if allergen.get_source_db() == "COMPARE":
            if allergen.get_genbank_prot() not in new_objects_genbankprot:
                new_objects_genbankprot[allergen.get_genbank_prot()] = allergen

    new_objects_genbanknucl = {}
    for allergen in genbanknucl_objects:
        if allergen.get_source_db() == "WHO/IUIS":
            if allergen.get_genbank_nucl() not in new_objects_genbanknucl:
                new_objects_genbanknucl[allergen.get_genbank_nucl()] = allergen
    for allergen in genbanknucl_objects:
        if allergen.get_source_db() == "COMPARE":
            if allergen.get_genbank_nucl() not in new_objects_genbanknucl:
                new_objects_genbanknucl[allergen.get_genbank_nucl()] = allergen

    uniprot_ids = []
    for k in new_objects_uniprot:
        uniprot_ids.append(new_objects_uniprot[k])
    genbankprot_ids = []
    for k in new_objects_genbankprot:
        genbankprot_ids.append(new_objects_genbankprot[k])
    genbanknucl_ids = []
    for k in new_objects_genbanknucl:
        genbanknucl_ids.append(new_objects_genbanknucl[k])

    return uniprot_ids, genbankprot_ids, genbanknucl_ids


def post_uniprot_request(original, to, id_list):
    """
    Performs a UniProt API request to convert IDS to UniProt IDs (if possible)

    Args:
        original: A string of the originale DB id
        to: A string of the database to where it must be converted to
        id_list: A list with gene ids
    Returns:
        from_ids: A list with the input ids
        to_ids: A list with the converted ids
    """
    try:
        params = {
            'from': original,
            'to': to,
            'format': 'tab',
            'query': ' '.join(id_list)
        }
        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(UNIPROT_ID_MAPPING_LINK, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()
        
        from_ids = []
        to_ids = []
        for line in response.decode('utf-8').strip().split('\n')[1:]:
            from_ids.append(line.split()[0].strip())
            to_ids.append(line.split()[1].strip())
        return from_ids, to_ids

    except urllib.error.HTTPError:
        print("UniProt Retrieve/ID Mapping api server failure...\n Retrying")
        from_ids, to_ids = post_uniprot_request(original, to, id_list)
        return from_ids, to_ids
  

def eutils_api_request(db, gene_list):
    """
    Performs a NCBI API request to check if genes exist in the NCBI database

    Args:
        db: A string for which NCBI DB to look in("protein" or "nuccore")
        gene_list: A list with gene IDs
    Returns:
        entrez_ids: A list with gene IDs that are in NCBI
    """
    page = requests.post(NCBI_LINK, data={"db": db,
                                    "id" : ",".join(gene_list)})
    entrez_ids = []
    myroot = et.fromstring(page.text)
    for x in myroot:
        if x.tag == "DocSum":
            if x[10].text == "live":
                entrez_ids.append(x[1].text)
            elif x[10].text == "replaced":
                entrez_ids.append(x[11].text)

    return entrez_ids


def to_fastafile(fasta_uniprot_objects, fasta_prepeptides_removed_uniprot_objects, fasta_genbank_objects, fasta_propeptides_removed_genbank_objects, datestr):
    with open("allergens/data/db/AllermatchDB_"+datestr+"/AllergenDB_original_sequences.fasta", 'w') as original_output:
        for allergen in fasta_uniprot_objects:
            original_output.write(allergen.to_sequence_fasta()+'\n')
        for allergen in fasta_genbank_objects:
            original_output.write(allergen.to_sequence_fasta()+'\n')
    with open("allergens/data/db/AllermatchDB_"+datestr+"/AllergenDB_propeptides_removed.fasta", 'w') as removed_output:
        for allergen in fasta_prepeptides_removed_uniprot_objects:
            removed_output.write(allergen.to_mature_sequence_fasta()+'\n')
        for allergen in fasta_propeptides_removed_genbank_objects:
            removed_output.write(allergen.to_mature_sequence_fasta()+'\n')


def set_current_db(datestr):
    """
    Creates a .pickle file with the path and date of the AllermatchDB

    Args:
        datestr: A String with the current month and year
    """
    curr_db = {"current_db": "allergens/data/db/AllermatchDB_"+datestr, "update_date": date.today().strftime("%m/%d/%Y")}
    with open("allergens/data/db/current_db.pickle", 'wb') as handle:
        pickle.dump(curr_db, handle, protocol=pickle.HIGHEST_PROTOCOL)


def remove_fragments_of_larger_sequences(leftovers, compare_path, datestr):
    """
    Removes allergens from leftovers if they have more than 98% identity hit with a allergen in the AllermatchDB.
    This reduces the amount of leftovers, which lowers the BLAST time.

    Args:
        leftovers: A list with Allergens objects of entries where no external reference ID was found for
        compare_path: A string with the path to the COMPARE db
        datestr: A String with the current month and year
    Returns:
        compare_hit_dict: A dictionary with as key the ID of which no data was found for and as value the best hit from Allermatch with the identity
        leftovers: A list with Allergens objects of entries where no external reference ID was found for(leftovers with >98% identity were removed)
    """
    issues_ids = []
    issues_dict = {}
    for allergen in leftovers:
        issues_ids.append(allergen.get_allergen_name())
        issues_dict[allergen.get_allergen_name()] = allergen
    
    compare_ids = []
    compare_seqs = []
    for record in SeqIO.parse(compare_path, 'fasta'):
        if record.id.split('.')[0] in issues_ids:
            compare_ids.append(str(record.id).split('.')[0])
            compare_seqs.append(str(record.seq))
    tmp_query_fasta = save_global_to_tmpfile(compare_seqs, compare_ids)
    
    with open(tmp_query_fasta.name, 'r') as query_file:
        commandline = GLSEARCH36_EXECUTABLE+" "+query_file.name+" -C 1000 "+"allergens/data/db/AllermatchDB_"+datestr+"/AllergenDB_original_sequences.fasta"
        fasta_pipe = os.popen(commandline)
        fasta_res = fasta_pipe.read()
    
    compare_hit_dict = {}
    for query in fasta_res.split(">>>")[1:]:
        query_id = query.split()[0]
        curr_ident = 0
        compare_hit_dict[query_id] = ("No hit", "0")
        for hit in query.split(">>")[1:]:
            if ">--" in hit:
                hit = hit.split(">--")[0]
            identity, idlen = re.search(r' ([0-9\.]+)\% *identity \(.+?\) in (\d*) aa overlap',
                                        hit).groups()
            identity = float(identity)
            idlen = int(idlen)
            hit_id = hit.split('\n')[0].split()[0]
            if identity > curr_ident:
                compare_hit_dict[query_id] = (hit_id, identity)
                curr_ident = identity
    
    for (key,value) in compare_hit_dict.items():
        if float(value[1]) >= 98.0:
            leftovers.remove(issues_dict[key])

    return compare_hit_dict, leftovers


def save_global_to_tmpfile(sequences, ids):
    """
    Saves the whole query-sequences to a tempfile, this will be used for a global GLSEARCH36

    Args:
        sequences: A list containing the query-sequences
        ids: A list containing the query-ids

    Returns:
        tmp: A tempfile(path) with the whole sequences
    """
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        for (seq, i) in zip (sequences, ids):
            if i.startswith(">"):
                f.write(i+"\n")
            else:
                f.write(">"+i+"\n")
            f.write(seq+"\n")
    return tmp

def create_issues_table(leftovers, uniprot_no_data, genbank_no_data, datestr):
    """
    Outputs a .tsv file with allergens of which no data was found for.

    Args:
        leftovers: A list with Allergens objects of entries where no external reference ID was found for
        uniprot_no_data: A list with Allergen objects of which no UniProt sequence data was found for
        genbank_no_data: A list with Allergen objects of which no GenBank sequence data was found for
        datestr: A String with the current month and year
    """
    for allergen in uniprot_no_data:
        allergen.set_message("No UniProt sequence data found")
        leftovers.append(allergen)
    for allergen in genbank_no_data:
        allergen.set_message("No GenBank sequence data found")
        leftovers.append(allergen)
    with open("allergens/data/db/AllermatchDB_"+datestr+"/Issues.tsv", 'w') as output:
        for allergen in leftovers:
            output.write('\t'.join([allergen.get_allergen_name(), allergen.get_genbank_nucl(), allergen.get_genbank_prot(), allergen.get_uniprot_id(), allergen.get_source_db(), allergen.get_url_link(), 
                                    allergen.get_message()])+'\n')
    #df = pd.DataFrame.from_records([s.to_dict() for s in leftovers])TODO
    #df.to_csv("allergens/data/db/AllermatchDB_"+datestr+"/Issues.tsv", sep='\t')


def check_output_folder(datestr):
    """
    Checks if the output folder exists, otherwise creates it
    """
    if not os.path.exists('allergens/data/db/AllermatchDB_'+datestr):
        os.makedirs('allergens/data/db/AllermatchDB_'+datestr)


def create_venn_diagram(allergen_objects, uniprot_no_data, genbank_no_data, fasta_uniprot_objects, fasta_prepeptides_removed_uniprot_objects, fasta_original_genbank_objects, fasta_propeptides_removed_genbank_objects, datestr): #TODO added fasta_prepeptides_removed_uniprot_objects
    """
    Creates a venn diagram

    Args:
        allergen_objects: A list with Allergen objects from all data sources(UniProt, WHO/IUIS and COMPARE)(Dupplicates not removed)
        uniprot_no_data: A list with Allergen objects of which no UniProt sequence data was found for
        genbank_no_data: A list with Allergen objects of which no GenBank sequence data was found for
        fasta_uniprot_objects: A list with FastaFile objects of allergens with UniProt sequence data with their original sequence
        fasta_prepeptides_removed_uniprot_objects: A list with FastaFile objects of allergens with UniProt sequence data with their mature sequence
        fasta_original_genbank_objects: A list with FastaFile objects of allergens with GenBank sequence data with their original sequence
        fasta_propeptides_removed_genbank_objects: A list with FastaFile objects of allergens with GenBank sequence data with their mature sequence
        datestr: A String with the current month and year
    """
    total_db_size = len(fasta_uniprot_objects) + len(fasta_original_genbank_objects) - len(uniprot_no_data) - len(genbank_no_data)
    uniprot_ids = []
    compare_ids = []
    who_ids = []
    for allergen in allergen_objects:
        if allergen.get_source_db() == "Uniprot":
            uniprot_ids.append(allergen.get_uniprot_id())
        elif allergen.get_source_db() == "COMPARE":
            if allergen.get_uniprot_id() != '':
                compare_ids.append(allergen.get_uniprot_id())
            elif allergen.get_genbank_prot() != '':
                compare_ids.append(allergen.get_genbank_prot())
        elif allergen.get_source_db() == "WHO/IUIS":
            if allergen.get_uniprot_id() != '':
                who_ids.append(allergen.get_uniprot_id())
            elif allergen.get_genbank_prot() != '':
                who_ids.append(allergen.get_genbank_prot())
    
    venn3([set(compare_ids), set(who_ids), set(uniprot_ids)], set_labels = ('COMPARE DB', 'WHO/IUIS Allergen.org', 'UniProt (SwissProt)'))
    plt.title('Overlap between the 3 databases.\nAllermatchDB = %s'% str(total_db_size))
    matplotlib.pyplot.savefig("allergens/data/db/AllermatchDB_"+datestr+"/venn_diagram.png")


def remove_from_list(main_list, delete_list):
    return [s for s in main_list if s not in delete_list]


def append_list(l1, l2):
    if l2:
        return l1 + l2
    else:
        return l1


def blast_leftovers(leftovers, compare_path, fasta_original_uniprot_objects, fasta_original_genbank_objects, datestr):
    """
    Startpoint for BLASTing the allergens of which no external DB reference ID was found

    Args:
        leftovers: A list with Allergens objects of entries where no external reference ID was found for
        compare_path: A String with the compareDB path
        datestr: A String with the current month and year

    Returns:
        fasta_objects_original: A list with new Allergen objects from BLAST of UniProt allergens with their original sequence
        fasta_objects_peptides_removed: A list with new Allergen from BLAST objects of UniProt allergens with their mature sequence
        uniprot_nodata: A list with Allergens objects which has no data at UniProt
        genbank_objects_original: A list with new Allergen objects from BLAST of GenBank allergens with their orignal sequence
        genbank_objects_peptides_removed: A list with new Allergen objects from BLAST of GenBank allergens with their mature sequence
        genbank_nodata: A list with Allergens objects which has no data at GenBank

    """
    fasta_objects_original, fasta_objects_peptides_removed, uniprot_nodata, genbank_objects_original, genbank_objects_peptides_removed, genbank_nodata = ([] for i in range(6))
    issues_ids = []
    accessions = set()
    empty_dict = {}
    for allergen in leftovers[50:53]:
        issues_ids.append(allergen.get_allergen_name())
    
    compare_issues_dict = {}
    for record in SeqIO.parse(compare_path, 'fasta'):
        if record.id.split('.')[0] in issues_ids:
            id = record.description.split()[0].split('.')[0]
            scientific_name = record.description.split('[')[1][:-1]
            compare_issues_dict[str(record.seq)] = (id, scientific_name)
    
    blast_results = ncbi_blast.blast_leftovers(compare_issues_dict, compare_path)

    compare_ids_with_hit = set()
    for hit in blast_results:
        compare_ids_with_hit.add(hit.get_compare_id())
        accessions.add(hit.get_accession())
        empty_dict[hit.get_accession()] = ""

    leftovers = [allergen for allergen in leftovers if allergen.get_allergen_name() not in list(compare_ids_with_hit)]

    new_objects, leftover_objects = expand_compare_ids(list(accessions), empty_dict)
    
    new_objects = remove_redundant_hits(new_objects, fasta_original_uniprot_objects, fasta_original_genbank_objects)

    uniprot_hits = []
    genbank_hits = []
    for hit in new_objects:
        if hit.get_uniprot_id() != '':
            uniprot_hits.append(hit)
        else:
            genbank_hits.append(hit)

    if uniprot_hits:
        fasta_objects_original, fasta_objects_peptides_removed, uniprot_nodata = get_uniprot_data.main(uniprot_hits)
    if genbank_hits:
        genbank_objects_original, genbank_objects_peptides_removed, genbank_nodata = get_ncbi_data.main(genbank_hits)

    append_blast_hits_to_fastas(fasta_objects_original, fasta_objects_peptides_removed, genbank_objects_original, genbank_objects_peptides_removed, datestr)

    return fasta_objects_original, fasta_objects_peptides_removed, uniprot_nodata, genbank_objects_original, genbank_objects_peptides_removed, genbank_nodata, leftovers


def remove_redundant_hits(new_objects, fasta_original_uniprot_objects, fasta_original_genbank_objects):
    accessions = []
    for allergen in fasta_original_uniprot_objects:
        accessions.append(allergen.get_accession())
    for allergen in fasta_original_genbank_objects:
        accessions.append(allergen.get_accession())

    blast_results_cleaned = []
    for allergen in new_objects:
        if allergen.get_uniprot_id() not in accessions and allergen.get_genbank_prot() not in accessions:
            blast_results_cleaned.append(allergen)

    return blast_results_cleaned



def append_blast_hits_to_fastas(fasta_uniprot_objects, fasta_prepeptides_removed_uniprot_objects, fasta_genbank_objects, fasta_propeptides_removed_genbank_objects, datestr):
    """
    Appends each of the hits from the BLAST to each of the .fasta files

    Args:
        fasta_uniprot_objects: A list with Allergen objects of UniProt allergens with their original sequence
        fasta_prepeptides_removed_uniprot_objects: A list with Allergen objects of UniProt allergens with their mature sequence
        fasta_genbank_objects: A list with Allergen objects of GenBank allergens with their orignal sequence
        fasta_propeptides_removed_genbank_objects: A list with Allergen objects of GenBank allergens with their mature sequence

    """
    with open("allergens/data/db/AllermatchDB_"+datestr+"/AllergenDB_original_sequences.fasta", 'a') as original_output:
        for allergen in fasta_uniprot_objects:
            original_output.write(allergen.to_sequence_fasta()+'\n')
        for allergen in fasta_genbank_objects:
            original_output.write(allergen.to_sequence_fasta()+'\n')
    with open("allergens/data/db/AllermatchDB_"+datestr+"/AllergenDB_propeptides_removed.fasta", 'a') as removed_output:
        for allergen in fasta_prepeptides_removed_uniprot_objects:
            removed_output.write(allergen.to_mature_sequence_fasta()+'\n')
        for allergen in fasta_propeptides_removed_genbank_objects:
            removed_output.write(allergen.to_mature_sequence_fasta()+'\n')

def yes_no(answer):
    """
    Asks if the leftovers must be BLAST ed to the NCBI database

    Args:
        answer: String with the question
    Returns:
        boolean
    """
    yes = set(['yes','y', 'ye', ''])
    no = set(['no','n'])
     
    while True:
        choice = input(answer).lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print("Please respond with 'yes' or 'no'('y' or 'n')\n")

if __name__ == "__main__":
    main()
