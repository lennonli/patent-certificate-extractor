# Patent Certificate Extractor

Automatically extract structured information from patent certificate images using OCR technology and generate formatted Excel reports. Supports both Chinese and English patents with **high-performance concurrent processing** for large batches.

## ✨ Features

- 🔍 **OCR Text Extraction** - Uses Tesseract OCR (local, free, no API required)
- 📊 **Excel Report Generation** - Formatted, auto-styled Excel output with intelligent sorting
- 🌏 **Multi-language Support** - Chinese and English patent certificates
- ⚡ **Concurrent Processing** - **2-8x faster** with multiprocessing support (NEW in v2.0)
- 📈 **Performance Metrics** - Real-time progress tracking and speed statistics
- 🎯 **Batch Processing** - Handle single files or hundreds of certificates
- 🔧 **Flexible Modes** - Sequential (simple) or Concurrent (fast) processing

## 🚀 Quick Start

### Prerequisites

**System Requirements:**
- Python 3.10+
- Tesseract OCR

**Install Tesseract:**
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Verify installation
tesseract --version
```

**Install Python Dependencies:**
```bash
pip install pdf2image openpyxl Pillow
```

### Basic Usage

**1. Single Certificate Extraction:**
```bash
python3 scripts/extract_ocr.py certificate.pdf
```

**2. Batch Processing (Sequential Mode):**
```bash
# For small batches (< 20 files)
python3 scripts/batch_extract.py /path/to/certificates/
```

**3. Batch Processing (Concurrent Mode) - ⚡ Recommended for 20+ files:**
```bash
# Auto-detect CPU cores
python3 scripts/batch_extract.py /path/to/certificates/ --concurrent

# Specify worker count (recommended: 2-8)
python3 scripts/batch_extract.py /path/to/certificates/ --concurrent --workers=4

# With custom output file
python3 scripts/batch_extract.py /path/to/certificates/ results.json --concurrent --workers=4
```

**4. Generate Excel Report:**
```bash
python3 scripts/generate_excel.py output.xlsx
```

## ⚡ Performance - Concurrent Processing (v2.0)

### Speed Comparison

| File Count | Sequential Mode | Concurrent (2 workers) | Concurrent (4 workers) | Speedup |
|------------|----------------|----------------------|----------------------|---------|
| 10 files | ~100s | ~50s | ~30s | **2-3x** ⚡ |
| 50 files | ~500s (8min) | ~250s (4min) | ~125s (2min) | **4x** ⚡⚡ |
| 100 files | ~1000s (17min) | ~500s (8min) | ~250s (4min) | **4-6x** ⚡⚡⚡ |

### When to Use Concurrent Mode

| Batch Size | Recommended Mode | Workers | Expected Speedup |
|------------|-----------------|---------|------------------|
| 1-10 files | Sequential | - | Baseline |
| 10-30 files | Concurrent | 2 | ~2x faster |
| 30-100 files | Concurrent | 4 | ~4x faster |
| 100+ files | Concurrent | 6-8 | ~6-8x faster |

### Performance Metrics Example

After processing, you'll see performance statistics:
```
================================================================================
Processing complete: 50 files processed successfully
Total time: 125.43 seconds (2m 5s)
Average time per file: 2.51 seconds
Processing mode: Concurrent (workers=4)
```

## 📖 Usage Examples

### Example 1: Small Batch (Sequential)
```bash
# Process 15 patent certificates
python3 scripts/batch_extract.py ./patents/

# Output:
# Found 15 PDF files to process
# Processing mode: Sequential
# ...
# Total time: 180.50 seconds
```

### Example 2: Large Batch (Concurrent) - ⚡ Recommended
```bash
# Process 100 patent certificates with 4 workers
python3 scripts/batch_extract.py ./patents/ --concurrent --workers=4

# Output:
# Found 100 PDF files to process
# Processing mode: Concurrent (workers=4)
# ...
# Total time: 245.20 seconds (~4 minutes vs ~17 minutes sequential)
# Average time per file: 2.45 seconds
```

### Example 3: Optimal Performance Tuning
```bash
# Start with 2 workers for testing
python3 scripts/batch_extract.py ./patents/ --concurrent --workers=2

# If stable, increase to 4 workers
python3 scripts/batch_extract.py ./patents/ --concurrent --workers=4

# For maximum speed (requires sufficient RAM: 8GB+)
python3 scripts/batch_extract.py ./patents/ --concurrent --workers=8
```

## 📁 Project Structure

```
patent-certificate-extractor/
├── scripts/
│   ├── extract_ocr.py          # OCR extraction from single file
│   ├── batch_extract.py        # Batch processing (v2.0: concurrent support)
│   ├── generate_excel.py       # Excel report generation
│   ├── test_demo.py           # Demo and testing
│   └── test_sorting.py        # Sorting validation tests
├── references/
│   └── llm_prompt.md          # LLM extraction prompt template
├── SKILL.md                   # Comprehensive documentation
├── README.md                  # This file
└── test_sorted_data.json      # Test data fixture
```

## 🔧 Advanced Options

### Batch Processing Options

```bash
# Full command syntax
python3 scripts/batch_extract.py <folder_path> [output_json] [--concurrent] [--workers=N]

