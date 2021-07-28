import os, pickle

from create_outputs.create_pdfs import scripts
from allergens import database
from celiac import celiac_database
from toxins import tox_database

LOC = os.getcwd()+"/CommandTool"

def create_orf_table(pdf, orf_list, options):
    genetic_code_dict = load_pickle(LOC + "/create_outputs/create_pdfs/the_genetic_codes_dict.pickle")
    type_orf_search = load_pickle(LOC + "/create_outputs/create_pdfs/type_orf_search.pickle")
    top = pdf.y

    effective_page_width = pdf.w-2*pdf.l_margin
    effective_page_height = pdf.h-2*pdf.b_margin

    pdf.set_font('Arial', 'BU', 16)
    pdf.cell(effective_page_width,0.0,'Open Reading Frames', align='C')
    top += 5

    pdf.set_font('Arial', '', 10)
    pdf.x = 10
    pdf.y = top
    with open(LOC + "/create_outputs/create_pdfs/pdf_text/orf_intro.txt", 'r') as orf_text:
        text = orf_text.read()
    pdf.multi_cell(effective_page_width, 3.5, (text.replace("ENTER", '\n') % 
                  (genetic_code_dict[str(options["table"])]+"' (table number "+str(options["table"])+')', type_orf_search[options["orf_type"]], str(options["word_length"]), str(len(orf_list)))))
    top += 30

    new_top = pdf.create_orf_header(top)

    pdf.set_font('Courier', '', 8)
    for orf in orf_list:
        id = orf[0]
        sequence = orf[1]
        height_id, height_sequence = 1, 1
        if len(sequence) > 50:
            sequence, height_sequence = scripts.split_lines(orf[1], 50)
        if len(id) > 10:
            id, height_id = scripts.split_lines(orf[0], 10)

        multiply_height = max([height_id, height_sequence])
        new_top = pdf.check_page_end(new_top, 5*multiply_height)

        pdf.x = 10
        new_x = pdf.create_multi_cell_line(width = 20, height = 5, text = id, border = 1, y = new_top, x = pdf.x, nlines = height_id, multiplier = multiply_height)
        new_x = pdf.create_multi_cell_line(width = 90, height = 5, text = sequence, border = 1, y = new_top, x = new_x, nlines = height_sequence, multiplier = multiply_height)
        new_x = pdf.create_multi_cell_line(width = 20, height = 5, text = str(orf[2]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)
        new_x = pdf.create_multi_cell_line(width = 30, height = 5, text = str(orf[5])+'-'+str(orf[6]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)
        new_x = pdf.create_multi_cell_line(width = 25, height = 5, text = "%s(%s)" % (orf[3], orf[4]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)   
        
        new_top = pdf.check_page_end(new_top, 5*multiply_height)
        new_top += 5 * multiply_height


def create_top_allergens(pdf, sorted_list, options):
    db = database.database_loaded[options["peptides_removed"]]
    top = pdf.y
    effective_page_width = pdf.w-2*pdf.l_margin
    effective_page_height = pdf.h-2*pdf.b_margin
    with open(LOC + "/create_outputs/create_pdfs/pdf_text/allergen_intro.txt", 'r') as allergen_text:
        text = allergen_text.read()
    paragraphs = text.split('\n\n')
    curr_db = load_pickle(LOC+ "/allergens/data/db/current_db.pickle")
    last_update = curr_db["update_date"]

    pdf.set_font('Arial', 'BU', 20)
    effective_page_width=pdf.w-2*pdf.l_margin
    pdf.cell(effective_page_width,0.0,'Allergen Results', align='C')
    top+= 12
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "Allergen database.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.5, paragraphs[0].replace("ENTER", '\n\n') % (str(len(db)), last_update))
    top += 30
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "FASTA.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.5, paragraphs[1])
    top += 10
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "Identity search to known allergens.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.4, paragraphs[2].replace("ENTER", '') % (options["window_cutoff"], options["word_length"], options["word_length"]))
    top += 60
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 14)
    pdf.cell(effective_page_width,0.0,'Top 100 full-FASTA search results', align='C')
    top += 1
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width,10,'Based on E-Value', align='C')
    new_top = top + 15

    for hit, i in zip(sorted_list[:100], range(1,101)):
        new_top = pdf.check_page_end(new_top, 40)
        new_top = pdf.create_top_allergens_header(new_top)
        
        pdf.x = 10
        pdf.set_font('Courier', 'B', 16)
        new_x = pdf.create_multi_cell_line(width = 15, height = 5, text = str(i), border = 0, y = new_top, x = pdf.x)
        pdf.set_font('Courier', '', 8)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = hit.get_query_id(), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_query_length()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 32.5, height = 5, text = hit.get_hit_id(), border = 1, y = new_top, x = new_x)
        pdf.x = new_x
        pdf.y = new_top
        pdf.set_text_color(0, 0, 255)
        pdf.cell(20, 5, db[hit.get_hit_id()]["Accession id"] , 1, 1, 'L', False, db[hit.get_hit_id()]["Hyperlink"])
        new_x += 20
        pdf.set_text_color(0, 0, 0)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_hit_length()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_e_value()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_overlap()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_identity()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_recalculated_ident()), border = 1, y = new_top, x = new_x)
        
        pdf.ln(2)

        pdf.set_font('Courier', '', 10)
        if hit.get_formatted_alignment() != "":
            pdf.x = 25
            pdf.multi_cell(190,3,hit.get_formatted_alignment())
            nlines = hit.get_formatted_alignment().count('\n')
        else:
            pdf.x = 25
            pdf.multi_cell(190,3,hit.get_alignment())
            nlines = hit.get_alignment().count('\n')
        
        new_top += 10 + (4 * nlines)


