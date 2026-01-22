import os
import re
import sys
import json
import argparse
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Try importing OpenAI and Google Gen AI
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import anthropic
except ImportError:
    anthropic = None

# Ensure Tesseract is in the path or configured
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def extract_text_from_file(file_path):
    """
    Extracts text from a PDF or Image file using OCR.
    """
    text = ""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.pdf':
            print(f"Processing PDF: {file_path}")
            # Convert PDF to images
            # Only process the first 3 pages to save time/resources, usually info is on page 1
            images = convert_from_path(file_path, first_page=1, last_page=3)
            for i, image in enumerate(images):
                print(f"  OCR Page {i+1}...")
                page_text = pytesseract.image_to_string(image, lang='chi_sim+eng')
                text += page_text + "\n"
        elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp']:
            print(f"Processing Image: {file_path}")
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        else:
            print(f"Unsupported file format: {file_ext}")
            return None
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None
        
    return text

def get_extraction_prompt(text):
    return f"""
    You are a professional patent analyst. Extract the following information from the provided OCR text of a Patent Certificate.
    The text may contain OCR errors, please correct them based on context.
    
    Required Fields:
    - Patent Number (专利号): Format usually starts with ZL...
    - Patent Name (专利名称): Title of the patent.
    - Patent Holder (专利权人): The owner/applicant.
    - Patent Type (专利类型): e.g., 发明, 实用新型, 外观设计.
    - Inventor (发明人): List of inventors.
    - Application Date (申请日): Format YYYY-MM-DD.

    Return ONLY a valid JSON object with these keys: "专利号", "专利名称", "专利权人", "专利类型", "发明人", "申请日".
    If a field is not found, set it to null.

    OCR Text:
    {text[:8000]} 
    """

def extract_with_gemini(text, api_key, model_name="gemini-1.5-flash"):
    print("  Invoking Gemini for extraction...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        prompt = get_extraction_prompt(text)
        
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        
        # Clean up response text if it contains markdown code blocks
        content = response.text
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        return json.loads(content)
    except Exception as e:
        print(f"  Gemini Extraction failed: {e}")
        return None

def extract_with_openai(text, client, model="gpt-3.5-turbo"):
    print("  Invoking OpenAI-compatible LLM for extraction...")
    prompt = get_extraction_prompt(text)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts JSON data from text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"  LLM Extraction failed: {e}")
        return None

def extract_with_claude(text, api_key, model="claude-3-5-sonnet-20241022"):
    print("  Invoking Claude for extraction...")
    prompt = get_extraction_prompt(text)
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system="You are a helpful assistant that extracts JSON data from text. Output ONLY valid JSON.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        
        # Simple cleanup if Claude wraps in markdown (though system prompt helps)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        print(f"  Claude Extraction failed: {e}")
        return None

