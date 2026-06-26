"""
generate_pdf.py — Converts PROJECT_OVERVIEW.md to a nicely formatted PDF
Run: venv\Scripts\python.exe generate_pdf.py
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import re


def clean(text: str) -> str:
    """Replace non-latin-1 characters with safe ASCII equivalents."""
    replacements = {
        "\u2014": "-",   # em dash
        "\u2013": "-",   # en dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2022": "*",   # bullet
        "\u2026": "...", # ellipsis
        "\u2192": "->",  # right arrow
        "\u2190": "<-",  # left arrow
        "\u2194": "<->", # left-right arrow
        "\u25ba": ">",   # play button
        "\u2588": "#",   # full block
        "\u2550": "=",   # double horizontal
        "\u2502": "|",   # box drawing vertical
        "\u251c": "|",   # box drawing tee
        "\u2500": "-",   # box drawing horizontal
        "\u2514": "+",   # box drawing corner
        "\u2510": "+",   # box drawing top-right corner
        "\u2518": "+",   # box drawing bottom-right
        "\u250c": "+",   # box drawing top-left
        "\u2588": "#",
        "\u2593": "#",
        "\u2592": "#",
        "\u2591": " ",
        "\u00ae": "(R)",
        "\u00a9": "(C)",
        "\u00b7": "*",
        "\u2605": "*",   # star
        "\u2764": "<3",  # heart
        "\u2713": "OK",  # checkmark
        "\u2714": "OK",
        "\u2717": "X",
        "\u2718": "X",
        "\u00e9": "e",
        "\u00e8": "e",
        "\u00ea": "e",
        "\u00e0": "a",
        "\u00e2": "a",
        "\u00f4": "o",
    }
    for ch, rep in replacements.items():
        text = text.replace(ch, rep)
    # Strip anything else outside latin-1
    return text.encode("latin-1", errors="ignore").decode("latin-1")

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BG      = (15,  23,  42)   # slate-900  (header bg)
ACCENT       = (99, 102, 241)   # indigo-500 (section rules)
TEXT_MAIN    = (30,  41,  59)   # slate-800
TEXT_MUTED   = (100, 116, 139)  # slate-500
CODE_BG      = (241, 245, 249)  # slate-100
CODE_TEXT    = (51,  65,  85)   # slate-700
TABLE_HEAD   = (99, 102, 241)   # indigo-500
TABLE_ROW_A  = (248, 250, 252)  # slate-50
TABLE_ROW_B  = (255, 255, 255)  # white
WHITE        = (255, 255, 255)

# ── Read source markdown ─────────────────────────────────────────────────────
with open("PROJECT_OVERVIEW.md", "r", encoding="utf-8") as f:
    lines = f.readlines()


# ── PDF class ────────────────────────────────────────────────────────────────
class OverviewPDF(FPDF):

    def header(self):
        # Only on the first page
        if self.page_no() == 1:
            return
        # Slim top-bar on subsequent pages
        self.set_fill_color(*DARK_BG)
        self.rect(0, 0, 210, 10, "F")
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*WHITE)
        self.set_xy(10, 2)
        self.cell(0, 6, "Pizza Restaurant AI Agent - Full Project Overview", align="L")
        self.set_xy(0, 2)
        self.cell(200, 6, f"Page {self.page_no()}", align="R")
        self.ln(8)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*TEXT_MUTED)
        self.cell(0, 6, "Research Project | RL-Based Stateful Fuzzing Framework for LLM Agent Workflows", align="C")

    # ── Cover / hero block ───────────────────────────────────────────────────
    def cover_block(self, title: str, subtitle: str, meta: str):
        self.set_fill_color(*DARK_BG)
        self.rect(0, 0, 210, 58, "F")

        # Emoji icon area
        self.set_font("Helvetica", "B", 36)
        self.set_text_color(*WHITE)
        self.set_xy(0, 8)
        self.cell(210, 14, clean("Pizza Restaurant AI Agent"), align="C")

        self.set_font("Helvetica", "", 13)
        self.set_text_color(199, 210, 254)   # indigo-200
        self.set_xy(0, 25)
        self.cell(210, 8, clean(subtitle), align="C")

        self.set_font("Helvetica", "I", 9)
        self.set_text_color(148, 163, 184)   # slate-400
        self.set_xy(0, 36)
        self.cell(210, 6, clean(meta), align="C")

        # Accent rule below hero
        self.set_fill_color(*ACCENT)
        self.rect(0, 55, 210, 2, "F")
        self.ln(62)

    # ── Section heading ──────────────────────────────────────────────────────
    def section_h1(self, text: str):
        self.ln(4)
        self.set_fill_color(*ACCENT)
        self.rect(10, self.get_y(), 3, 8, "F")
        self.set_xy(15, self.get_y())
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*DARK_BG)
        self.cell(0, 8, clean(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # Thin underline
        y = self.get_y()
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.4)
        self.line(10, y, 200, y)
        self.ln(3)

    def section_h2(self, text: str):
        self.ln(3)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*ACCENT)
        self.cell(0, 7, clean(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def section_h3(self, text: str):
        self.ln(2)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*TEXT_MAIN)
        self.cell(0, 6, clean(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ── Normal paragraph ─────────────────────────────────────────────────────
    def para(self, text: str):
        # strip bold/italic markers for plain PDF rendering
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"\*(.+?)\*",   r"\1", text)
        text = re.sub(r"`(.+?)`",     r"\1", text)
        text = clean(text)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*TEXT_MAIN)
        self.set_x(10)
        self.multi_cell(190, 5.5, text.strip())
        self.ln(1)

    # ── Bullet ───────────────────────────────────────────────────────────────
    def bullet(self, text: str, indent: int = 0):
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"`(.+?)`", r"\1", text)
        text = clean(text)
        x = 13 + indent * 5
        self.set_x(x)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*ACCENT)
        self.cell(4, 5, ">")             # bullet
        self.set_text_color(*TEXT_MAIN)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(190 - (x - 10), 5, text.strip())

    # ── Code block ───────────────────────────────────────────────────────────
    def code_block(self, lines_list: list[str]):
        content = clean("\n".join(lines_list))
        self.set_fill_color(*CODE_BG)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.3)
        # Measure height
        self.set_font("Courier", "", 7.5)
        nb_lines = len(lines_list)
        block_h = nb_lines * 4 + 6
        # Draw box
        y0 = self.get_y()
        if y0 + block_h > 275:
            self.add_page()
            y0 = self.get_y()
        self.set_xy(10, y0)
        self.rect(10, y0, 190, block_h, "FD")
        self.set_xy(13, y0 + 3)
        self.set_text_color(*CODE_TEXT)
        self.multi_cell(184, 4, content)
        self.ln(3)

    # ── Table ────────────────────────────────────────────────────────────────
    def draw_table(self, rows: list[list[str]]):
        if not rows:
            return
        col_n = len(rows[0])
        col_w = 188 / col_n
        row_h = 6

        for ri, row in enumerate(rows):
            if ri == 0:                    # header row
                self.set_fill_color(*TABLE_HEAD)
                self.set_text_color(*WHITE)
                self.set_font("Helvetica", "B", 8)
            else:
                fill = TABLE_ROW_A if ri % 2 == 1 else TABLE_ROW_B
                self.set_fill_color(*fill)
                self.set_text_color(*TEXT_MAIN)
                self.set_font("Helvetica", "", 8)

            self.set_x(10)
            for ci, cell in enumerate(row):
                cell = re.sub(r"\*\*(.+?)\*\*", r"\1", cell)
                cell = re.sub(r"`(.+?)`", r"\1", cell)
                cell = clean(cell)
                self.cell(col_w, row_h, cell.strip(), border=1, fill=True)
            self.ln(row_h)
        self.ln(2)

    # ── Horizontal rule ──────────────────────────────────────────────────────
    def hr(self):
        self.ln(2)
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)


# ── Parse & render ───────────────────────────────────────────────────────────
pdf = OverviewPDF(orientation="P", unit="mm", format="A4")
pdf.set_margins(10, 14, 10)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Cover block
pdf.cover_block(
    title    = "🍕 Pizza Restaurant AI Agent",
    subtitle = "Multi-Step Stateful RAG Agent — Full Project Overview",
    meta     = "Research Project | RL-Based Stateful Fuzzing Framework for LLM Agent Workflows"
)

# ── State machine for parsing ────────────────────────────────────────────────
in_code   = False
code_buf  = []
in_table  = False
table_buf = []

i = 0
while i < len(lines):
    raw  = lines[i].rstrip("\n")
    line = raw.strip()

    # ── Code fence ──────────────────────────────────────────────────────────
    if line.startswith("```"):
        if not in_code:
            in_code  = True
            code_buf = []
        else:
            in_code = False
            pdf.code_block(code_buf)
        i += 1
        continue

    if in_code:
        code_buf.append(raw)
        i += 1
        continue

    # ── Markdown table ───────────────────────────────────────────────────────
    if line.startswith("|"):
        if not in_table:
            in_table  = True
            table_buf = []
        cells = [c.strip() for c in line.strip("|").split("|")]
        # skip separator rows like |---|---|
        if not all(re.match(r"^[-: ]+$", c) for c in cells):
            table_buf.append(cells)
        i += 1
        continue
    else:
        if in_table:
            in_table = False
            pdf.draw_table(table_buf)
            table_buf = []

    # ── Headings ─────────────────────────────────────────────────────────────
    if line.startswith("#### "):
        pdf.section_h3(line[5:])
    elif line.startswith("### "):
        pdf.section_h3(line[4:])
    elif line.startswith("## "):
        pdf.section_h2(line[3:])
    elif line.startswith("# "):
        pdf.section_h1(line[2:])

    # ── Horizontal rule ──────────────────────────────────────────────────────
    elif line == "---":
        pdf.hr()

    # ── Bullets ──────────────────────────────────────────────────────────────
    elif re.match(r"^[\-\*] ", line):
        pdf.bullet(line[2:], indent=0)
    elif re.match(r"^ {2,4}[\-\*] ", line):
        pdf.bullet(line.lstrip()[2:], indent=1)

    # ── Numbered list ────────────────────────────────────────────────────────
    elif re.match(r"^\d+\. ", line):
        pdf.bullet(re.sub(r"^\d+\. ", "", line), indent=0)

    # ── Blank line ───────────────────────────────────────────────────────────
    elif line == "":
        pdf.ln(2)

    # ── Normal paragraph ─────────────────────────────────────────────────────
    else:
        pdf.para(line)

    i += 1

# Flush any trailing table
if in_table and table_buf:
    pdf.draw_table(table_buf)

# ── Save ─────────────────────────────────────────────────────────────────────
output_path = "PROJECT_OVERVIEW.pdf"
pdf.output(output_path)
print(f"✅ PDF saved to: {output_path}")