def create_allergen_hits(pdf, orf_list, results_window, alignments_window, results_word, alignments_word):
    top = pdf.y
    effective_page_width = pdf.w-2*pdf.l_margin
    effective_page_height = pdf.h-2*pdf.b_margin
    unique_hits = scripts.get_unique_hits(results_window, results_word)

    pdf.set_font('Arial', 'BU', 18)
    pdf.cell(effective_page_width,0.0,'Exact word and sliding window results', align='C')
    top += 1
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width,10,'Shown per ORF', align='C')
    new_top = top + 15

    for hit in unique_hits:
        new_top = pdf.check_page_end(new_top, 40)
        for orf in orf_list:
            if hit == orf[0]:
                pdf.y = new_top
                pdf.x = 10
                pdf.set_font('Arial', 'BU', 14)
                pdf.cell(effective_page_width,0.0,orf[0], align='C')            
                new_top += 10
        if hit in [rw[0] for rw in results_word]:
            pdf.set_font('Courier', 'BU', 10)
            pdf.x = 10
            pdf.y = new_top
            pdf.multi_cell(100, 0, "Exact word results:")
            new_top += 3
        for rw in results_word:
            if hit == rw[0]:
                new_top = pdf.check_page_end(new_top, 50)
                new_top =pdf.create_wordhit_header(new_top)

                description = rw[3]
                species = rw[6]
                height_desc, height_spec = 1, 1
                if len(description) > 25:
                    description, height_desc = scripts.split_lines(description, 25)
                if len(species) > 25:
                    species, height_spec = scripts.split_lines(species, 25)
                multiply_height = max([height_desc, height_spec])

                pdf.set_font('Courier', '', 8)
                pdf.x = 10
                new_x = pdf.create_multi_cell_line(width = 30, height = 5, text = rw[1], border = 1, y = new_top, x = pdf.x, nlines = 1, multiplier = multiply_height)
                pdf.x = new_x
                pdf.y = new_top
                pdf.set_text_color(0, 0, 255)
                pdf.cell(25, 5*multiply_height, rw[5], 1, 1, 'C', False, rw[9])
                new_x += 25
                pdf.set_text_color(0, 0, 0)
                new_x = pdf.create_multi_cell_line(width = 45, height = 5, text = description, border = 1, y = new_top, x = new_x, nlines = height_desc, multiplier = multiply_height)
                new_x = pdf.create_multi_cell_line(width = 45, height = 5, text = species, border = 1, y = new_top, x = new_x, nlines = height_spec, multiplier = multiply_height)
                new_x = pdf.create_multi_cell_line(width = 30, height = 5, text = str(rw[2]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)
                new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(rw[4]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)
                pdf.ln(2)

                pdf.set_font('Courier', '', 10)
                for al in alignments_word[(hit, rw[1])]:
                    pdf.multi_cell(190,3,al.upper())
                    pdf.ln(3)
                    new_top += 12
                new_top += 5 + (5*multiply_height)
                
        if hit in [rw[0] for rw in results_window]:
            pdf.x = 10
            pdf.y = new_top
            pdf.set_font('Courier', 'BU', 10)
            pdf.multi_cell(100, 5, "Sliding window results:")
            new_top += 5
        for rw in results_window:
            if hit == rw[0]:
                new_top = pdf.check_page_end(new_top, 50)
                new_top = pdf.create_window_header(new_top)

                description = rw[9]
                species = rw[8]
                height_desc, height_spec = 1, 1
                if len(description) > 30:
                    description, height_desc = scripts.split_lines(description, 30)
                if len(species) > 30:
                    species, height_spec = scripts.split_lines(species, 30)
                multiply_height = max([height_desc, height_spec])

                pdf.set_font('Courier', '', 8)
                pdf.x = 10
                new_x = pdf.create_multi_cell_line(width = 30, height = 5, text = rw[1], border = 1, y = new_top, x = pdf.x, nlines = 1, multiplier = multiply_height)
                pdf.x = new_x
                pdf.y = new_top
                pdf.set_text_color(0, 0, 255)
                pdf.cell(25, 5*multiply_height, rw[7], 1, 1, 'C', False, rw[11])
                new_x += 25
                pdf.set_text_color(0, 0, 0)
                new_x = pdf.create_multi_cell_line(width = 45, height = 5, text = description, border = 1, y = new_top, x = new_x, nlines = height_desc, multiplier = multiply_height)
                new_x = pdf.create_multi_cell_line(width = 45, height = 5, text = species, border = 1, y = new_top, x = new_x, nlines = height_spec, multiplier = multiply_height)
                new_x = pdf.create_multi_cell_line(width = 30, height = 5, text = str(rw[3]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)
                new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(rw[4]), border = 1, y = new_top, x = new_x, nlines = 1, multiplier = multiply_height)
                pdf.ln(4)
                new_top += 8 * multiply_height  

                n_alignments = 0
                for al in alignments_window:
                    if al.get_query_id() == hit and al.get_hit_id() == rw[1]:
                        nlines = 0
                        new_top = pdf.check_page_end(new_top, 50)
                        pdf.y = new_top

                        pdf.set_font("Arial", 'B', 10)
                        pdf.multi_cell(150, 3, "Alignments containing "+str(al.get_no_slices())+" window(s):")
                        for key in al.get_window_identities():
                            pdf.multi_cell(150,3,"(%s) %s%% identity" % (key, al.get_window_identities()[key]))
                            nlines += 1
                        pdf.ln(1)
                        pdf.set_font('Courier', '', 10)
                        if al.get_formatted_alignment() != "":
                            pdf.multi_cell(190,3,al.get_formatted_alignment())
                            nlines += al.get_formatted_alignment().count('\n')
                        else:
                            pdf.multi_cell(190,3,al.get_alignment())
                            nlines += al.get_alignment().count('\n')
                        n_alignments += 1
                        new_top += 12
                        new_top += 3*nlines
                new_top += 5*n_alignments

def create_top_celiac(pdf, results_partial):
    top = pdf.y
    db = celiac_database.import_database("")
    sorted_list = sorted(results_partial, key = lambda x: float(x.e_value))
    curr_db = load_pickle(LOC+ "/celiac/data/current_db.pickle")
    last_update = curr_db["update_date"]

    pdf.set_font('Arial', 'BU', 20)
    effective_page_width=pdf.w-2*pdf.l_margin
    pdf.cell(effective_page_width,0.0,'Celiac Results', align='C')
    top+= 12
    pdf.y = top
    pdf.x = 10
    with open(LOC + "/create_outputs/create_pdfs/pdf_text/celiac_intro.txt", 'r') as celiac_text:
        text = celiac_text.read()
    paragraphs = text.split('\n\n')
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "Celiac database.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.5, paragraphs[0].replace("ENTER", '\n\n') % last_update)
    top += 20
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "FASTA.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.5, paragraphs[1])
    top += 10
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "Identity search to known celiac epitopes.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.4, paragraphs[2].replace("ENTER", ''))
    top += 60
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 14)
    pdf.cell(effective_page_width,0.0,'Top 100 epitope match results', align='C')
    top += 1
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width,10,'Based on E-Value', align='C')
    new_top = top + 15

    for hit, i in zip(sorted_list[:100], range(1,101)):
        new_top = pdf.check_page_end(new_top, 40)
        id = hit.get_query_id()
        name = db[hit.get_hit_id()]["Name"]
        height_id, height_name = 1, 1
        if len(id) > 10:
            id, height_id = scripts.split_lines(hit.get_query_id(), 10)
        if len(name) > 20:
            name, height_name = scripts.split_lines(db[hit.get_hit_id()]["Name"], 20)
        multiply_height = max([height_id, height_name])

        new_top = pdf.create_top_celiac_header(new_top)
        pdf.x = 5
        pdf.set_font('Courier', 'B', 16)
        new_x = pdf.create_multi_cell_line(width = 15, height = 5, text = str(i), border = 0, y = new_top, x = pdf.x, nlines= 1, multiplier= multiply_height)
        pdf.set_font('Courier', '', 8)
        new_x = pdf.create_multi_cell_line(width = 20, height = 5, text = id, border = 1, y = new_top, x = new_x, nlines= height_id, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 12.5, height = 5, text = str(hit.get_query_length()), border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 40, height = 5, text = name, border = 1, y = new_top, x = new_x, nlines= height_name, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 12.5, height = 5, text = str(hit.get_hit_length()), border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_e_value()), border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_overlap()), border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_identity()), border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 19.5, height = 5, text = str(hit.get_similar()), border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_x = pdf.create_multi_cell_line(width = 26, height = 5, text = db[hit.get_hit_id()]["Database"], border = 1, y = new_top, x = new_x, nlines= 1, multiplier= multiply_height)
        new_top += 5 * multiply_height

        links = scripts.get_url_link(db[hit.get_hit_id()]["Source_id"], db[hit.get_hit_id()]["Source"])
        pdf.set_text_color(0, 0, 255)
        for link in links:
            pdf.x=20
            pdf.cell(183, 5, link, 1, 1, 'C', False, link)
            new_top += 5
        pdf.ln(2)
        pdf.set_text_color(0, 0, 0)
        pdf.x = 25
        pdf.set_font('Courier', '', 10)
        pdf.multi_cell(160, 3, hit.get_alignment())
        new_top += 15

