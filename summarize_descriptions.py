"""
Script to summarize job descriptions using Perplexity API

This script processes job description JSON files and summarizes descriptions
that exceed MAX_DESCRIPTION_LENGTH (900 chars) using the Perplexity API.

KEY FEATURES:
- Batched processing: Groups up to BATCH_SIZE (5) descriptions per API call
- Efficient API usage: Reduces costs and improves speed vs individual calls
- Structured parsing: Uses [JOB_N] markers to reliably extract batch results
- Fallback support: Can fall back to single-item processing if needed
- Test mode: Run with --test to process only the first batch

USAGE:
1. Set PERPLEXITY_API_KEY in .env file
2. Configure DESCRIPTION_FILES list with files to process
3. Run: python3 summarize_descriptions.py [--test]

OPTIONS:
  --test, -t    Process only the first batch (useful for testing)

The script modifies files in-place, replacing long descriptions with summaries.
"""

import json
import os
import sys
import argparse
from typing import Optional
from dotenv import load_dotenv
import requests


# Load environment variables from .env file
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("perplexity_api_key")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

# Description files to process
DESCRIPTION_FILES = [
    #"ai_jobs_descriptions.json",        # AshbyHQ
    "ai_jobs_greenhouse_descriptions.json",  # Greenhouse
    #"ai_jobs_lever_descriptions.json",  # Lever
]

MAX_DESCRIPTION_LENGTH = 600
BATCH_SIZE = 10  # Number of descriptions to process in one API call


def validate_api_key():
    """Validate that API key is loaded"""
    if not PERPLEXITY_API_KEY:
        print("Error: perplexity_api_key not found in .env file", file=sys.stderr)
        sys.exit(1)
    print(f"✓ API key loaded (length: {len(PERPLEXITY_API_KEY)} chars)")


def summarize_descriptions_batch(descriptions: list[tuple[int, str]]) -> dict[int, Optional[str]]:
    """
    Summarize multiple descriptions in a single API call.
    
    Args:
        descriptions: List of tuples (index, description)
    
    Returns:
        Dictionary mapping index to summarized description
    """
    if not descriptions:
        return {}
    
    # Build batch prompt
    batch_items = []
    for idx, desc in descriptions:
        batch_items.append(f"[JOB_{idx}]\n{desc}\n")
    
    batch_text = "\n".join(batch_items)
    
    prompt = f"""Summarize each of the following job descriptions in less than 500 characters each, keeping the most important information about responsibilities, requirements, and benefits. Be concise and clear. Do not add any information that is not present in the original descriptions. Do not add information about the company or job title.

For each job, output ONLY in this format:
[JOB_N]
<summary text>

Job Descriptions:
{batch_text}

Provide only the summaries in the exact format shown above, no additional text."""
    
    try:
        response = requests.post(
            PERPLEXITY_API_URL,
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "max_tokens": 3000,
                "temperature": 0.1,
            },
            timeout=60,
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            
            # Parse the batch response
            results = {}
            current_idx = None
            current_summary = []
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('[JOB_') and line.endswith(']'):
                    # Save previous summary if exists
                    if current_idx is not None and current_summary:
                        results[current_idx] = '\n'.join(current_summary).strip()
                    
                    # Extract new index
                    try:
                        current_idx = int(line[5:-1])
                        current_summary = []
                    except ValueError:
                        continue
                elif current_idx is not None:
                    current_summary.append(line)
            
            # Save last summary
            if current_idx is not None and current_summary:
                results[current_idx] = '\n'.join(current_summary).strip()
            
            return results
        else:
            print(f"  ✗ API error {response.status_code}: {response.text}", file=sys.stderr)
            return {}
    
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Request error: {e}", file=sys.stderr)
        return {}
    except (KeyError, json.JSONDecodeError) as e:
        print(f"  ✗ Response parsing error: {e}", file=sys.stderr)
        return {}


