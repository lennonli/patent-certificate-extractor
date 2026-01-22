# Patent Extraction Skill (AI Enhanced)

This tool extracts information from Chinese Patent Certificates (PDF or Image) using **OCR** and **LLM** for high accuracy.

It supports:
- **Google Gemini** (Preferred for accuracy and large context)
- **OpenAI-compatible models** (DeepSeek, GPT-4, etc.)
- **Regex Fallback** (Basic)

## Setup

### Option 1: Using Gemini (Recommended)
You need a Google AI Studio API Key. 

1. Export your key:
   ```bash
   export GEMINI_API_KEY="AIzaSy..."
   ```
2. Run the tool:
   ```bash
   python3 patent_skill/extractor.py /path/to/files/
   ```

### Option 2: Using OpenAI / DeepSeek
1. Export your key:
   ```bash
   export OPENAI_API_KEY="sk-..."
   # Optional: Set Base URL for DeepSeek
   # export OPENAI_BASE_URL="https://api.deepseek.com"
   ```
2. Run the tool:
   ```bash
   python3 patent_skill/extractor.py /path/to/files/ --provider openai
   ```

### Option 3: Basic Regex (No API Key)
Just run without keys.
```bash
python3 patent_skill/extractor.py /path/to/files/
```