def create_celiac_hits(pdf, results_identical, alignments_identical, results_motif, total_hits):
    new_top = pdf.y
    unique_hits = scripts.get_unique_hits(results_identical, results_motif)
    effective_page_width=pdf.w-2*pdf.l_margin

    for hit in unique_hits:
        new_top = pdf.check_page_end(new_top, 40)
        pdf.y = new_top
        pdf.x = 10
        pdf.set_font('Arial', 'BU', 14)
        pdf.cell(effective_page_width,0.0,hit, align='C')
        new_top += 10

        if hit in [ri[0] for ri in results_identical]:
            pdf.y = new_top
            pdf.set_font('Courier', 'BU', 10)
            pdf.x = 10
            pdf.multi_cell(100, 0, "Exact epitope match results:")
            new_top += 5
        
        if hit in [rm[0] for rm in results_motif]:
            pdf.y = new_top
            pdf.set_font('Courier', 'BU', 10)
            pdf.x = 10
            pdf.multi_cell(100, 0, "Motif results:")
            new_top += 5
        for rm in results_motif:
            if hit == rm[0]:
                new_top = pdf.create_motif_header(new_top)
                pdf.set_font('Courier', '', 8)
                pdf.x = 10
                pdf.y = new_top
                new_x = pdf.create_multi_cell_line(width = 80, height = 5, text = rm[0], border = 1, y = new_top, x = pdf.x)
                new_x = pdf.create_multi_cell_line(width = 25, height = 5, text = rm[1], border = 1, y = new_top, x = new_x)
                new_x = pdf.create_multi_cell_line(width = 30, height = 5, text = str(rm[2])+'-'+str(rm[3]), border = 1, y = new_top, x = new_x)
                new_x = pdf.create_multi_cell_line(width = 60, height = 5, text = "%s (%s/%s)" % (rm[4], rm[5], str(total_hits)), border = 1, y = new_top, x = new_x)
                pdf.ln(2)
                pdf.set_font('Courier', '', 10)
                pdf.multi_cell(160, 3, rm[7])
                new_top += 20


