"""  
Uses a generative AI model to extract detailed, structured markdown from page images.  
"""  
  
import os  
import base64  
from pathlib import Path  
from openai import AzureOpenAI  
import logging  
from dotenv import load_dotenv 
from tqdm import tqdm   
  
SYSTEM_PROMPT = (  
    "You will be provided with images of a PDF document. "  
    "Your task is to extract and present the content in as much detail as possible, "  
    "conveying the information faithfully and reproducing the structure, layout, and any relevant formatting in markdown. "  
    "Do not summarize—preserve as much of the original detail as possible, including headings, tables, lists, text, and layout. "  
    "For any non-text content (such as images, diagrams, charts, or illustrations), describe them accurately and include the description at the appropriate place within the markdown. "  
    "IMPORTANT: Output only the markdown content as plain text. "  
    "Do NOT wrap your response in any code blocks or triple backticks (such as ``` or ```markdown). "  
    "Do NOT prepend or append any extra formatting, comments, or explanation. "  
    "Your response should be the raw, unadorned markdown only."  
)  
  
def base64_image(img_path: Path) -> str:  
    with open(img_path, "rb") as f:  
        return base64.b64encode(f.read()).decode("ascii")  
  
def image_to_markdown(  
    image_path: Path,  
    client: AzureOpenAI,  
    deployment: str,  
    system_prompt=SYSTEM_PROMPT,  
) -> str:  
    # Compose prompt  
    user_content = [{  
        "type": "image_url",  
        "image_url": {"url": f"data:image/png;base64,{base64_image(image_path)}"}  
    }]  
    system_content = {  
        "role": "system",  
        "content": [{"type": "text", "text": system_prompt}]  
    }  
    messages = [system_content, {"role": "user", "content": user_content}]  
  
    response = client.chat.completions.create(  
        model=deployment,  
        messages=messages,  
        max_tokens=32000,  
        temperature=1,  
        top_p=1,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stream=False  
    )  
    # Collect combined output from all choices (usually 1)  
    md_output = ''  
    for choice in response.choices:  
        md_output += choice.message.content  
    return md_output  
  
def batch_images_to_markdown(images_by_doc: dict, output_root: Path, openai_config: dict):  
    """  
    For each document (keyed by name), for each image, run the model and save the markdown outputs.  
    images_by_doc: dict of {doc_name: [img_paths]}  
    """  
    os.makedirs(output_root, exist_ok=True) 
    load_dotenv(override=True) # Make sure env is available for openai client  
  
    client = AzureOpenAI(  
        azure_endpoint=openai_config["endpoint"],  
        api_key=openai_config["api_key"],  
        api_version=openai_config["api_version"]  
    )  
    deployment = openai_config["deployment"]  
  
    for doc_name, image_paths in images_by_doc.items():  
        doc_md_dir = output_root / doc_name  
        os.makedirs(doc_md_dir, exist_ok=True)
        logging.info(f'Processing {len(image_paths)} pages from document "{doc_name}"...')  
        for img_path in tqdm(sorted(image_paths, key=lambda p: int(p.stem.split('_')[-1])), desc=f"{doc_name} pages"):  
            md = image_to_markdown(img_path, client, deployment)  
            md_filename = doc_md_dir / f"{img_path.stem}.md"  
            with open(md_filename, "w", encoding="utf-8") as f:  
                f.write(md)  
            logging.debug(f"Saved markdown {md_filename}")  
        logging.info(f"Completed markdown generation for {doc_name}")  