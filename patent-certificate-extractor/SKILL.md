# Patent Certificate Extractor

## Description
Automatically extract structured information from patent certificate images using OCR technology and generate formatted Excel reports. Processes single or multiple certificates in batch with optional high-performance concurrent processing. Extracts patent numbers, dates, inventor information, and other key data.

## When to Use This Skill
Use this skill when the user wants to:
- Extract information from patent certificate images (专利证书图片信息提取)
- Process multiple patent certificates in batch (批量处理专利证书)
- Generate Excel reports from patent data (生成专利数据报表)
- Convert patent certificate images to structured data (证书图片转结构化数据)
- Organize and validate patent information (整理和验证专利信息)
- High-performance processing of large batches (大批量高性能处理)

Trigger keywords: "extract patent", "patent certificate", "专利证书", "提取专利信息", "批量处理证书", "并发处理"

## Prerequisites and Environment Setup

Before running this skill, Claude should verify:

1. **Tesseract OCR Installation**
   - Check if Tesseract OCR is installed: `tesseract --version`
   - Must support Chinese and English: `chi_sim` and `eng` language packs
   - If not installed, guide user to: https://github.com/tesseract-ocr/tesseract
   - macOS: `brew install tesseract tesseract-lang`
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim`

2. **Python Dependencies**
   - Python 3.10 or higher
   - Required packages: `pdf2image`, `openpyxl`, `Pillow`
   - Check if dependencies are installed, if not, run: `pip install pdf2image openpyxl Pillow`

3. **Project Structure**
   - Verify all core scripts exist (extract_ocr.py, batch_extract.py, generate_excel.py)
   - Check for input/output directories
   - Verify test data files if running validation

**Important Note**: This skill uses **Tesseract OCR** (open-source, local, free), NOT Google Cloud Vision API. No API keys or cloud credentials required!

## Workflow

When this skill is invoked, Claude should follow these steps:

### Step 1: Initial Assessment
- Ask user about their task:
  - Single certificate or batch processing?
  - How many certificates need to be processed? (determines concurrent vs sequential)
  - Where are the certificate images located?
  - What output format do they prefer (Excel, JSON, or both)?
  - Any specific data fields they need extracted?

### Step 2: Environment Verification
```bash
# Check Tesseract OCR installation
tesseract --version

# Verify Python version
python3 --version

# Check if required packages are installed
python3 -c "import pdf2image; import openpyxl; from PIL import Image; print('Dependencies OK')"
```

### Step 3: Process Certificates

**For Single Certificate:**
```bash
# Run OCR extraction
python3 extract_ocr.py /path/to/certificate.pdf
```

**For Small Batch Processing (< 20 files):**
```bash
# Sequential processing (simple, reliable)
python3 batch_extract.py /path/to/certificates/
```

**For Large Batch Processing (20+ files) - Recommended:**
```bash
# Concurrent processing with auto-detected CPU cores
python3 batch_extract.py /path/to/certificates/ --concurrent

# Concurrent processing with specified workers (recommended: 2-8)
python3 batch_extract.py /path/to/certificates/ --concurrent --workers=4

# With custom output file
python3 batch_extract.py /path/to/certificates/ results.json --concurrent --workers=4
```

### Step 4: Generate Excel Report
```bash
# Convert JSON data to Excel (requires manual data extraction from OCR text)
python3 generate_excel.py output.xlsx
```

### Step 5: Validation (Optional)
```bash
# Run tests to validate extraction accuracy
python3 test_sorting.py

