import os, requests, re, json, time, pickle
import pandas as pd 

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import date

class ProPepperRequest(object):
    def __init__(self):
        self.url = "https://www.propepper.net/epitope/list"
        self.post_request = {
            "draw": "1",
            "columns[0][data]": "0",
            "columns[0][name]": "",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "true",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "columns[1][data]": "1",
            "columns[1][name]": "",
            "columns[1][searchable]": "true",
            "columns[1][orderable]": "true",
            "columns[1][search][value]": "Tcell",
            "columns[1][search][regex]": "false",
            "columns[2][data]": "2",
            "columns[2][name]": "",
            "columns[2][searchable]": "true",
            "columns[2][orderable]": "true",
            "columns[2][search][value]": "",
            "columns[2][search][regex]": "false",
            "columns[3][data]": "3",
            "columns[3][name]": "",
            "columns[3][searchable]": "true",
            "columns[3][orderable]": "true",
            "columns[3][search][value]": "",
            "columns[3][search][regex]": "false",
            "columns[4][data]": "4",
            "columns[4][name]": "",
            "columns[4][searchable]": "true",
            "columns[4][orderable]": "true",
            "columns[4][search][value]": "",
            "columns[4][search][regex]": "false",
            "columns[5][data]": "5",
            "columns[5][name]": "",
            "columns[5][searchable]": "true",
            "columns[5][orderable]": "true",
            "columns[5][search][value]": "celiac disease",
            "columns[5][search][regex]": "false",
            "columns[6][data]": "6",
            "columns[6][name]": "",
            "columns[6][searchable]": "true",
            "columns[6][orderable]": "true",
            "columns[6][search][value]": "",
            "columns[6][search][regex]": "false",
            "columns[7][data]": "7",
            "columns[7][name]": "",
            "columns[7][searchable]": "true",
            "columns[7][orderable]": "true",
            "columns[7][search][value]": "",
            "columns[7][search][regex]": "false",
            "columns[8][data]": "8",
            "columns[8][name]": "",
            "columns[8][searchable]": "true",
            "columns[8][orderable]": "true",
            "columns[8][search][value]": "",
            "columns[8][search][regex]": "false",
            "columns[9][data]": "9",
            "columns[9][name]": "",
            "columns[9][searchable]": "true",
            "columns[9][orderable]": "true",
            "columns[9][search][value]": "",
            "columns[9][search][regex]": "false",
            "order[0][column]": "1",
            "order[0][dir]": "desc",
            "start": "0",
            "length": "10000",
            "search[value]": "",
            "search[regex]": "false"
        }
    

    def scrape_epitopes(self):
        r = requests.post(self.url, data=self.post_request)
        return r.json()



class AllergenOnlineRequest(object):
    url = ""

    def __init__(self, url: str):
        self.url = url

    def scrape(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'lxml')
        scripts = soup.select('script')
        scripts = [script for script in scripts]
        for script in scripts:
            if "celiac_database" in str(script):
                json_string = re.search(r'celiac_database\s*=\s*(.*?}])', str(script), flags=re.DOTALL)
        json_data = json.loads('{"data":' + json_string[1] + '}')
        
        return json_data



def main():
    print('Enter full path to the Sollid file:')
    sollid_path = input()

    propepper = ProPepperRequest()
    propepper_data = propepper.scrape_epitopes()

    allergenonline = AllergenOnlineRequest("http://allergenonline.org/celiacbrowse.shtml")
    allergenonline_data = allergenonline.scrape()
    
    allergenonline = AllergenOnlineRequest("http://www.allergenonline.org/celiacrefs.shtml")
    allergenonline_refs = allergenonline.scrape()

    sollid_df, propepper_df, allergenonline_df, allergenonlinerefs_df = create_dataframes(sollid_path, propepper_data["data"], allergenonline_data["data"], allergenonline_refs["data"])

    allergenonline_df = merge_pmids(allergenonline_df, allergenonlinerefs_df)

    output_file = save_db(propepper_df, allergenonline_df, sollid_df)
    print(output_file.name)
    set_new_db(output_file)


def create_dataframes(sollid_path, propepper_data, allergenonline_data, allergenonline_refs):
    sollid_df = pd.read_csv(sollid_path, sep='\t')
    sollid_df.dropna(axis = 0, how = 'all', inplace = True)
    sollid_df = sollid_df.reset_index(drop=True)
    propepper_df = pd.DataFrame(propepper_data)
    allergenonline_df = pd.DataFrame(allergenonline_data)
    allergenonlinerefs_df = pd.DataFrame(allergenonline_refs)

    return sollid_df, propepper_df, allergenonline_df, allergenonlinerefs_df


def merge_pmids(allergenonline_df, references_df):
    ref_dict = {}
    for index, row in references_df.iterrows():
        ref_dict[str(row["id"])] = str(row["pubmed"])
    ref_dict['90'] = "32728397"

    pubmed_ids = []
    for index, row in allergenonline_df.iterrows():
        ref_ids = row["refs"].split(',')
        pmid = [] 
        for ref in ref_ids:
            if ref in ref_dict.keys():
                pmid.append(ref_dict[ref])
        pubmed_ids.append(';'.join(pmid))
    
    allergenonline_df["PMID"] = pubmed_ids
     
    return allergenonline_df   


def save_db(propepper_df, allergenonline_df, sollid_df):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    script_dir = Path(os.path.dirname(__file__))
    rel_path = "data/Celiac_epitopes_"+timestr+".fasta"
    script_dir = str(script_dir.parent)
    abs_file_path = os.path.join(script_dir, rel_path)

    counter = 1

    with open(abs_file_path, 'w') as output_file:
        for index, row in propepper_df.iterrows():
            output_file.write('>' + '\t'.join([str(counter), row["3"], str(row["7"]), "ProPepper", "IEDB", str(row["9"])]) + '\n')
            output_file.write(row["4"] + '\n')
            counter += 1
        for index, row in allergenonline_df.iterrows():
            output_file.write('>' + '\t'.join([str(counter), row["Description"].replace('\r\n', ' '), str(row["HLADQ"]), "AllergenOnline", "Pubmed", str(row["PMID"])]) + '\n')
            output_file.write(row["Sequence"] + '\n')
            counter += 1
        for index, row in sollid_df.iterrows():
            output_file.write('>' + '\t'.join([str(counter), row["Name"], str(row["HLADQ"]), "Sollid", "Pubmed", str(row["PMID"])]) + '\n')
            output_file.write(row["Sequence"] + '\n')
            counter += 1
    
    return output_file 


def set_new_db(output_file):
    script_dir = Path(os.path.dirname(__file__))
    rel_path = 'data/current_db.pickle'
    script_dir = str(script_dir.parent)
    abs_file_path = os.path.join(script_dir, rel_path)

    current_db = {"Current_DB": "/celiac/data/"+output_file.name.split('/')[-1],  "update_date": date.today().strftime("%m/%d/%Y")}
    with open(abs_file_path, 'wb') as file:
        pickle.dump(current_db, file)

if __name__ == "__main__":
    main()