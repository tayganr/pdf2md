"""  
Concatenates per-page markdown files of each document into a single markdown file.  
"""  
  
import re  
from pathlib import Path  
import logging  
  
def natural_sort_key(s):  
    # E.g., page_12.md -> ['page_', 12, '.md']  
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]  
  
def concat_markdown(doc_md_dir: Path, output_filename="full_document.md"):  
    """  
    Concatenate all page_X.md in doc_md_dir into one file, with start/end comments.  
    """  
    md_files = [f for f in doc_md_dir.glob("page_*.md")]  
    if not md_files:  
        logging.warning(f"No page markdown files found in {doc_md_dir}.")  
        return  
    md_files.sort(key=lambda f: natural_sort_key(f.name))  
  
    out_path = doc_md_dir / output_filename  
    with open(out_path, "w", encoding="utf-8") as outf:  
        for mdfile in md_files:  
            page_num = re.search(r'page_(\d+)\.md', mdfile.name).group(1)  
            outf.write(f"<!-- START PAGE {page_num} ({mdfile.name}) -->\n")  
            with open(mdfile, "r", encoding="utf-8") as inf:  
                outf.write(inf.read().rstrip('\n'))  
            outf.write(f"\n<!-- END PAGE {page_num} ({mdfile.name}) -->\n\n")  
    logging.info(f"Concatenated markdown saved to {out_path}")  
  
def batch_concat_markdown(markdown_root: Path):  
    """  
    For every subfolder (document) in markdown_root, call concat_markdown.  
    """  
    for doc_dir in markdown_root.iterdir():  
        if doc_dir.is_dir():  
            logging.info(f"Concatenating markdown for {doc_dir.name}")  
            concat_markdown(doc_dir)  