# Run demo to verify end-to-end workflow
python3 test_demo.py
```

### Step 6: Review Results
- Show extracted data summary to user
- Display performance statistics (time, speed)
- Ask if they want to adjust any extraction parameters
- Verify output file locations
- Check if further processing is needed

## Performance Optimization - Concurrent Processing

### Overview
The batch extraction script now supports **high-performance concurrent processing** using Python multiprocessing. This can provide **2-8x speed improvement** for large batches.

### When to Use Concurrent Mode

| File Count | Recommended Mode | Workers | Expected Speedup |
|------------|-----------------|---------|------------------|
| 1-10 files | Sequential | N/A | Baseline |
| 10-30 files | Concurrent | 2 | ~2x faster |
| 30-100 files | Concurrent | 4 | ~4x faster |
| 100+ files | Concurrent | 6-8 | ~6-8x faster |

### Usage Examples

**Basic Concurrent Processing:**
```bash
python3 batch_extract.py /path/to/patents --concurrent
```

**Optimized for Medium Batches (20-50 files):**
```bash
python3 batch_extract.py /path/to/patents --concurrent --workers=4
```

**Optimized for Large Batches (100+ files):**
```bash
python3 batch_extract.py /path/to/patents --concurrent --workers=8
```

**With Custom Output File:**
```bash
python3 batch_extract.py /path/to/patents results.json --concurrent --workers=4
```

### Performance Metrics

After processing, the script displays:
- **Total time**: Complete processing duration
- **Average time per file**: Helps identify bottlenecks
- **Processing mode**: Sequential vs Concurrent (workers=N)
- **Success rate**: Files processed successfully

Example output:
```
================================================================================
Processing complete: 14 files processed successfully
Total time: 109.09 seconds
Average time per file: 7.79 seconds
```

### Concurrent Processing Notes

**Advantages:**
- ✅ Significantly faster for large batches
- ✅ Automatic CPU core detection
- ✅ Better resource utilization
- ✅ Real-time progress tracking

**Considerations:**
- ⚠️ Higher memory usage (each worker loads OCR engine)
- ⚠️ May not be faster for very small batches (< 10 files)
- ⚠️ Limit workers to avoid memory issues (recommended max: 8)

**Best Practices:**
- Start with `--workers=2` for testing
- Increase workers gradually based on available RAM
- Monitor system resources during processing
- Use sequential mode if encountering memory issues

## Project Structure

### Core Scripts

**`extract_ocr.py`** - Main OCR extraction script
- Uses Tesseract OCR for text extraction (local, no API required)
- Processes patent certificate images and PDFs
- Extracts structured data including patent numbers, dates, and inventor information
- Key function: `extract_text()` for OCR processing
- Supports various image formats (JPG, PNG, TIFF, PDF)
- Supports Chinese and English text recognition

**`batch_extract.py`** - Batch processing script (NEW: Concurrent Support)
- Processes multiple patent certificates in bulk
- **Two modes**: Sequential (default) and Concurrent (optional)
- **Concurrent processing**: Uses multiprocessing for 2-8x speed improvement
- Configurable worker processes (`--workers=N`)
- Outputs extracted data to JSON format
- Handles error logging and validation
- Progress tracking for large batches
- Performance metrics (total time, average per file)

**`generate_excel.py`** - Excel generation utility
- Converts extracted JSON data to Excel spreadsheets
- Creates formatted tables with patent information
- Includes sorting and data validation functions
- Uses `openpyxl` library for Excel manipulation
- Supports custom column ordering and styling
- Auto-adjusts column widths for readability

**`test_sorting.py`** - Data sorting and validation tests
- Tests sorting algorithms for patent data
- Validates data extraction accuracy
- Compares extracted data against expected results
- Unit tests for data processing functions

**`test_demo.py`** - Demonstration and testing script
- Provides usage examples
- Tests end-to-end workflow
- Validates OCR accuracy on sample certificates
- Quick verification of environment setup

### Configuration Files

**`SKILL.md`** - Skill documentation (this file)
- Describes the skill's capabilities and usage
- Provides setup instructions
- Documents dependencies and requirements
- Performance optimization guidelines

**`llm_prompt.md`** (in references/)
- Contains prompts for LLM-assisted data extraction
- Defines expected data formats
- Provides extraction guidelines
- Field mapping and parsing rules

**`test_sorted_data.json`** - Test data fixture
- Sample extracted patent data
- Used for validation and testing
- Contains reference data for comparison
- Expected output format examples

## Expected Output Format

### JSON Output Structure
```json
{
  "patent_number": "ZL 2013 1 0435279.1",
  "patent_title": "一种XXX化合物在制备药物中的应用",
  "patent_type": "发明专利",
  "inventors": ["张三", "李四"],
  "patent_holder": "XX生物医药技术有限公司",
  "application_date": "2013-09-23"
}
```

### Excel Output Structure
| 专利号 | 专利名称 | 权利人 | 专利类型 | 发明人 | 申请日期 |
|--------|----------|--------|----------|--------|----------|
| ZL 2013 1 0435279.1 | 一种XXX化合物的制备方法 | XX生物医药技术有限公司 | 发明专利 | 张三;李四 | 2013-09-23 |

Excel features:
- Header row with blue background and white text
- Auto-adjusted column widths
- Borders for visual grouping
- Thick borders between different patent holders
- Sorted by: Patent Holder → Patent Type → Application Date

## Key Technologies
- **Python 3.10+** - Programming language
- **Tesseract OCR** - Open-source OCR engine (local, no API needed)
- **pdf2image** - PDF to image conversion
- **OpenPyXL** - Excel file generation and manipulation
- **JSON** - Intermediate data storage format
- **Regular Expressions** - Pattern matching for data extraction
- **PIL/Pillow** - Image preprocessing
- **concurrent.futures** - Multiprocessing for concurrent OCR
- **multiprocessing** - Process pool management

## Error Handling

### Common Issues and Solutions

**1. Tesseract Not Installed**
```
Error: Tesseract OCR is not installed or not in PATH
```
Solution:
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Verify installation
tesseract --version
```

