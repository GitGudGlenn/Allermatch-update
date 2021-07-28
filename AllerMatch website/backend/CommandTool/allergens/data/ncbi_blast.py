import requests, json, re, time, pickle, queue

from Bio import SeqIO
from collections import defaultdict

import get_uniprot_data
import get_ncbi_data

BLAST_RESULTS_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
BLAST_REQUEST = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?QUERY=%s&DATABASE=nr&PROGRAM=blastp&CMD=Put&FORMAT_TYPE=JSON"
SOFT_LIMIT = 50

# Order of which hit to keep, Same means query has the same organism as the hit
FAVORABLE_HIT = {
	("UniProt", "Same"): 6,
	("GenBank", "Same"): 5,
	("RefSeq", "Same"): 4,
	("UniProt", "Different"): 3,
	("GenBank", "Different"): 2,
	("RefSeq", "Different"): 1
}

ABBREV_DICT = {
		"sp": "UniProt",
		"gb": "GenBank",
		"emb": "GenBank",
		"ref": "RefSeq"
	}


class BlastResult:
	protein_id = ""
	accession = ""
	query_id = ""
	source_db = ""
	scientific_name = ""
	identity = float
	query_start = 0
	query_end = 0
	hit_start = 0
	hit_end = 0
	query_seq = ""
	midline = ""
	hit_seq = ""
	type_hit = 0

	def __init__(self, protein_id: str, accession: str, query_id: str, source_db: str, scientific_name: str, identity: float, query_start: int, query_end: int, 
				hit_start: int, hit_end: int, query_seq: str, midline: str, hit_seq: str, type_hit: int):
		self.protein_id = protein_id
		self.accession = accession
		self.query_id = query_id
		self.source_db = source_db
		self.scientific_name = scientific_name
		self.identity = identity
		self.query_start = query_start
		self.query_end = query_end
		self.hit_start = hit_start
		self.hit_end = hit_end
		self.query_seq = query_seq
		self.midline = midline
		self.hit_seq = hit_seq
		self.type_hit = type_hit

	def get_accession(self):
		return self.accession
	
	def get_type_hit(self):
		return self.type_hit

	def get_compare_id(self):
		return self.query_id

	def to_dict(self):
		info = {
			"Protein_id": self.protein_id,
			"Accession": self.accession,
			"Compare_id": self.query_id,
			"Source_DB": self.source_db,
			"Scientific_name": self.scientific_name,
			"Identity": self.identity,
			"Query_start": self.query_start,
			"Query_end": self.query_end,
			"Hit_start": self.hit_start,
			"Hit_end": self.hit_end,
			"Query_seq": self.query_seq,
			"Midline": self.midline,
			"Hit_seq": self.hit_seq,
			"Hit_type": self.type_hit
		}
		return info

def blast_leftovers(compare_dict, compare_path):
	full_json_dict = run_blast(compare_dict, compare_path)
	accession_list = get_compare_path_accessions(compare_path)
	blast_results = parse_blast_json(full_json_dict, compare_dict, accession_list)

	return blast_results



def run_blast(compare_dict, compare_path):
	"""
	BLAST every sequence that is a leftover from the create_allergen_db.py
	Keeps the total running BLAST processes under the SOFT_LIMIT(50)

	Args:
		compare_dict: A dictionary with as key the sequences and
		compare_path: A string with the path location to the COMPARE DB
	Returns:
		full_json_dict: A dictionary with as key the sequence and as value the response from BLAST
	"""
	full_json_dict = {}

	running = []
	finished = set()
	failed = []

	sequences = list(compare_dict)
	q = queue.Queue()
	for seq in sequences:
		q.put(seq)
	while len(finished) != len(sequences):
		if len(running) < SOFT_LIMIT and not q.empty():
			running.append(get_rid(q.get()))
		for run in running:
			seq = next(iter(run))
			rid = run[seq]
			request_dict = get_post_request_dict(rid)
			page = requests.post(BLAST_RESULTS_URL, data=request_dict)
			status = ""
			try:
				status = re.findall(r"Status=(.*)", page.text)[0]
			except:
				try:
					blast_json = json.loads(page.text)
					finished.add(seq)
					full_json_dict[seq] = blast_json
					running.remove(run)
					print(len(finished), '/', len(sequences))
				except:
					print(page.text)
			if status == "FAILED":
				failed.append(seq)
				finished.append(seq)
			elif status == "WAITING":
				if len(running) < SOFT_LIMIT:
					if q.empty():
						time.sleep(60)
					else:
						continue
				else:
					time.sleep(60)

	return full_json_dict