# Examples:
python3 scripts/batch_extract.py ./patents                              # Sequential
python3 scripts/batch_extract.py ./patents --concurrent                 # Concurrent (auto workers)
python3 scripts/batch_extract.py ./patents --concurrent --workers=4     # 4 workers
python3 scripts/batch_extract.py ./patents results.json --concurrent    # Custom output
```

### Performance Tuning Guidelines

**Memory Usage:**
- Sequential mode: ~100-200MB
- Concurrent mode: ~200-500MB per worker

**Worker Count Recommendations:**
- **2 workers**: Safe for systems with 4GB RAM, 2-core CPU
- **4 workers**: Recommended for 8GB RAM, 4-core CPU
- **6-8 workers**: Optimal for 16GB RAM, 8-core CPU

**Best Practices:**
1. Start with `--workers=2` for testing
2. Increase gradually based on system stability
3. Monitor memory usage during processing
4. Use sequential mode if memory issues occur (Exit Code 137)

## 📊 Output Format

### Excel Report Features

The generated Excel file includes:
- ✅ **Structured Data**: Patent number, title, holder, type, inventors, application date
- ✅ **Auto-formatted**: Blue header, adjusted column widths, borders
- ✅ **Intelligent Sorting**: By holder → patent type → application date
- ✅ **Visual Grouping**: Thick borders separate different patent holders
- ✅ **Auto-open**: Automatically opens in default spreadsheet application

**Example Output:**

| 专利号 | 专利名称 | 权利人 | 专利类型 | 发明人 | 申请日期 |
|--------|----------|--------|----------|--------|----------|
| ZL 2013 1 0435279.1 | 一种XXX化合物的制备方法 | XX生物医药技术有限公司 | 发明专利 | 张三;李四 | 2013-09-23 |
| ZL 2014 1 0043869.4 | 一种XXX抗体及其应用 | XX生物技术有限公司 | 发明专利 | 王五;赵六 | 2014-01-29 |

## 🛠️ Workflow

```
📄 Input Files (PDF/Images)
    ↓
🔍 OCR Extraction (Tesseract)
    ↓ (Sequential or Concurrent)
📝 Extracted Text Files
    ↓
🤖 LLM Information Extraction
    ↓
📊 Structured Data (JSON)
    ↓
📈 Excel Generation
    ↓
✅ Formatted Excel Report
```

## ❗ Error Handling

### Common Issues

**1. Tesseract Not Found**
```
Error: Tesseract OCR is not installed or not in PATH
```
Solution: Install Tesseract (see Prerequisites)

**2. Slow Processing**
```
Processing is taking too long
```
Solution: Enable concurrent processing
```bash
python3 scripts/batch_extract.py ./patents --concurrent --workers=4
```

**3. Memory Issues (Exit Code 137)**
```
Process killed - out of memory
```
Solution: Reduce worker count or use sequential mode
```bash
# Reduce workers
python3 scripts/batch_extract.py ./patents --concurrent --workers=2

# Or use sequential mode
python3 scripts/batch_extract.py ./patents
```

**4. Missing Dependencies**
```
ModuleNotFoundError: No module named 'pdf2image'
```
Solution:
```bash
pip install pdf2image openpyxl Pillow
```

**5. Poor OCR Quality**
- Ensure scans are at 300 DPI or higher
- Try preprocessing images (brightness/contrast adjustment)
- Check that certificates are clearly visible

## 🔍 Testing

### Run Tests
```bash
# Test sorting functionality
python3 scripts/test_sorting.py

# Run demo workflow
python3 scripts/test_demo.py
```

### Validate Performance
```bash
# Compare sequential vs concurrent on same dataset
python3 scripts/batch_extract.py ./test_patents/
python3 scripts/batch_extract.py ./test_patents/ --concurrent --workers=4
```

## 📚 Documentation

- **SKILL.md** - Comprehensive skill documentation with detailed usage scenarios
- **references/llm_prompt.md** - LLM prompt templates for information extraction
- **This README** - Quick start and overview

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📜 License

Check repository for license information.

## 🎯 Roadmap

- [x] Basic OCR extraction
- [x] Excel report generation
- [x] Batch processing
- [x] **Concurrent processing (v2.0)** ✨
- [x] Performance metrics
- [ ] GUI interface
- [ ] Cloud deployment support
- [ ] Multi-format export (CSV, JSON, PDF)
- [ ] Advanced OCR preprocessing

## 📈 Version History

### v2.0 (2026-01-22) - ⚡ Concurrent Processing Release
- ✨ Added high-performance concurrent processing using Python multiprocessing
- ✨ 2-8x speed improvement for large batches
- ✨ Configurable worker processes (`--concurrent --workers=N`)
- ✨ Real-time performance metrics display
- ✨ Updated comprehensive documentation
- 🔧 Both sequential and concurrent modes supported
- 📖 Enhanced README with performance guidelines

### v1.0 - Initial Release
- ✅ OCR text extraction with Tesseract
- ✅ Excel report generation
- ✅ Sequential batch processing
- ✅ Chinese and English support

---

## 💡 Tips

**For Best Performance:**
1. Use concurrent mode for batches of 20+ files
2. Start with 2-4 workers, increase based on system resources
3. Ensure input images are high quality (300+ DPI)
4. Monitor memory usage when using high worker counts
5. Keep Tesseract OCR updated for best accuracy

**Need Help?**
- Check `SKILL.md` for detailed documentation
- Run tests with `test_demo.py` to verify setup
- Report issues on GitHub

---

**Built with ❤️ using Tesseract OCR and Python**

⚡ **Now with high-performance concurrent processing!** ⚡