def save_results_to_excel(results, output_dir=None):
    """
    Saves the list of dictionaries (results) to an Excel file.
    Automatically determines the filename based on the Patent Holder.
    """
    if not results:
        print("No information to save.")
        return

    if not output_dir:
        output_dir = os.getcwd()

    df = pd.DataFrame(results)
    cols = ['专利号', '专利名称', '专利权人', '专利类型', '发明人', '申请日', '文件路径']
    for col in cols:
        if col not in df.columns:
            df[col] = None
    df = df[cols]
    
    # Determine output filename based on one of the patent holders
    holder_name = "专利信息汇总"
    for res in results:
        name = res.get('专利权人')
        if name and isinstance(name, str) and name.strip() and name.lower() != 'none':
            # Sanitize filename
            holder_name = re.sub(r'[\\/*?:"<>|]', '', name.strip())
            break
    
    output_filename = f"{holder_name}-专利信息.xlsx"
    output_path = os.path.join(output_dir, output_filename)
    
    print(f"Saving results to {output_path}...")
    df.to_excel(output_path, index=False)
    print("Done.")
    
    try:
        if sys.platform == 'darwin':
            os.system(f'open "{output_path}"')
        elif sys.platform == 'win32':
            os.startfile(output_path)
        else:
            os.system(f'xdg-open "{output_path}"')
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Extract patent info using OCR and optional LLM.")
    parser.add_argument("path", help="Path to file or directory", nargs='?')
    parser.add_argument("--api-key", help="API Key", default=None)
    parser.add_argument("--base-url", help="Base URL (for OpenAI compatible)", default=os.environ.get("OPENAI_BASE_URL"))
    parser.add_argument("--model", help="Model name", default=None)
    parser.add_argument("--provider", help="Provider: 'gemini', 'openai', or 'regex'", default="auto")
    parser.add_argument("--action", choices=['full', 'ocr_only', 'save_excel'], default='full', help="Action mode")
    parser.add_argument("--data", help="JSON string data for save_excel action")
    parser.add_argument("--output-dir", help="Explicit output directory")
    
    args = parser.parse_args()

    # Determine Output Directory
    target_output_dir = args.output_dir
    if not target_output_dir and args.path:
        if os.path.isdir(args.path):
            target_output_dir = args.path
        else:
            target_output_dir = os.path.dirname(os.path.abspath(args.path))

    # --- Mode: Save Excel ---
    if args.action == 'save_excel':
        if not args.data:
            print("Error: --data (JSON string) is required for save_excel action.")
            sys.exit(1)
        try:
            data = json.loads(args.data)
            # Ensure it's a list
            if isinstance(data, dict):
                data = [data]
            save_results_to_excel(data, target_output_dir)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            sys.exit(1)
        return

    # For other modes, path is required
    if not args.path:
        print("Error: path argument is required.")
        sys.exit(1)

    input_path = args.path
    files_to_process = []
    
    if os.path.isfile(input_path):
        files_to_process.append(input_path)
    elif os.path.isdir(input_path):
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                    files_to_process.append(os.path.join(root, file))
    
    if not files_to_process:
        print("No valid files found.")
        sys.exit(0)

    # --- Mode: OCR Only ---
    if args.action == 'ocr_only':
        print(f"Found {len(files_to_process)} files to process.")
        for file_path in files_to_process:
            print(f"---START_OCR: {os.path.basename(file_path)}---")
            text = extract_text_from_file(file_path)
            if text:
                print(text)
            else:
                print("(OCR Failed or Empty)")
            print(f"---END_OCR---")
        return

    # --- Mode: Full (Extraction) ---
    print(f"Found {len(files_to_process)} files to process.")
    
    # ... (Provider setup remains the same)
    # Determine Provider and Key for Full Mode
    provider = args.provider
    api_key = args.api_key
    model = args.model
    
    # Auto-detection logic
    if provider == "auto":
        # Check keys in order: Gemini -> Claude -> OpenAI
        if os.environ.get("GEMINI_API_KEY"):
            provider = "gemini"
            api_key = os.environ.get("GEMINI_API_KEY")
        elif os.environ.get("ANTHROPIC_API_KEY"):
            provider = "claude"
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        elif os.environ.get("OPENAI_API_KEY"):
            provider = "openai"
            api_key = os.environ.get("OPENAI_API_KEY")
        else:
            # Default to gemini and expect a key later or error out
            provider = "gemini" 

    if provider == "gemini":
        if not api_key:
             api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            print("Error: GEMINI_API_KEY is required for Gemini extraction. Please set the environment variable or pass --api-key.")
            sys.exit(1)

        if not model:
            model = "gemini-1.5-flash"
        if not genai:
            print("Error: google-generativeai library not installed. Please install it with `pip install google-generativeai`.")
            sys.exit(1)

    if provider == "claude":
        if not api_key:
             api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY is required for Claude extraction.")
            sys.exit(1)
        if not model:
            model = "claude-3-5-sonnet-20241022"
        if not anthropic:
            print("Error: anthropic library not installed. Please install it with `pip install anthropic`.")
            sys.exit(1)
            
    if provider == "openai":
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY is required for OpenAI extraction.")
            sys.exit(1)
        if not model:
            model = "gpt-3.5-turbo"
        if not OpenAI:
            print("Error: openai library not installed.")
            sys.exit(1)

    print(f"Extraction Mode: {provider.upper()}")
    if provider != "regex":
        print(f"Model: {model}")
    
    # Define keywords for non-certificate files to skip
    skip_keywords = ['通知书', '收据', '合同', '检测报告', '受理', '清单', '说明书']
    
    results = []
    
    # Initialize Clients
    openai_client = None
    if provider == "openai":
        openai_client = OpenAI(api_key=api_key, base_url=args.base_url)

    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        
        # Check if file should be skipped
        if any(keyword in filename for keyword in skip_keywords):
            print(f"Skipping non-certificate file: {filename}")
            continue
            
        text = extract_text_from_file(file_path)
        if text:
            data = None
            if provider == "gemini":
                data = extract_with_gemini(text, api_key, model)
            elif provider == "claude":
                data = extract_with_claude(text, api_key, model)
            elif provider == "openai":
                data = extract_with_openai(text, openai_client, model)
            
            # STRICT MODE: No Regex Fallback
            if data:
                data['文件路径'] = file_path
                results.append(data)
            else:
                print(f"  Warning: LLM extraction failed for {filename}. Skipping.")
            
    save_results_to_excel(results, target_output_dir)

if __name__ == "__main__":
    main()
