# src/pdf_parser.py

import fitz  # PyMuPDF
from pathlib import Path

class PDFParser:
    def extract_sections(self, file_path: str) -> list:
        """
        Extracts structured sections (title, content, page) from a PDF.
        A section is defined by a heading and the text that follows it.
        """
        doc = fitz.open(file_path)
        sections = []
        current_section = None
        
        # Heuristic: Find the most common font sizes to identify body text vs headings
        font_sizes = {}
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = round(span["size"])
                            font_sizes[size] = font_sizes.get(size, 0) + 1
        
        if not font_sizes:
            return [] # Empty document

        sorted_sizes = sorted(font_sizes.items(), key=lambda x: x[1], reverse=True)
        body_font_size = sorted_sizes[0][0]
        
        # A heading is larger than the most common font size and likely bold
        heading_threshold = body_font_size + 1

        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    text_content = ""
                    is_heading = False
                    first_span = block["lines"][0]["spans"][0]
                    font_size = round(first_span["size"])
                    is_bold = "bold" in first_span["font"].lower()

                    # Check if the block is a heading
                    if font_size >= heading_threshold and is_bold:
                        is_heading = True
                        heading_text = " ".join([line["spans"][0]["text"] for line in block["lines"]]).strip()
                    else:
                        text_content = " ".join([line["spans"][0]["text"] for line in block["lines"]]).strip()

                    if is_heading:
                        if current_section:
                            sections.append(current_section)
                        current_section = {
                            "title": heading_text,
                            "content": "",
                            "page": page_num + 1,
                            "source_doc": Path(file_path).name,
                        }
                    elif current_section:
                        current_section["content"] += f" {text_content}"
        
        if current_section:
            sections.append(current_section)
            
        return [s for s in sections if len(s['content'].split()) > 20] # Filter out very short sections