# Allermatch&trade; command line tool
  
## Description
Allermatch-command-line-tool is a Python tool for the risk assesment of novel proteins introduced in genetically modified food. It will analyze the potential allergenicity, toxicity or celiac sensitivity by using different search methods for sequence identiy to known allergens/toxins sequences or celiac epitopes. Allermatch-command-line-tool is an extension of the online [Allermatch tool](http://allermatch.org/). This command line tool is split up in 4 modules:

#### allergen_search.py
allergen_search uses a combination of three different curated datasources for finding sequence similarities. These datasources are: allergens from [UniProt](https://www.uniprot.org/docs/allergen), [WHO/IUIS Allergen Nomenclature](http://www.allergen.org/) and [COMPARE DB](http://db.comparedatabase.org/). For finding potential allergens Allermatch uses three different search methods, which are according to the current recommendations of FAO/WHO Codex alimentarius and EFSA's guidelines:
* 80aa sliding window approach
* Wordmatch
* Full FASTA36 alignment


#### celiac_search.py
celiac_search uses a combination of three different curated datasources to find similarities to known celiac restricted epitopes. These databases are: [listing of celiac disease-relevant gluten epitopes](https://pubmed.ncbi.nlm.nih.gov/31735991/) by Sollid and co-authors, [ProPrepper](https://www.propepper.net/epitope) and [AllergenOnline](http://www.allergenonline.org/celiacbrowse.shtml). For celiac risk assesment Allermatch uses three different search methods, which are according to the current recommendations of EFSA's guidelines:
* Identical epitope match
* Partial epitope match
* Q/E-X1-P-X2 motif search


#### toxic_search.py
toxic_search uses sequences from UniProt's [Animal toxin annotation project](https://www.uniprot.org/program/Toxins). For finding potential toxins Allermatch only uses a full FASTA36 alignment search. There are no official guidelines yet for the risk assesment of toxins.


#### app.py
A combination of all of the above modules.


## Installation 

### Prerequisites
* Linux
* Python3
* Pip3
* Git

#### Set-up
1. `git clone https://git.wur.nl/jordan.dekker/allermatch-command-line.git`
2. Go to the folder: `cd allermatch-command-line`
3. `pip install -r requirements.txt`
4. Install FASTA36: 
    * `cd fasta-36.3.8h/src`
    * `make -f ../make/Makefile.linux_sse2 all`


## Usage

```bash
$ python app.py {options}
```
Options.

| Option         |default | description                                                                                                               |
|----------------|--------|---------------------------------------------------------------------------------------------------------------------------|
| -i --input     |n/a     | Path to the query input file                                                                                              |
| -t --table     |1       | Which genetic code table to use. More info: [NCBI](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi)              |
| -o --orf       |        | Use if you want to search between start and stop coding(default is to search between stop codons)                         |
| -l --length    |8       | Minimum peptide length to be a ORF (only applicable for app.py & allergen_search.py)                                      |
| -w --word      |6       | Identical word length (only applicable for app.py & allergen_search.py)                                                   |
| -c --cutoff    |35      | Sliding window minimum identity (only applicable for app.py & allergen_search.py)                                         |
| -p --propeptide|        | Use if you want to search in the database with signal- and propeptides(default is database without)                       |
| -d --database  |0(all)  | Which celiac database to use(0=all, 1=Sollid, 2=ProPepper, 3=AllergenOnline, 4=Sollid&PP, 5=Sollid&AO, 6=AO&PP) (only applicable for app.py & celiac_search.py)           |

#### output
Output can be found in the /ouput folder.

## Examples

To run app.py with all default parameter:
```bash
$ python app.py -i /home/name/Documents/input.fasta
```

To run app.py with a minimum exact word length at 7, minimum sliding window identity at 30 and search ORFs between start- and stop codon:
```bash
$ python app.py -i /home/name/Documents/input.fasta -w 7 -c 45 -o
```

To run celiac_search.py and only compare to Sollid epitopes:
```bash
$ python celiac_search.py -i /home/name/Documents/input.fasta -d 1
```


## Contact Information
*  Jordan Dekker jordan.dekker@wur.nl

## Update databases
Not needed, and only needed to be run periodically.

#### Update allergen database(AllermatchDB)
If you want to update the AllermatchDB:
1. `python allergens/data/create_allergen_db.py`
2. Enter the full path to the COMPARE DB
    * (2020 version is located at /allergens/data/COMPARE-2020-FastA-Seq.txt
    * If available, download new database from http://db.comparedatabase.org/
3. Choose if you want to BLAST the leftovers(y/n)(this process will take a long time.)

##### Update celiac database.
If you want to update the celiac database:
1. `python celiac/create_database/create_db.py`
2. Enter the full path to the Sollid tsv file:
    * Located in /celiac/create_database/data/Sollid.tsv
    * Update manually if needed

##### Update toxin database.
If you want to update the toxin database:
1. `python toxins/data/create_toxin_db.py `