**2. Image Format Not Supported**
```
Error: Cannot identify image file
```
Solution: Convert image to supported format (JPG, PNG, TIFF)
```bash
convert input.webp output.jpg  # Using ImageMagick
```

**3. OCR Extraction Incomplete**
- Check image quality and resolution (recommend 300 DPI or higher)
- Ensure certificate is clearly visible without watermarks
- Try preprocessing: adjust brightness/contrast

**4. Missing Dependencies**
```
ModuleNotFoundError: No module named 'pdf2image'
```
Solution:
```bash
pip install pdf2image openpyxl Pillow
```

**5. Permission Denied for Output Directory**
- Create output directory with proper permissions
- Verify write access to target location

**6. Concurrent Processing Memory Issues (Exit Code 137)**
```
Exit code 137 (Process killed - out of memory)
```
Solution: Reduce number of workers
```bash
# Instead of --workers=8, try:
python3 batch_extract.py /path/to/patents --concurrent --workers=2

# Or use sequential mode:
python3 batch_extract.py /path/to/patents
```

**7. Slow Processing Speed**
Solution: Enable concurrent processing
```bash
# Add --concurrent flag for faster processing
python3 batch_extract.py /path/to/patents --concurrent --workers=4
```

## User Interaction Guidelines

### Initial Questions to Ask
1. "How many patent certificates do you need to process?"
   - If 20+, recommend concurrent mode
2. "Please provide the path to your certificate image(s) or folder"
3. "What output format would you prefer: Excel, JSON, or both?"
4. "Are there any specific fields you need extracted beyond the standard patent information?"
5. "Do you want to use high-performance concurrent processing? (recommended for 20+ files)"

### Progress Updates
- Show extraction progress for batch processing
- Display intermediate results for user verification
- Show performance metrics (time elapsed, files remaining)
- Ask for confirmation before overwriting existing files

### Result Verification
- Display a sample of extracted data for user review
- Show performance statistics (total time, speed)
- Ask if the extraction looks accurate
- Offer to re-run with adjusted parameters if needed

## Example Usage Scenarios

### Scenario 1: Single Certificate Extraction
```
User: "我有一张专利证书图片，帮我提取里面的信息"

Claude:
1. Checks Tesseract OCR installation
2. Asks for image path
3. Runs extract_ocr.py
4. Shows extracted data
5. Asks if user wants Excel output
6. Generates Excel if requested
```

### Scenario 2: Small Batch Processing (< 20 files)
```
User: "I have 15 patent certificates in a folder, extract all the data"

Claude:
1. Verifies Tesseract OCR is installed
2. Asks for folder path and output preferences
3. Runs batch_extract.py in sequential mode
4. Shows summary of successful/failed extractions
5. Generates consolidated Excel report
6. Validates data sorting with test_sorting.py
```

### Scenario 3: Large Batch Processing (50+ files) - High Performance
```
User: "我有100个专利证书需要批量处理，要快速完成"

Claude:
1. Verifies Tesseract OCR installation
2. Asks for folder path
3. Recommends concurrent processing mode
4. Suggests optimal worker count based on file count
5. Runs: batch_extract.py --concurrent --workers=6
6. Shows real-time progress updates
7. Displays performance metrics (e.g., "Total time: 180s, Avg: 1.8s/file")
8. Generates consolidated Excel report
9. Summary: "Processed 100 files in 3 minutes (vs 15 minutes sequential)"
```

