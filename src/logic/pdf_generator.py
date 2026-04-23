import io
from pypdf import PdfWriter, PdfReader
from fpdf import FPDF, XPos, YPos
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image

class ASEM_PDF(FPDF):
    def header(self):
        """Κεφαλίδα με λογότυπο και τίτλο - Center Aligned με το Logo"""
        base_dir = Path(__file__).parent.parent.parent
        logo_path = str(base_dir / "assets" / "logo.png")
        try: 
            self.image(logo_path, 10, 8, 55) 
        except: 
            pass
        
        # 1. Τίτλος (Center Aligned με το σώμα του logo - y:13)
        self.set_font('ArialGreek', 'B', 20) 
        self.set_text_color(0, 82, 161)
        self.set_xy(170, 10) 
        self.cell(117, 8, "Οικονομική Πρόταση", align='R')
        self.set_text_color(0)
        self.ln(20)

def draw_terms_footer(pdf, terms, global_discount):
    """Σχεδιασμός footer με όρους και προϋποθέσεις"""
    footer_start_y = 160
    if pdf.get_y() > footer_start_y:
        pdf.add_page()
    pdf.set_y(footer_start_y)
    pdf.set_draw_color(0, 82, 159)
    pdf.set_line_width(0.5)
    pdf.line(10, footer_start_y, 287, footer_start_y)
    pdf.ln(4)
    pdf.set_font('ArialGreek', 'B', 9)
    pdf.set_text_color(0, 82, 161)
    pdf.cell(0, 5, "ΟΡΟΙ ΚΑΙ ΠΡΟΫΠΟΘΕΣΕΙΣ ΠΡΟΣΦΟΡΑΣ", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    pdf.set_font('ArialGreek', '', 8)
    pdf.set_text_color(50, 50, 50)
    validity = f"• Ισχύς προσφοράς: Η προσφορά ισχύει για {terms.get('validity', '30')} ημερολογιακές ημέρες."
    payment = f"• Τρόπος πληρωμής: {terms.get('payment', '-')}"
    delivery = f"• Τρόπος παράδοσης: {terms.get('delivery', '-')}"
    if global_discount == 0:
        price_info = "• Οι αναγραφόμενες τιμές είναι προ Φ.Π.Α."
    else:
        price_info = f"• Οι τιμές είναι μετά έκπτωση και είναι προ Φ.Π.Α."
    for term in [validity, payment, delivery, price_info]:
        pdf.cell(0, 4, term, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    disclaimer = f"* {terms.get('disclaimer_text', 'Η ASEM διατηρεί το δικαίωμα να προβαίνει σε αλλαγές τιμών χωρίς προηγούμενη ειδοποίηση μετά το πέρας της προσφοράς.')}"
    pdf.cell(0, 4, disclaimer, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

def unify_subcategories(val, keywords_det, keywords_dry):
    s = str(val).lower()
    has_det = any(k.lower() in s for k in keywords_det)
    has_dry = any(k.lower() in s for k in keywords_dry)
    if has_det or has_dry:
        return "Απορρυπαντικά & Στεγνωτικά Πλυντηρίου"
    return val

def draw_category_header(pdf, cat_text, color, y_pos):
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('ArialGreek', 'B', 11)
    pdf.set_xy(10, y_pos)
    pdf.cell(277, 7, f"  {cat_text}", fill=True, ln=1)
    return 7 

def draw_subcategory_header(pdf, subcat_text, y_pos):
    pdf.set_fill_color(110, 181, 219)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('ArialGreek', 'B', 9.5)
    pdf.set_xy(10, y_pos)
    pdf.cell(277, 5.5, f"  {subcat_text}", fill=True, ln=1)
    return 5.5 

def draw_product(pdf, vars_df, start_x, start_y, block_width, col_m, col_k, discount, base_dir):
    img_code = str(vars_df['ΚΩΔΙΚΟΣ'].iloc[0]).strip()
    if img_code.endswith('.0'):
       img_code = img_code[:-2]
    img_path = base_dir / "assets" / "pictures" / f"{img_code}.png"
    
    CANVAS_SIZE = 28
    if img_path.exists():
        try:
            with Image.open(img_path) as im:
                orig_w, orig_h = im.size
            
            aspect = orig_w / orig_h if orig_h > 0 else 1
            
            if aspect > 1:
                render_w = CANVAS_SIZE
                render_h = CANVAS_SIZE / aspect
                pos_x = start_x
                pos_y = (start_y + 1) + (CANVAS_SIZE - render_h) / 2
            else:
                render_h = CANVAS_SIZE
                render_w = CANVAS_SIZE * aspect
                pos_x = start_x + (CANVAS_SIZE - render_w) / 2
                pos_y = start_y + 1
            
            pdf.image(str(img_path), x=pos_x, y=pos_y, w=render_w, h=render_h)
        except:
            pdf.image(str(img_path), x=start_x, y=start_y + 1, w=28, h=0)
    else:
        pdf.set_draw_color(200, 200, 200)
        pdf.set_fill_color(245, 245, 245)
        pdf.rect(start_x + 3, start_y + 1 + 3, 22, 22, style='FD')
    content_x = start_x + 24
    pdf.set_xy(content_x, start_y + 3)
    pdf.set_font('ArialGreek', 'B', 9)
    pdf.set_text_color(0, 0, 0)
    prod_name = str(vars_df['ΠΡΟΪΟΝ'].iloc[0])
    pdf.multi_cell(block_width - 24, 3, prod_name, max_line_height=3.5)
    pdf.set_x(content_x)
    pdf.set_font('ArialGreek', '', 7)
    pdf.set_text_color(80, 80, 80)
    desc = str(vars_df['ΠΕΡΙΓΡΑΦΗ'].iloc[0])
    pdf.multi_cell(block_width - 24, 2.8, desc[:180], max_line_height=2.8)
    pdf.set_xy(content_x, pdf.get_y() + 2)
    pdf.set_fill_color(40, 40, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('ArialGreek', 'B', 6.5)
    w = [24, 18, 18, 22, 22]
    headers = ["Κωδικός", "Lt/Kg", "Συσκ.", "Τιμή Μ.", "Τιμή Κ."]
    for i, h in enumerate(headers):
        pdf.cell(w[i], 4, h, fill=True, align='C')
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)
    for idx, (_, row) in enumerate(vars_df.iterrows()):
        pdf.set_x(content_x)
        try:
            raw_m = str(row.get(col_m, 0)).replace(',', '.').strip()
            raw_k = str(row.get(col_k, 0)).replace(',', '.').strip()
            p_m = float(raw_m) * (1 - discount/100) if raw_m not in ['nan', ''] else 0
            p_k = float(raw_k) * (1 - discount/100) if raw_k not in ['nan', ''] else 0
        except:
            p_m, p_k = 0.0, 0.0
        p_m_text = f"{p_m:.2f} €" if p_m > 0 else ""
        p_k_text = f"{p_k:.2f} €" if p_k > 0 else ""
        fill = (idx % 2 == 0)
        if fill: pdf.set_fill_color(248, 248, 248)
        pdf.set_font('ArialGreek', '', 7)
        code_display = str(row.get('ΚΩΔΙΚΟΣ', '-')).replace('.0', '').strip()
        sysk_display = str(row.get('ΣΥΣΚΕΥΑΣΙΑ', '-')).replace('nan', '-')
        pdf.cell(w[0], 3.5, code_display, border='B', align='C', fill=fill)
        pdf.cell(w[1], 3.5, str(row.get('ΛΙΤΡΑ', '-')), border='B', align='C', fill=fill)
        pdf.cell(w[2], 3.5, sysk_display, border='B', align='C', fill=fill)
        pdf.set_font('ArialGreek', 'B', 7)
        pdf.cell(w[3], 3.5, p_m_text, border='B', align='C', fill=fill)
        pdf.cell(w[4], 3.5, p_k_text, border='B', align='C', fill=fill)
        pdf.ln(3.5)

def create_pdf(selected_products, df_print, terms=None, price_setup=None, global_discount=0, customer_name="", product_discounts=None):
    if product_discounts is None:
        product_discounts = {}
    pdf = ASEM_PDF(orientation='L', unit='mm', format='A4')
    base_dir = Path(__file__).parent.parent.parent
    font_path = str(base_dir / "fonts" / "arial.ttf")
    pdf.add_font('ArialGreek', '', font_path)
    pdf.add_font('ArialGreek', 'B', font_path)
    pdf.set_margins(10, 10, 10)
    pdf.add_page()

    if customer_name:
        pdf.set_font('ArialGreek', 'B', 11)
        pdf.set_text_color(0, 82, 161)
        pdf.set_xy(170, 18) 
        pdf.cell(117, 5, f"Προς: {customer_name.upper()}", align='R')
    
    df_working = df_print.copy()
    keywords_det = ['Απορρυπαντικά', 'πλυντηρίου']
    keywords_dry = ['Στεγνωτικά', 'λαμπρυντικά']
    df_working['ΥΠΟΚΑΤΗΓΟΡΙΑ'] = df_working['ΥΠΟΚΑΤΗΓΟΡΙΑ'].apply(lambda x: unify_subcategories(x, keywords_det, keywords_dry))
    COLOR_MAP = {
        "ΥΓΙΕΙΝΗ ΚΟΥΖΙΝΑΣ": (9, 93, 169), "ΟΡΟΦΟΚΟΜΙΑ": (115, 191, 68), "ΧΩΡΟΣ ΥΓΙΕΙΝΗΣ": (112, 48, 160),
        "ΦΡΟΝΤΙΔΑ ΙΜΑΤΙΣΜΟΥ": (214, 108, 108), "ECONOMY LINE": (0, 32, 96), "ΦΡΟΝΤΙΔΑ ΧΑΛΙΩΝ": (237, 125, 49),
        "ΚΑΘΑΡΙΣΜΟΣ ΜΗΧΑΝΗΣ ESPRESSO": (88, 40, 8), "ΑΠΟΛΥΜΑΝΣΗ ΧΕΡΙΩΝ & ΕΠΙΦΑΝΕΙΩΝ": (95, 3, 105),
        "ΒΙΟΜΗΧΑΝΙΑ ΤΡΟΦΙΜΩΝ & ΠΟΤΩΝ": (192, 0, 0), "ΕΠΑΓΓΕΛΜΑΤΙΚΕΣ ΣΥΣΚΕΥΕΣ & ΑΞΕΣΟΥΑΡ": (255, 192, 0), 
        "ΕΠΑΓΓΕΛΜΑΤΙΚΑ ΧΑΡΤΙΚΑ":(169, 208, 142), "ΕΠΑΓΓΕΛΜΑΤΙΚΆ ΧΑΡΤΙΚΆ": (169, 208, 142),
        "DEFAULT": (0, 82, 161)
    }
    col_m = price_setup.get('single', 'ΤΙΜΗ_Α') if price_setup else 'ΤΙΜΗ_Α'
    col_k = price_setup.get('box', 'ΤΙΜΗ_Α_ΚΙΒΩΤΙΟ') if price_setup else 'ΤΙΜΗ_Α_ΚΙΒΩΤΙΟ'
    MAX_ROWS_PER_PAGE = 4
    ROW_HEIGHT = 42
    START_Y_BASE = 28 
    LEFT_COL_X = 10
    RIGHT_COL_X = 152
    BLOCK_MAX_WIDTH = 145
    grouped = df_working[df_working['ΠΡΟΪΟΝ'].isin(selected_products)].groupby('ΠΡΟΪΟΝ', sort=False)
    current_row = 0 
    current_col = 0 
    current_cat = None
    current_subcat = None
    header_height_in_row = 0 
    for prod_name, vars_df in grouped:
        cat_raw = str(vars_df['ΚΑΤΗΓΟΡΙΑ'].iloc[0]).strip().upper()
        raw_sub = vars_df.get('ΥΠΟΚΑΤΗΓΟΡΙΑ', pd.Series([None])).iloc[0]
        subcat_raw = str(raw_sub).strip() if not (pd.isna(raw_sub) or str(raw_sub).lower() == 'nan') else ""
        is_new_cat = (cat_raw != current_cat)
        is_new_sub = (subcat_raw != current_subcat and subcat_raw != "")
        if is_new_cat or is_new_sub:
            if current_col != 0:
                current_row += 1
                current_col = 0
            if current_row >= MAX_ROWS_PER_PAGE:
                pdf.add_page()
                current_row = 0
            y_pos = START_Y_BASE + (current_row * ROW_HEIGHT)
            header_height_in_row = 0
            if is_new_cat:
                h = draw_category_header(pdf, cat_raw, COLOR_MAP.get(cat_raw, COLOR_MAP["DEFAULT"]), y_pos)
                header_height_in_row += h
                current_cat = cat_raw
                if subcat_raw:
                    h = draw_subcategory_header(pdf, subcat_raw, y_pos + header_height_in_row + 0.2)
                    header_height_in_row += h + 0.2
                    current_subcat = subcat_raw
                else:
                    current_subcat = ""
            elif is_new_sub:
                h = draw_subcategory_header(pdf, subcat_raw, y_pos + 1)
                header_height_in_row = h + 1
                current_subcat = subcat_raw
            current_col = 0
        if current_row >= MAX_ROWS_PER_PAGE:
            pdf.add_page()
            current_row = 0
            current_col = 0
            header_height_in_row = 0
        start_y = START_Y_BASE + (current_row * ROW_HEIGHT) + header_height_in_row
        start_x = LEFT_COL_X if current_col == 0 else RIGHT_COL_X
        
        spec_discount = product_discounts.get(prod_name)
        eff_discount = spec_discount if spec_discount is not None else global_discount
        
        draw_product(pdf, vars_df, start_x, start_y, BLOCK_MAX_WIDTH, col_m, col_k, eff_discount, base_dir)
        if current_col == 0:
            current_col = 1
        else:
            current_col = 0
            current_row += 1
            header_height_in_row = 0
    if terms:
        draw_terms_footer(pdf, terms, global_discount)
    return pdf.output()

def generate_final_asem_pdf(selected_products, df_print, terms=None, price_setup=None, global_discount=0, customer_name="", product_discounts=None):
    base_dir = Path(__file__).parent.parent.parent
    writer = PdfWriter()
    intro_path = base_dir / "assets" / "pdf" / "intro.pdf"
    if intro_path.exists():
        intro_reader = PdfReader(str(intro_path))
        for page in intro_reader.pages:
            writer.add_page(page)
    catalog_bytes = create_pdf(selected_products, df_print, terms, price_setup, global_discount, customer_name, product_discounts)
    catalog_reader = PdfReader(io.BytesIO(catalog_bytes))
    for page in catalog_reader.pages:
        writer.add_page(page)
    back_path = base_dir / "assets" / "pdf" / "back_cover.pdf"
    if back_path.exists():
        back_reader = PdfReader(str(back_path))
        for page in back_reader.pages:
            writer.add_page(page)
    out_buffer = io.BytesIO()
    writer.write(out_buffer)
    return out_buffer.getvalue()