# PDF-to-Markdown with GenAI  
   
Extract faithful, detailed markdown—including layout, formatting, and inline descriptions of non-text elements—from PDF files using Azure OpenAI’s GPT models. This pipeline splits PDFs into images, generates structured markdown for each page with generative AI, and combines the results into a single markdown file per document.  
   
---  
   
## Features  
   
- Converts multipage PDFs to per-page PNG images  
- Uses Azure OpenAI to extract detailed markdown from page images  
- Produces accurate, non-summarized markdown (structure, layout, lists, tables, etc.)  
- Describes images/diagrams/figures in context within markdown output  
- Each stage (split, conversion, concat) is independently runnable via CLI flags  
- All configuration via `.env`
   
---  
   
## Quickstart  
   
### 1. Clone the Repository  
   
```sh  
git clone https://github.com/tayganr/pdf2md.git  
cd pdf2md
```  
   
### 2. Install Requirements  
   
```sh  
pip install -r requirements.txt  
```  
   
### 3. Set Up Your Environment  
   
Copy `.env.example` to `.env` and fill in all values:  
```sh  
cp .env.example .env  
```  
Edit `.env` to specify input/output folders and your Azure OpenAI credentials/deployment.  
   
Example:  
```ini  
# Input / Output paths  
INPUT_PDF_DIR=example_docs  
OUTPUT_IMAGE_DIR=output/images  
OUTPUT_MARKDOWN_DIR=output/markdown  
   
# OpenAI API settings  
OPENAI_DEPLOYMENT=gpt-4.1  
OPENAI_API_VERSION=2025-01-01-preview  
AZURE_OPENAI_ENDPOINT=https://your-azure-endpoint.openai.azure.com/  
AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here  
```  
   
---  
   
## Usage  
   
The pipeline has three stages. Each can be run separately or the full pipeline can be run with no extra arguments.  
   
**Full pipeline (split → markdown → concat):**  
```sh  
python main.py  
```  
   
**Split PDFs to per-page images only:**  
```sh  
python main.py --split  
```  
   
**Convert images to markdown only (using existing images):**  
```sh  
python main.py --genai  
```  
   
**Concatenate per-page markdown files to a full-document markdown file:**  
```sh  
python main.py --concat  
```  
   
_Output for each PDF will be saved under `OUTPUT_IMAGE_DIR` and `OUTPUT_MARKDOWN_DIR`._  
   
---  
   
## How It Works  
   
1. **Splitting PDFs:**    
   PDFs are split into per-page PNG images, named and organized by document.  
   
2. **Generative AI Markdown Extraction:**    
   Each image is sent to your Azure OpenAI deployment, with a system prompt instructing it to output **only raw markdown** (no code fences), structured faithfully, and with descriptive captions for non-text elements.  
   
3. **Concatenation:**    
   All per-page markdown files are concatenated into a final `full_document.md` for each original PDF.  

---  
   
## Dependencies  
   
- Python 3.8+  
- [PyMuPDF](https://pymupdf.readthedocs.io/) (`fitz`)  
- [python-dotenv](https://pypi.org/project/python-dotenv/)  
- [openai](https://pypi.org/project/openai/) (Azure mode)  
- [tqdm](https://pypi.org/project/tqdm/) (for progress bars)  
