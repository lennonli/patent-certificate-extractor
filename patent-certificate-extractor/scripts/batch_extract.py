#!/usr/bin/env python3
"""
Batch processing script for patent certificates

Extracts OCR text from multiple patent certificate files and uses LLM to extract structured information.
Supports both sequential and concurrent processing for improved performance.
"""

import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import time


def extract_text_from_file(file_path: Path, ocr_script_path: Path) -> str:
    """Extract OCR text from a single file"""
    result = subprocess.run(
        ['python3', str(ocr_script_path), str(file_path)],
        capture_output=True,
        text=True
    )
    return result.stdout


def save_extracted_text(file_path: Path, text: str):
    """Save extracted text to a file"""
    output_file = file_path.parent / f"{file_path.stem}_extracted.txt"
    output_file.write_text(text, encoding='utf-8')
    return output_file


def process_single_file(args: tuple) -> Optional[Dict[str, Any]]:
    """
    Process a single PDF file (wrapper for concurrent execution)

    Args:
        args: Tuple of (pdf_file, ocr_script_path, file_index, total_files)

    Returns:
        Dictionary with extracted data or None if failed
    """
    pdf_file, ocr_script_path, idx, total = args

    try:
        # Extract OCR text
        text = extract_text_from_file(pdf_file, ocr_script_path)

        if text:
            # Save extracted text for manual review
            saved_file = save_extracted_text(pdf_file, text)
            print(f"  [{idx}/{total}] ✓ {pdf_file.name}")

            return {
                'filename': pdf_file.name,
                'file_path': str(pdf_file),
                'extracted_text': text,
                'extracted_text_file': str(saved_file)
            }
        else:
            print(f"  [{idx}/{total}] ✗ Failed to extract text from {pdf_file.name}")
            return None

    except Exception as e:
        print(f"  [{idx}/{total}] ✗ Error processing {pdf_file.name}: {e}")
        return None


def batch_process_sequential(folder_path: Path, ocr_script_path: Path) -> List[Dict[str, Any]]:
    """
    Process all PDF files in a folder sequentially (original implementation)

    Args:
        folder_path: Path to folder containing PDF files
        ocr_script_path: Path to OCR extraction script

    Returns:
        List of dictionaries with extracted data
    """
    pdf_files = sorted(folder_path.glob("*.pdf"))
    results = []

    print(f"Found {len(pdf_files)} PDF files to process")
    print("Processing mode: Sequential")
    print("=" * 80)

    for idx, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file.name}")

        # Extract OCR text
        text = extract_text_from_file(pdf_file, ocr_script_path)

        if text:
            # Save extracted text for manual review
            saved_file = save_extracted_text(pdf_file, text)
            print(f"  ✓ Extracted text saved to: {saved_file.name}")

            # Store for LLM processing
            results.append({
                'filename': pdf_file.name,
                'file_path': str(pdf_file),
                'extracted_text': text,
                'extracted_text_file': str(saved_file)
            })
        else:
            print(f"  ✗ Failed to extract text")

    return results


def batch_process_concurrent(folder_path: Path, ocr_script_path: Path, max_workers: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Process all PDF files in a folder concurrently using multiprocessing

    Args:
        folder_path: Path to folder containing PDF files
        ocr_script_path: Path to OCR extraction script
        max_workers: Maximum number of worker processes (default: CPU count)

    Returns:
        List of dictionaries with extracted data
    """
    pdf_files = sorted(folder_path.glob("*.pdf"))
    results = []

    # Default to CPU count if not specified
    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), len(pdf_files))

    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"Processing mode: Concurrent (workers={max_workers})")
    print("=" * 80)
    print()

    # Prepare arguments for each file
    task_args = [
        (pdf_file, ocr_script_path, idx, len(pdf_files))
        for idx, pdf_file in enumerate(pdf_files, 1)
    ]

    # Process files concurrently
    completed_count = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(process_single_file, args): args[0]
            for args in task_args
        }

        # Collect results as they complete
        for future in as_completed(future_to_file):
            completed_count += 1
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                pdf_file = future_to_file[future]
                print(f"  [{completed_count}/{len(pdf_files)}] ✗ Unexpected error with {pdf_file.name}: {e}")

    # Sort results by filename to maintain consistent order
    results.sort(key=lambda x: x['filename'])

    return results


def save_batch_results(results: List[Dict[str, Any]], output_file: Path):
    """Save batch processing results to JSON"""
    # Remove extracted_text to avoid huge files
    results_copy = []
    for result in results:
        result_copy = result.copy()
        result_copy.pop('extracted_text', None)
        results_copy.append(result_copy)

    output_file.write_text(json.dumps(results_copy, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\n✓ Batch results saved to: {output_file}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python batch_extract.py <folder_path> [output_json] [--concurrent] [--workers=N]")
        print("\nExamples:")
        print("  python batch_extract.py ./patents")
        print("  python batch_extract.py ./patents --concurrent")
        print("  python batch_extract.py ./patents batch_results.json --concurrent --workers=8")
        print("\nOptions:")
        print("  --concurrent    Enable concurrent processing (default: sequential)")
        print("  --workers=N     Set number of worker processes (default: CPU count)")
        sys.exit(1)

    # Parse arguments
    folder_path = Path(sys.argv[1])

    # Check for optional arguments
    use_concurrent = '--concurrent' in sys.argv
    output_json = None
    max_workers = None

    for arg in sys.argv[2:]:
        if arg.startswith('--workers='):
            try:
                max_workers = int(arg.split('=')[1])
            except ValueError:
                print(f"Warning: Invalid workers value '{arg}', using default")
        elif not arg.startswith('--'):
            output_json = arg

    if not folder_path.exists():
        print(f"Error: Folder not found: {folder_path}")
        sys.exit(1)

    # Path to OCR script
    script_dir = Path(__file__).parent
    ocr_script = script_dir / 'extract_ocr.py'

    if not ocr_script.exists():
        print(f"Error: OCR script not found: {ocr_script}")
        sys.exit(1)

    # Start timing
    start_time = time.time()

    # Process files
    if use_concurrent:
        results = batch_process_concurrent(folder_path, ocr_script, max_workers)
    else:
        results = batch_process_sequential(folder_path, ocr_script)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Save results
    output_file = Path(output_json) if output_json else folder_path / 'batch_extraction_results.json'
    save_batch_results(results, output_file)

    print(f"\n{'='*80}")
    print(f"Processing complete: {len(results)} files processed successfully")
    print(f"Total time: {elapsed_time:.2f} seconds")
    if len(results) > 0:
        print(f"Average time per file: {elapsed_time/len(results):.2f} seconds")
    print("\nNext steps:")
    print("1. Review the extracted text files (*_extracted.txt)")
    print("2. Use LLM to extract structured information from the saved results")
    print(f"3. Generate Excel file with: python generate_excel.py <output.xlsx>")


if __name__ == "__main__":
    main()
