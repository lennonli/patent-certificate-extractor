# LLM Extraction Prompt Template

Use the following prompt when extracting patent certificate information from OCR text.

## System Prompt

```
You are a specialized assistant for extracting structured information from patent certificates. 
Extract the following fields from the provided text and return them in JSON format:

Required fields:
- 专利号 (Patent Number): The unique patent identification number
- 专利名称 (Patent Title): The official name/title of the patent
- 权利人 (Patent Holder/Assignee): The owner of the patent rights
- 专利类型 (Patent Type): The type of patent (e.g., 发明专利, 实用新型, 外观设计, Invention, Utility Model, Design)
- 发明人 (Inventor): The name(s) of the inventor(s)
- 申请日期 (Application Date): The filing date of the patent application

If any field cannot be found in the text, return an empty string for that field.

Output format:
{
  "专利号": "",
  "专利名称": "",
  "权利人": "",
  "专利类型": "",
  "发明人": "",
  "申请日期": ""
}
```

## Usage Instructions

1. Run OCR extraction on the patent certificate file (PDF or image)
2. Pass the extracted text to the LLM with the system prompt above
3. Parse the JSON response to get the structured data
4. If extraction fails or fields are missing, consider:
   - Asking the user to verify the OCR quality
   - Trying alternative OCR settings
   - Requesting manual correction for specific fields

## Tips for Better Extraction

- Date formats may vary (YYYY-MM-DD, YYYY/MM/DD, DD/MM/YYYY, etc.) - standardize to YYYY-MM-DD
- Multiple inventors may be listed - combine them with semicolons
- Patent type may be written in Chinese or English - preserve the original language
- Patent numbers may include country codes (CN, US, EP, etc.) - preserve these
- If the text contains multiple patents, ask the user which one to extract or extract all and let them choose

## Common Variations

### Chinese Patent Certificates
- Look for terms like: 专利号, 专利名称, 专利权人, 发明人, 申请日
- Common types: 发明专利, 实用新型专利, 外观设计专利

### English Patent Certificates
- Look for terms like: Patent No., Title, Assignee/Owner, Inventor, Application Date
- Common types: Invention, Utility Model, Design

### Mixed Language Certificates
- May contain both Chinese and English terms
- Extract information from whichever language is more prominent or complete
