from dotenv import load_dotenv  
import os  
import argparse  
from pathlib import Path  
import logging  
import pdf2images  
import img2markdown  
import concat_markdown  
  
def main():  
    # Set up logging  
    logging.basicConfig(  
        format='[%(asctime)s | %(levelname)s]: %(message)s', level=logging.INFO  
    )  
  
    # Load environment variables from .env  
    load_dotenv(override=True)  
  
    # Parse CLI arguments  
    parser = argparse.ArgumentParser(description="Extract detailed markdown (with non-text descriptions) from PDF(s) using GenAI.")  
    parser.add_argument("--split", action="store_true", help="Only split PDF(s) to images")  
    parser.add_argument("--genai", action="store_true", help="Only convert images to markdown using GenAI")  
    parser.add_argument("--concat", action="store_true", help="Only concatenate markdown per document")  
    args = parser.parse_args()  
  
    # Read config from environment variables  
    input_pdf_dir = Path(os.environ["INPUT_PDF_DIR"])  
    output_image_dir = os.environ["OUTPUT_IMAGE_DIR"]  
    output_markdown_dir = os.environ["OUTPUT_MARKDOWN_DIR"]  
    openai_conf = {  
        "deployment": os.environ["OPENAI_DEPLOYMENT"],  
        "api_version": os.environ["OPENAI_API_VERSION"],  
        "endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],  
        "api_key": os.environ["AZURE_OPENAI_API_KEY"]  
    }  
  
    pdf_paths = sorted(str(p) for p in input_pdf_dir.glob("*.pdf"))  
  
    # Stage 1: PDF → Images  
    if not (args.genai or args.concat):  
        logging.info("=== Stage 1: Splitting PDFs to images")  
        images_by_doc = pdf2images.batch_pdf_to_images(pdf_paths, output_image_dir)  
    else:  
        images_by_doc = {}  
        image_root = Path(output_image_dir)  
        for doc_dir in image_root.iterdir():  
            if doc_dir.is_dir():  
                images = sorted(doc_dir.glob("*.png"))  
                if images:  
                    images_by_doc[doc_dir.name] = images  
  
    # Stage 2: Images → Markdown  
    if not (args.split or args.concat):  
        logging.info("=== Stage 2: Generating markdown from images via GenAI")  
        img2markdown.batch_images_to_markdown(  
            images_by_doc,  
            Path(output_markdown_dir),  
            openai_conf,  
        )  
  
    # Stage 3: Concatenate  
    if not (args.split or args.genai):  
        logging.info("=== Stage 3: Concatenating markdown per document")  
        concat_markdown.batch_concat_markdown(Path(output_markdown_dir))  
  
    logging.info("Pipeline complete.")  
  
if __name__ == "__main__":  
    main()  