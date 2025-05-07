"""  
Splits one or more PDF files into per-page PNG images.  
"""  
import os
import fitz  # PyMuPDF  
from pathlib import Path  
import logging  
  
def pdf_to_images(pdf_path: Path, output_dir: Path) -> list:  
    """  
    Splits all pages of the PDF at pdf_path into PNG images in output_dir.  
    Returns a list of image file paths.  
    """  
    os.makedirs(output_dir, exist_ok=True) 
    doc = fitz.open(pdf_path)  
    exported_images = []  
    for page_num in range(doc.page_count):  
        page = doc.load_page(page_num)  
        pix = page.get_pixmap()  
        img_path = output_dir / f"page_{page_num + 1}.png"  
        pix.save(img_path)  
        exported_images.append(img_path)  
        logging.debug(f"Exported page {page_num+1} to {img_path}")  
    doc.close()  
    return exported_images  
  
def batch_pdf_to_images(pdf_paths, global_output_dir):  
    """  
    Process multiple PDFs, placing images in folders named after each PDF.  
    Returns a dict: {pdf_stem: [list of images]}  
    """  
    pdf_output = {}  
    for pdf in pdf_paths:  
        pdf = Path(pdf)  
        pdf_name = pdf.stem  
        dest_dir = Path(global_output_dir) / pdf_name  
        pdf_output[pdf_name] = pdf_to_images(pdf, dest_dir)  
    return pdf_output  