def create_top_toxins(pdf, results_toxins, options):
    db = tox_database.database_loaded[options["peptides_removed"]]
    top = pdf.y
    sorted_list = sorted(results_toxins, key = lambda x: float(x.e_value))
    curr_db = load_pickle(LOC+ "/toxins/data/current_db.pickle")
    last_update = curr_db["update_date"]

    pdf.set_font('Arial', 'BU', 20)
    effective_page_width=pdf.w-2*pdf.l_margin
    pdf.cell(effective_page_width,0.0,'Toxin Results', align='C')
    top+= 12
    pdf.y = top
    pdf.x = 10
    with open(LOC + "/create_outputs/create_pdfs/pdf_text/toxin_intro.txt", 'r') as toxin_text:
        text = toxin_text.read()
    paragraphs = text.split('\n\n')
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "Toxin database.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.5, paragraphs[0].replace("ENTER", '\n\n') % (str(len(db)),last_update))
    top += 20
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "FASTA.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.5, paragraphs[1])
    top += 10
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 10)
    pdf.multi_cell(effective_page_width, 3.5, "Identity search to known toxins.")
    top += 4
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width, 3.4, paragraphs[2].replace("ENTER", ''))
    top += 20
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', 'BU', 14)
    pdf.cell(effective_page_width,0.0,'Top 100 full-FASTA search results', align='C')
    top += 1
    pdf.y = top
    pdf.x = 10
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(effective_page_width,10,'Based on E-Value', align='C')
    new_top = top + 15

    for hit, i in zip(sorted_list[:100], range(1,101)):
        new_top = pdf.check_page_end(new_top, 40)
        new_top = pdf.create_top_toxins_header(new_top)
        
        pdf.x = 10
        pdf.set_font('Courier', 'B', 16)
        new_x = pdf.create_multi_cell_line(width = 15, height = 5, text = str(i), border = 0, y = new_top, x = pdf.x)
        pdf.set_font('Courier', '', 8)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = hit.get_query_id(), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_query_length()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 35, height = 5, text = hit.get_hit_id(), border = 1, y = new_top, x = new_x)
        pdf.x = new_x
        pdf.y = new_top
        pdf.set_text_color(0, 0, 255)
        pdf.cell(17.5, 5, db[hit.get_hit_id()]["Accession id"] , 1, 1, 'L', False, db[hit.get_hit_id()]["Hyperlink"])
        new_x += 17.5
        pdf.set_text_color(0, 0, 0)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_hit_length()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_e_value()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_overlap()), border = 1, y = new_top, x = new_x)
        new_x = pdf.create_multi_cell_line(width = 17.5, height = 5, text = str(hit.get_identity()), border = 1, y = new_top, x = new_x)
        
        pdf.ln(2)

        pdf.set_font('Courier', '', 10)
        if hit.get_formatted_alignment() != "":
            pdf.x = 25
            pdf.multi_cell(190,3,hit.get_formatted_alignment())
            nlines = hit.get_formatted_alignment().count('\n')
        else:
            pdf.x = 25
            pdf.multi_cell(190,3,hit.get_alignment())
            nlines = hit.get_alignment().count('\n')
        
        new_top += 10 + (4 * nlines)


def load_pickle(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data