def summarize_description(description: str) -> Optional[str]:
    """Summarize description using Perplexity API (single item fallback)"""
    if not description or len(description) < 100:
        return description
    
    if len(description) <= MAX_DESCRIPTION_LENGTH:
        return description
    
    prompt = f"""Summarize the following job description in less than 500 characters, keeping the most important information about responsibilities, requirements, and benefits. Be concise and clear. Do not add any information that is not present in the original description. Do not add information about the company or job title.

Job Description:
{description}

Provide only the summary, no additional text."""
    
    try:
        response = requests.post(
            PERPLEXITY_API_URL,
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "sonar",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7,
            },
            timeout=30,
        )
        
        if response.status_code == 200:
            data = response.json()
            summary = data["choices"][0]["message"]["content"].strip()
            return summary
        else:
            print(f"  ✗ API error {response.status_code}: {response.text}", file=sys.stderr)
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Request error: {e}", file=sys.stderr)
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"  ✗ Response parsing error: {e}", file=sys.stderr)
        return None


def process_file(file_path: str, test_mode: bool = False) -> tuple[int, int, int]:
    """Process a single description file
    
    Args:
        file_path: Path to the JSON file to process
        test_mode: If True, only process the first batch
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 0, 0, 0
    
    print(f"\nProcessing: {file_path}")
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ✗ Error reading file: {e}", file=sys.stderr)
        return 0, 0, 0
    
    if not isinstance(data, list):
        print(f"  ✗ Invalid file format: expected list", file=sys.stderr)
        return 0, 0, 0
    
    total = len(data)
    summarized = 0
    skipped = 0
    
    # Collect items that need summarization
    items_to_summarize = []
    
    for idx, item in enumerate(data):
        if not isinstance(item, dict) or "description" not in item:
            skipped += 1
            continue
        
        original_len = len(item["description"])
        
        # Skip if already short enough
        if original_len <= MAX_DESCRIPTION_LENGTH:
            skipped += 1
            continue
        
        items_to_summarize.append((idx, item["description"]))
    
    # Process in batches
    for i in range(0, len(items_to_summarize), BATCH_SIZE):
        batch = items_to_summarize[i:i + BATCH_SIZE]
        batch_indices = [idx for idx, _ in batch]
        
        print(f"  Processing batch {i // BATCH_SIZE + 1}/{(len(items_to_summarize) + BATCH_SIZE - 1) // BATCH_SIZE} ({len(batch)} items)...", flush=True)
        
        summaries = summarize_descriptions_batch(batch)
        
        # Update data with summaries
        for idx in batch_indices:
            if idx in summaries:
                summary = summaries[idx]
                original_len = len(data[idx]["description"])
                new_len = len(summary)
                data[idx]["description"] = summary
                summarized += 1
                print(f"    ✓ Job {idx + 1}: {original_len} → {new_len} chars")
            else:
                print(f"    ✗ Job {idx + 1}: Failed to summarize", file=sys.stderr)
        
        # Stop after first batch if in test mode
        if test_mode:
            print(f"\n  ⚠ Test mode: Stopping after first batch")
            break
    
    # Save back to file
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\n  ✓ Saved to {file_path}")
    except IOError as e:
        print(f"  ✗ Error saving file: {e}", file=sys.stderr)
        return summarized, skipped, total
    
    return summarized, skipped, total


def main():
    """Main function to process all description files"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Summarize job descriptions using Perplexity API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 summarize_descriptions.py              # Process all files completely
  python3 summarize_descriptions.py --test       # Process only first batch (for testing)
  python3 summarize_descriptions.py -t           # Same as --test
        """
    )
    parser.add_argument(
        '-t', '--test',
        action='store_true',
        help='Test mode: process only the first batch of descriptions'
    )
    args = parser.parse_args()
    
    # Validate API key
    validate_api_key()
    
    if args.test:
        print("⚠ Running in TEST MODE - will process only first batch\n")
    
    total_summarized = 0
    total_skipped = 0
    total_items = 0
    
    for file_path in DESCRIPTION_FILES:
        summarized, skipped, total = process_file(file_path, test_mode=args.test)
        total_summarized += summarized
        total_skipped += skipped
        total_items += total
    
    print(f"\n✓ Summarization complete!")
    print(f"  Total items processed: {total_items}")
    print(f"  Summarized: {total_summarized}")
    print(f"  Skipped (already short): {total_skipped}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSummarization interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
