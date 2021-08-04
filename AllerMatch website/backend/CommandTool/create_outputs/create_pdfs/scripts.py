import re

def check_output_folder(input_file, timestr):
    """
    Checks if the output folder exists, otherwise creates it
    """
    if not os.path.exists('output/'+input_file):
        os.makedirs('output/'+input_file)

def make_same_height(text, nlines, multiplier):

    if nlines == 1 and multiplier == 1:
        return text, nlines, multiplier
    elif nlines > 1 and nlines < multiplier:
        factor = multiplier - nlines
        text = text + ('\n' * factor)
        return text, nlines, 1
    elif nlines == multiplier:
        return text, nlines, 1
    elif nlines == 1:
        return text, nlines, multiplier
    else:
        print(nlines, multiplier, text)#TODO


def split_lines(text, length):
    new_text = ""
    multiply_height = 0
    chunks = [text[i:i+length] for i in range(0, len(text), length)]
    for c in chunks:
        new_text += c+'\n'
        multiply_height += 1
    new_text = new_text.strip()

    return new_text, multiply_height


def get_url_link(id, source):
    result = []
    if source == "Pubmed":
        for link in id.split(';'):
            result.append("https://pubmed.ncbi.nlm.nih.gov/%s" % link)
    elif source == "IEDB":
        for link in id.split(';'):
            result.append("https://www.iedb.org/epitope/%s" % link)
    return result


def get_unique_hits(list1, list2):
    unique_hits = set()
    for rw in list1:
        unique_hits.add(rw[0])
    for rw in list2:
        unique_hits.add(rw[0])
    
    unique_hits = list(unique_hits)
    unique_hits.sort(key=natural_keys)

    return unique_hits

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]