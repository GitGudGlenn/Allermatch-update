from fpdf import FPDF
from datetime import date

class CustomPDF(FPDF):

    file_name = ""

    def __init__(self, file_name):
        super(CustomPDF, self).__init__()
        self.file_name = file_name
    
    def header(self):
        self.image('/home/glenn/Desktop/allermatch-website-revamp/AllerMatch-website/backend/CommandTool/create_outputs/create_pdfs/allermatch_logo.png', 10, 12, 60)
        self.image('/home/glenn/Desktop/allermatch-website-revamp/AllerMatch-website/backend/CommandTool/create_outputs/create_pdfs/wur_logo.png', 80, 14, 60)
        self.set_font('Arial', '', 12)

        today = date.today()
        self.cell(150)
        self.cell(0, 5, today.strftime("%b-%d-%Y"), ln=1)
        self.cell(150)
        self.cell(0, 5, 'WFSR', ln=1)
        self.cell(150)
        self.cell(0, 5, 'Report: '+self.file_name, ln=1)
        
        self.ln(20)
        
    def footer(self):
        self.set_y(-10)
        
        self.set_font('Arial', 'I', 8)
        
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')
    
    def create_multi_cell_line(self, width, height, text, border, y, x, nlines = 1, multiplier = 1):
        self.y = y
        self.x = x
        text, nlines, multiplier = make_same_height(text, nlines, multiplier)
        self.multi_cell(width, height*multiplier, text, border)
        return x + width
    
    def check_page_end(self, top, height):
        effective_page_height = self.h-2*self.b_margin

        if top + height > effective_page_height:
            self.add_page()
            return 45.0
        return top

    def create_orf_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 10
        new_x = self.create_multi_cell_line(width = 20, height = 5, text = "ID", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 90, height = 5, text = "Sequence", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 20, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 30, height = 5, text = "Position", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 25, height = 5, text = "Strand(frame)", border = 1, y = top, x = new_x)
        
        top += 5
        return top
    
    def create_top_allergens_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 25
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "ID", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 32.5, height = 5, text = "Hit ID", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 20, height = 5, text = "Accession", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "E-value", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Overlap", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Identity", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Recalc", border = 1, y = top, x = new_x)
        
        top += 5
        return top
    
    def create_wordhit_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 10
        new_x = self.create_multi_cell_line(width = 30, height = 5, text = "Name", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 25, height = 5, text = "Accession ID", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 45, height = 5, text = "Description", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 45, height = 5, text = "Species", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 30, height = 5, text = "No exact words", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Hit %", border = 1, y = top, x = new_x)

        top += 5
        return top
    
    def create_window_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 10
        new_x = self.create_multi_cell_line(width = 30, height = 5, text = "Name", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 25, height = 5, text = "Accession ID", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 45, height = 5, text = "Description", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 45, height = 5, text = "Species", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 30, height = 5, text = "No windows", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Hit %", border = 1, y = top, x = new_x)

        top += 5
        return top

    def create_top_celiac_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 20
        new_x = self.create_multi_cell_line(width = 20, height = 5, text = "ID", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 12.5, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 40, height = 5, text = "Hit ID", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 12.5, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "E-value", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Overlap", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Identity", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 19.5, height = 5, text = "Similarity", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 26, height = 5, text = "Database", border = 1, y = top, x = new_x)

        top += 5
        return top
    
    def create_motif_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 10
        new_x = self.create_multi_cell_line(width = 80, height = 5, text = "ID", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 25, height = 5, text = "Motif", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 30, height = 5, text = "Range", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 60, height = 5, text = "Motif Occurence", border = 1, y = top, x = new_x)

        top += 5
        return top
    
    def create_top_toxins_header(self, top):
        self.set_font('Courier', 'B', 8)
        self.y = top
        self.x = 25
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "ID", border = 1, y = top, x = self.x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 35, height = 5, text = "Hit ID", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Accession", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Length", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "E-value", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Overlap", border = 1, y = top, x = new_x)
        new_x = self.create_multi_cell_line(width = 17.5, height = 5, text = "Identity", border = 1, y = top, x = new_x)
        
        top += 5
        return top

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