def parse_blast_json(json_dict, compare_dict, accession_list):
	blast_results = []
	already_in_compare_dict = {}
	hit_same_organism = {} #TODO
	hit_different_organism = defaultdict(list) #TODO
	no_sig_hit = [] #TODO
	no_hit_found = []

	for (seq, value) in json_dict.items():
		compare_id = compare_dict[seq][0]
		compare_organism_name = compare_dict[seq][1].lower()
		duplicate_hit = check_if_hit_in_db(value, accession_list)
		if duplicate_hit != False:
			already_in_compare_dict[seq] = duplicate_hit
			continue    # if one BLAST hit is already in the compare fasta file, skip

		if not value["BlastOutput2"][0]["report"]["results"]["search"]["hits"]:
			no_hit_found.append(seq)
			continue    # if no BLAST hit found, skip

		curr_identity = 0.0
		curr_hit = BlastResult('','','','','',0.0,0,0,0,0,'','','',0)
		curr_type_hit = 0

		for hits in value["BlastOutput2"][0]["report"]["results"]["search"]["hits"]:
			identity = hits["hsps"][0]["identity"] / hits["hsps"][0]["align_len"] * 100
			if identity >= curr_identity:
				curr_identity = identity    # Only keeps the BLAST hits with the highest identity
				for hit in hits["description"]:
					if get_source_db(hit["id"]) != None:
						source_db = get_source_db(hit["id"])
						scientific_name = hit["sciname"].lower()
						if scientific_name == compare_organism_name:    # If BLAST hit is same organism as organism from COMPARE
							organism = "Same"
						else:
							organism = "Different"
						if FAVORABLE_HIT[(source_db, organism)] > curr_type_hit:    # If a specific BLAST hit is more favorable, loop
							curr_type_hit = FAVORABLE_HIT[(source_db, organism)]
							alignment = hits["hsps"][0]
							query_start = alignment["query_from"]
							query_end = alignment["query_to"]
							query_seq = alignment["qseq"]
							hit_start = alignment["hit_from"]
							hit_end = alignment["hit_to"]
							hit_seq = alignment["hseq"]
							midline = alignment["midline"]
							protein_id = hit["id"]
							accession = hit["accession"]
							description = hit["title"]
							sciname = hit["sciname"].lower()
							curr_hit = BlastResult(protein_id, accession, compare_id, source_db, scientific_name, identity, query_start, query_end,
													hit_start, hit_end, query_seq, midline, hit_seq, curr_type_hit)
		if curr_identity > 95.0:
			blast_results.append(curr_hit)

	return blast_results #TODO add other lists



def check_if_hit_in_db(blast_json, accessions_list):
	for hits in blast_json["BlastOutput2"][0]["report"]["results"]["search"]["hits"]:
		identity = hits["hsps"][0]["identity"] / hits["hsps"][0]["align_len"] * 100
		if identity >= 95.0:
			for hit in hits["description"]:
				if hit["accession"] in accessions_list:
					return hit["accession"]
	
	return False


def get_compare_path_accessions(compare_path):
	accession_list = []
	for record in SeqIO.parse(compare_path, 'fasta'):
		accession_list.append(record.id.split('.')[0])

	return accession_list


def get_source_db(protein_id):
	db_abbrev = protein_id.split('|')[0]
	if db_abbrev in list(ABBREV_DICT):
		return ABBREV_DICT[db_abbrev]
	
	return None


def get_rid(seq):
	page = requests.get(BLAST_REQUEST % seq)
	rid = re.findall(r'type="text" value="(.*)" id="rid"', page.text)[0]

	return {seq: rid}

