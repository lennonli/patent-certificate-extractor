# Patent Certificate Extractor

A Claude skill for extracting structured information from scanned patent certificates (PDF/image formats) using OCR and LLM-based information extraction.

## Features

- 📄 **Multi-format Support**: Handles PDF, PNG, JPG, JPEG, BMP, TIFF files
- 🌐 **Bilingual OCR**: Tesseract-based text extraction for Chinese and English
- 🤖 **LLM Extraction**: Intelligent information extraction using Claude
- 📊 **Smart Excel Output**: Automatically sorted and grouped by:
  - 权利人 (Patent Holder) - alphabetical order
  - 专利类型 (Patent Type) - priority: 发明专利 > 实用新型专利 > 外观设计专利
  - 申请日期 (Application Date) - descending (most recent first)
- 📦 **Batch Processing**: Process multiple patent certificates at once
- 🎨 **Visual Grouping**: Thick border lines separate different patent holder groups

## Extracted Information

- 专利号 (Patent Number)
- 专利名称 (Patent Title)
- 权利人 (Patent Holder/Assignee)
- 专利类型 (Patent Type)
- 发明人 (Inventor)
- 申请日期 (Application Date)

## Requirements

### System Dependencies

```bash
# macOS
brew install tesseract
brew install tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim
```

### Python Dependencies

```bash
pip install openpyxl pdf2image Pillow
```

## Usage

### Quick Start

1. **Extract OCR Text**

```bash
python scripts/extract_ocr.py certificate.pdf > extracted_text.txt
```

2. **Extract Information with LLM**

Use the prompt template from `references/llm_prompt.md` with Claude or another LLM to extract structured data.

3. **Generate Excel File**

```bash
python scripts/generate_excel.py patent_list.json
```

### Batch Processing

```bash
# Extract OCR text from all PDFs in a folder
python scripts/batch_extract.py /path/to/patents

# This will create:
# - *_extracted.txt files for each certificate
# - batch_extraction_results.json with metadata
```

### Testing

```bash
# Test sorting and grouping logic
python scripts/test_sorting.py

# Run complete demo with sample data
python scripts/test_demo.py
```

## File Structure

```
patent-certificate-extractor/
├── SKILL.md                           # Skill documentation
├── scripts/
│   ├── extract_ocr.py                 # OCR text extraction
│   ├── generate_excel.py              # Excel generation with sorting
│   ├── batch_extract.py              # Batch processing
│   ├── test_sorting.py              # Sorting logic tests
│   └── test_demo.py                # Complete workflow demo
└── references/
    └── llm_prompt.md               # LLM prompt template
```

## Sorting Rules

The Excel output is automatically sorted and grouped:

1. **Primary Sort**: 权利人 (Patent Holder) - alphabetically
2. **Secondary Sort**: 专利类型 (Patent Type) - priority order:
   - 发明专利 (Invention) - Priority 1
   - 实用新型专利 (Utility Model) - Priority 2
   - 外观设计专利 (Design) - Priority 3
3. **Tertiary Sort**: 申请日期 (Application Date) - descending

## Example Output

```
Shenzhen Pregene Biopharma Co. Ltd. | 发明专利 | 2020-06-01
Shenzhen Pregene Biopharma Co. Ltd. | 发明专利 | 2019-07-10
──────────────────────────────────────────────────────────
深圳普瑞金生物药业有限公司            | 发明专利 | 2019-04-12
深圳普瑞金生物药业有限公司            | 发明专利 | 2019-04-10
深圳普瑞金生物药业有限公司            | 实用新型专利 | 2020-02-27
深圳普瑞金生物药业有限公司            | 实用新型专利 | 2020-02-26
```

## Installation

1. Download the `.skill` file
2. Add it to your Claude skills directory
3. The skill will be automatically available when you need to process patent certificates

## Troubleshooting

### Tesseract Not Found
```
Error: Tesseract OCR is not installed or not in PATH
```
**Solution**: Install Tesseract OCR and ensure it's in your PATH

### Poor OCR Quality
**Solution**:
- Ensure scans are at 300 DPI or higher
- Try pre-processing images (contrast adjustment, noise reduction)
- Use Tesseract's advanced configuration options

### PDF Processing Fails
**Solution**:
- Install pdf2image: `pip install pdf2image`
- Install Poppler (required by pdf2image)
- macOS: `brew install poppler`
- Ubuntu: `sudo apt-get install poppler-utils`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

Created with ❤️ for Claude Skills