### Scenario 4: Performance Comparison
```
User: "批量处理速度太慢了"

Claude:
1. Asks: "How many files are you processing?"
2. Checks if user is using sequential mode
3. Recommends switching to concurrent mode
4. Suggests: --concurrent --workers=4
5. Estimates time savings: "Should reduce from 10 min to ~2.5 min"
6. Runs concurrent processing
7. Shows before/after performance comparison
```

### Scenario 5: Validation and Testing
```
User: "Test if the patent extractor is working correctly"

Claude:
1. Runs test_demo.py to verify environment
2. Processes test certificates
3. Compares results with test_sorted_data.json
4. Reports accuracy metrics
5. Suggests adjustments if accuracy is low
```

## Best Practices

1. **Always verify environment setup** before processing user data
2. **Recommend concurrent mode** for batches of 20+ files
3. **Start with fewer workers** (2-4) and increase if stable
4. **Show progress updates** for operations taking more than a few seconds
5. **Display performance metrics** to help users optimize settings
6. **Validate extraction results** by showing samples to the user
7. **Handle errors gracefully** with clear explanations and solutions
8. **Preserve original images** - never delete or overwrite input files
9. **Create backups** before overwriting existing output files
10. **Log errors** to help with debugging and quality improvement
11. **Monitor memory usage** when using high worker counts
12. **Educate users** about performance tradeoffs (speed vs memory)

## Performance Considerations

### Concurrent Processing
- **Optimal Workers**: 2-8 processes (based on CPU cores and RAM)
- **Memory Usage**: ~200-500MB per worker process
- **Speed Improvement**: 2-8x faster than sequential
- **Best For**: Batches of 20+ files

### Sequential Processing
- **Memory Usage**: Minimal (~100MB)
- **Speed**: Baseline (1x)
- **Best For**: Small batches (< 20 files), low-memory systems

### Recommendations by Batch Size
- **1-10 files**: Sequential mode (simple, reliable)
- **10-30 files**: Concurrent with 2-4 workers
- **30-100 files**: Concurrent with 4-6 workers
- **100+ files**: Concurrent with 6-8 workers

### System Requirements
- **Minimum**: 2GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4+ CPU cores for concurrent processing
- **Optimal**: 16GB RAM, 8+ CPU cores for large batches

## Post-Processing Options

After extraction, Claude can offer:
- **Data cleaning**: Remove duplicates, standardize formats
- **Sorting**: By date, patent number, inventor name, etc.
- **Filtering**: Extract subset based on criteria (date range, type, etc.)
- **Export formats**: CSV, JSON, XLSX, or custom formats
- **Data analysis**: Statistics, summaries, visualizations
- **Performance tuning**: Adjust worker count for optimal speed

## Integration Notes

This skill can be combined with other skills for:
- **Document management**: Organize extracted data into databases
- **Report generation**: Create formatted reports using docx/pptx skills
- **Data validation**: Cross-reference with patent databases
- **Workflow automation**: Trigger downstream processes based on extracted data
- **Batch operations**: Process multiple folders in parallel

## Command Reference

### Basic Commands
```bash
# Single file OCR
python3 extract_ocr.py certificate.pdf

# Batch sequential
python3 batch_extract.py /path/to/folder

# Batch concurrent (auto workers)
python3 batch_extract.py /path/to/folder --concurrent

# Batch concurrent (custom workers)
python3 batch_extract.py /path/to/folder --concurrent --workers=4

# With output file
python3 batch_extract.py /path/to/folder results.json --concurrent --workers=4

# Generate Excel
python3 generate_excel.py output.xlsx

# Run tests
python3 test_demo.py
python3 test_sorting.py
```

### Performance Optimization Commands
```bash
# Fast processing (2 workers)
python3 batch_extract.py /path/to/folder --concurrent --workers=2

# Balanced (4 workers)
python3 batch_extract.py /path/to/folder --concurrent --workers=4

# Maximum speed (8 workers) - requires sufficient RAM
python3 batch_extract.py /path/to/folder --concurrent --workers=8
```

---

## Skill Metadata
- **Version**: 2.0 (Added concurrent processing support)
- **Category**: Document Processing, OCR, Data Extraction
- **Language Support**: Chinese (primary), English
- **OCR Engine**: Tesseract OCR (local, open-source)
- **Performance**: Sequential mode (baseline), Concurrent mode (2-8x faster)
- **Dependencies**: Python 3.10+, Tesseract OCR, pdf2image, openpyxl, Pillow
- **License**: Check repository for license information