def get_post_request_dict(rid):
	blast_post_request_dict = {
		"RID": [
			rid,
			rid
		],
		"ViewReport": "View+report",
		"FORMAT_OBJECT": "Alignment",
		"FORMAT_TYPE": "JSON2_S",
		"PSSM_FORMAT_TYPE": "Text",
		"BIOSEQ_FORMAT_TYPE": "ASN.1",
		"PSSM_SC_FORMAT_TYPE": "ASN.1",
		"ALIGNMENT_VIEW": "Pairwise",
		"SHOW_OVERVIEW": "on",
		"SHOW_LINKOUT": "on",
		"GET_SEQUENCE": "on",
		"MASK_CHAR": "2",
		"MASK_COLOR": "1",
		"DESCRIPTIONS": "100",
		"NUM_OVERVIEW": "100",
		"ALIGNMENTS": "100",
		"LINE_LENGTH": "60",
		"FORMAT_ORGANISM": "",
		"FORMAT_NUM_ORG": "1",
		"FORMAT_EQ_TEXT": "",
		"EXPECT_LOW": "",
		"EXPECT_HIGH": "",
		"PERC_IDENT_LOW": "",
		"PERC_IDENT_HIGH": "",
		"I_THRESH": [
			"",
			""
		],
		"CDD_RID": "",
		"CDD_SEARCH_STATE": "",
		"STEP_NUMBER": "",
		"CMD": "Get",
		"FORMAT_EQ_OP": "AND",
		"RESULTS_PAGE_TARGET": "Blast_Results_for_736311483",
		"QUERY_INFO": "Nucleotide+Sequence",
		"ENTREZ_QUERY": [
			"",
			""
		],
		"QUERY_INDEX": "0",
		"NUM_QUERIES": "1",
		"CONFIG_DESCR": "2,3,6,7,8,9,10,11,12",
		"BLAST_PROGRAMS": "blastn",
		"PAGE": "Nucleotides",
		"PROGRAM": "blastn",
		"MEGABLAST": "",
		"RUN_PSIBLAST": "",
		"BLAST_SPEC": "",
		"QUERY": "",
		"JOB_TITLE": "Nucleotide+Sequence",
		"QUERY_TO": "",
		"QUERY_FROM": "",
		"SUBJECTS_FROM": "",
		"SUBJECTS_TO": "",
		"EQ_TEXT": "",
		"ORGN": "",
		"EQ_MENU": "",
		"ORG_EXCLUDE": "",
		"PHI_PATTERN": "",
		"EXPECT": "",
		"DATABASE": "nt",
		"DB_GROUP": "",
		"SUBGROUP_NAME": "",
		"GENETIC_CODE": "",
		"WORD_SIZE": "",
		"MATCH_SCORES": "",
		"MATRIX_NAME": "",
		"GAPCOSTS": "",
		"MAX_NUM_SEQ": "",
		"COMPOSITION_BASED_STATISTICS": "",
		"NEWWIN": "",
		"SHORT_QUERY_ADJUST": "",
		"FILTER": "",
		"REPEATS": "",
		"ID_FOR_PSSM": "",
		"EXCLUDE_MODELS": "",
		"EXCLUDE_SEQ_UNCULT": "",
		"WP_PROTEINS": "",
		"SEQ_FROM_TYPE": "",
		"ENTREZ_QUERY_PRESET": "",
		"ENTREZ_QUERY_PRESET_EXCL": "",
		"NUM_ORG": "1",
		"LCASE_MASK": "",
		"TEMPLATE_TYPE": "",
		"TEMPLATE_LENGTH": "",
		"PSI_PSEUDOCOUNT": "",
		"DI_THRESH": "",
		"HSP_RANGE_MAX": "",
		"ADJUSTED_FOR_SHORT_QUERY": "",
		"MIXED_QUERIES": "",
		"MIXED_DATABASE": "",
		"BUILD_NAME": "",
		"ORG_DBS": "dbvers5",
		"WWW_BLAST_TYPE": ""
	}

	return blast_post_request_dict

def to_pickle(filename, value):#TODO delete
	with open(filename, 'wb') as handle:
		pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(file):
	with open(file, 'rb') as handle:
		data = pickle.load(handle)
	return data
