from fpdf import FPDF

from create_outputs.create_pdfs import CustomPDF, create_tables


def create_all_pdf(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word,
                     results_identical, alignments_identical, results_partial, results_motif, total_hits, toxin_results, options):
    pdf = CustomPDF.CustomPDF(options["file_name"])
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Courier", '', 10)

    if orf_list != '':
        create_tables.create_orf_table(pdf, orf_list, options)
        pdf.add_page()
    
    create_tables.create_top_allergens(pdf, sorted_list, options)
    pdf.add_page()

    create_tables.create_allergen_hits(pdf, orf_list, results_window, alignments_window, results_word, alignments_word)
    pdf.add_page()

    create_tables.create_top_celiac(pdf, results_partial)
    pdf.add_page()

    create_tables.create_celiac_hits(pdf, results_identical, alignments_identical, results_motif, total_hits)
    pdf.add_page()
    
    create_tables.create_top_toxins(pdf, toxin_results, options)
    pdf.output("output/"+options["file_name"]+"_"+options["timestr"]+'_'+options["search_type"]+"/Total_report.pdf")


def create_allergen_pdf(orf_list, sorted_list, results_window, alignments_window, results_word, alignments_word, options):
    pdf = CustomPDF.CustomPDF(options["file_name"])
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Courier", '', 10)

    if orf_list != '':
        create_tables.create_orf_table(pdf, orf_list, options)
        pdf.add_page()
    
    create_tables.create_top_allergens(pdf, sorted_list, options)
    pdf.add_page()

    create_tables.create_allergen_hits(pdf, orf_list, results_window, alignments_window, results_word, alignments_word)
    pdf.output("output/"+options["file_name"]+"_"+options["timestr"]+'_'+options["search_type"]+"/Allergen_report.pdf")

def create_celiac_pdf(orf_list, results_identical, alignments_identical, results_partial, results_motif, total_hits, options):
    pdf = CustomPDF.CustomPDF(options["file_name"])
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Courier", '', 10)

    if orf_list != '':
        create_tables.create_orf_table(pdf, orf_list, options)
        pdf.add_page()
    
    create_tables.create_top_celiac(pdf, results_partial)
    pdf.add_page()

    create_tables.create_celiac_hits(pdf, results_identical, alignments_identical, results_motif, total_hits)
    pdf.output("output/"+options["file_name"]+"_"+options["timestr"]+'_'+options["search_type"]+"/Celiac_report.pdf")


def create_toxin_pdf(orf_list, toxin_results, options):
    pdf = CustomPDF.CustomPDF(options["file_name"])
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Courier", '', 10)

    if orf_list != '':
        create_tables.create_orf_table(pdf, orf_list, options)
        pdf.add_page()
    
    create_tables.create_top_toxins(pdf, toxin_results, options)
    pdf.output("output/"+options["file_name"]+"_"+options["timestr"]+'_'+options["search_type"]+"/Toxin_report.pdf")
