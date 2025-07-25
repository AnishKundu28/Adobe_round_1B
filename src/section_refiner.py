# src/section_refiner.py
import fitz

def extract_section_text(pdf_path, page_num, heading_text):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return ""

    if page_num < 1 or page_num > doc.page_count:
        print("Page number out of range.")
        return ""

    page = doc.load_page(page_num - 1)
    text_blocks = page.get_text("blocks")

    section_content = []
    target_found = False

    for block in text_blocks:
        # Ensure block has enough elements
        if len(block) < 5:
            continue
        block_text = block[4].strip()

        if heading_text.lower() in block_text.lower():
            target_found = True
            continue

        if target_found and block_text and not block_text.isspace():
            section_content.append(block_text)

        # Heuristic: stop after 3–4 non-empty blocks
        if target_found and len(section_content) > 3:
            break

    return " ".join(section_content)