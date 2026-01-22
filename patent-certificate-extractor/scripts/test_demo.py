#!/usr/bin/env python3
"""
Test script demonstrating the full workflow of patent certificate extraction
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import subprocess


def extract_text(file_path: Path, ocr_script: Path) -> str:
    """Extract OCR text from a file"""
    result = subprocess.run(
        ['python3', str(ocr_script), str(file_path)],
        capture_output=True,
        text=True
    )
    return result.stdout


def extract_with_llm(extracted_texts: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Extract structured information using LLM
    In a real implementation, this would call an LLM API
    For demonstration, we'll include sample extractions
    """
    # In production, you would:
    # 1. Call Claude or another LLM with the OCR text
    # 2. Use the prompt from references/llm_prompt.md
    # 3. Parse the JSON response
    # 4. Handle errors and missing fields

    # For this demo, return placeholder data
    results = []

    for item in extracted_texts:
        # Here you would call LLM to extract information from item['text']
        # Example:
        # response = anthropic.messages.create(
        #     model="claude-3-5-sonnet-20241022",
        #     max_tokens=1024,
        #     system="You are a specialized assistant for extracting structured information from patent certificates...",
        #     messages=[{"role": "user", "content": item['text']}]
        # )
        # extracted_data = json.loads(response.content[0].text)

        # For now, return a placeholder
        results.append({
            'filename': item['filename'],
            '专利号': '',
            '专利名称': '',
            '权利人': '',
            '专利类型': '',
            '发明人': '',
            '申请日期': '',
            'extracted_text': item['text']
        })

    return results


def main():
    """Main test function"""
    print("Patent Certificate Extractor - Test Demo")
    print("=" * 80)

    # Configuration
    test_files = [
        "/Users/licheng/Desktop/AGENT/7-公司的主要财产/7.1 知识产权-专利/AU2019325036-一种基于单域抗体的BCMA嵌合抗原受体及应用-澳大利亚发明专利证书(专利证书).pdf",
        "/Users/licheng/Desktop/AGENT/7-公司的主要财产/7.1 知识产权-专利/2019102974627-CD22单域抗体、核苷酸序列及试剂盒-中国发明专利证书(专利证书).pdf",
        "/Users/licheng/Desktop/AGENT/7-公司的主要财产/7.1 知识产权-专利/2020202177990-一种新型冠状病毒抗原检测试剂盒-实用新型专利证书(专利证书).pdf"
    ]

    script_dir = Path(__file__).parent
    ocr_script = script_dir / 'extract_ocr.py'
    excel_script = script_dir / 'generate_excel.py'

    # Step 1: Extract OCR text
    print("\n[Step 1] Extracting OCR text from patent certificates...")
    extracted_texts = []

    for file_path in test_files:
        file_path = Path(file_path)
        if file_path.exists():
            print(f"  Processing: {file_path.name}")
            text = extract_text(file_path, ocr_script)

            if text:
                extracted_texts.append({
                    'filename': file_path.name,
                    'text': text
                })
                print(f"  ✓ Extracted {len(text)} characters")
            else:
                print(f"  ✗ Failed to extract text")
        else:
            print(f"  ✗ File not found: {file_path.name}")

    print(f"\n  Successfully extracted text from {len(extracted_texts)} files")

    # Step 2: Extract structured information using LLM
    print("\n[Step 2] Extracting structured information using LLM...")
    print("  Note: In production, this would call an LLM API")
    print("  See references/llm_prompt.md for the prompt template")
    print("  For this demo, we'll save the OCR text for manual review")

    # Save extracted texts for review
    output_dir = Path('/tmp/patent_extraction_demo')
    output_dir.mkdir(exist_ok=True)

    for idx, item in enumerate(extracted_texts, 1):
        output_file = output_dir / f"{item['filename']}_extracted.txt"
        output_file.write_text(item['text'], encoding='utf-8')
        print(f"  Saved: {output_file.name}")

    # Step 3: Example of how to use LLM (commented out)
    print("\n[Step 3] Example LLM extraction process:")
    print("""
    To extract structured information using Claude:

    1. Load the prompt template from references/llm_prompt.md
    2. Pass the OCR text to Claude with the system prompt
    3. Request JSON output with these fields:
       - 专利号 (Patent Number)
       - 专利名称 (Patent Title)
       - 权利人 (Patent Holder)
       - 专利类型 (Patent Type)
       - 发明人 (Inventor)
       - 申请日期 (Application Date)
    4. Parse the JSON response

    Example request to Claude:
    "Extract patent information from this text and return as JSON:
     [PASTE OCR TEXT HERE]"
    """)

    # Step 4: Generate Excel (with sample data)
    print("\n[Step 4] Generating Excel file...")

    # For demonstration, create sample data based on what we saw in the OCR text
    sample_data = [
        {
            '专利号': 'AU2019325036',
            '专利名称': 'BCMA chimeric antigen receptor based on single domain antibody and use thereof',
            '权利人': 'Shenzhen Pregene Biopharma Co. Ltd.',
            '专利类型': 'Standard Patent (Invention)',
            '发明人': 'ZHANG, Jishuai; LI, Hongjian; SU, Hongchang; BAO, Chaolemeng; SONG, Zongpei; CAI, Qinghua; DING, Yijin and CAI, Zhibo',
            '申请日期': '2019-07-10'
        },
        {
            '专利号': 'ZL201910297462.7',
            '专利名称': 'CD22单域抗体、核苷酸序列及试剂盒',
            '权利人': '深圳普瑞金生物药业股份有限公司',
            '专利类型': '发明专利',
            '发明人': '李胜华;包朝乐戎;李莹莹;许沙沙;余祥',
            '申请日期': '2019-04-12'
        },
        {
            '专利号': 'ZL202020217799.0',
            '专利名称': '一种新型冠状病毒抗原检测试剂盒',
            '权利人': '深圳普瑞金生物药业有限公司',
            '专利类型': '实用新型专利',
            '发明人': '包朝乐萌;吴显辉;贾向娇;栗红建;袭志波;张继帅;宋宗培',
            '申请日期': '2020-02-26'
        }
    ]

    excel_output = output_dir / '专利清单.xlsx'

    # Convert sample_data to JSON string for the script
    json_data = json.dumps(sample_data, ensure_ascii=False)

    result = subprocess.run(
        ['python3', str(excel_script), str(excel_output), json_data],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"  ✓ Excel file created: {excel_output}")
        print(f"    {result.stdout}")
    else:
        print(f"  ✗ Failed to create Excel file")
        print(f"    Error: {result.stderr}")

    # Summary
    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("\nResults saved to: /tmp/patent_extraction_demo/")
    print(f"  - OCR text files: {len(extracted_texts)} files")
    print(f"  - Excel file: {excel_output.name}")
    print("\nNext steps for production use:")
    print("  1. Install required dependencies: pip install openpyxl pdf2image Pillow anthropic")
    print("  2. Set up LLM API credentials (e.g., Claude API key)")
    print("  3. Modify the extract_with_llm function to call the LLM API")
    print("  4. Process all files in the patent folder using batch_extract.py")
    print("  5. Review and verify the extracted data in the Excel file")


if __name__ == "__main__":
    main()
