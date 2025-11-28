import argparse
import sys

def remove_non_chinese(text: str) -> str:
    """
    Removes Korean (Hangul), Japanese (Hiragana/Katakana), and characters in other languages
    from a string by checking if each character's Unicode code point falls 
    within a defined set of exclusion ranges.
    
    NOTE: This method excludes the CJK Unified Ideographs range to preserve 
    Chinese Hanzi characters, mirroring the logic in text_cleaner.py.

    Args:
        text: The input string containing mixed characters.

    Returns:
        The string with the specified characters removed.
    """
    
    # Define the Unicode code point ranges (start, end) for the characters to remove.
    # We use hexadecimal notation (0x...) for clarity.
    removal_ranges = [
        # 🇸🇦 Arabic Script
        (0x0600, 0x06FF),
        
        # 🇸🇦 Arabic Presentation Forms-A (Includes Basmala U+FDFD)
        (0xFB50, 0xFDFF),
        
        # 🇮🇳 Gurmukhi/Punjabi Script (NEW)
        (0x0A00, 0x0A7F),
        
        # 🇮🇳 Malayalam Script (NEW)
        (0x0D00, 0x0D7F),
        
        # 🇹🇭 Thai Script
        (0x0E00, 0x0E7F),
        
        # 🇲🇲 Burmese/Myanmar Script
        (0x1000, 0x109F),

        # 🇰🇷 Korean (Hangul Jamo - decomposed)
        (0x1100, 0x11FF),

        # 🇯🇵 Japanese (Hiragana ONLY)
        (0x3040, 0x309F),  
        
        # 🇯🇵 Japanese (Katakana ONLY)
        (0x30A0, 0x30FF),  

        # 🇰🇷 Korean (Hangul Compatibility Jamo)
        (0x3130, 0x318F),

        # 🇰🇷 Korean (Hangul Syllables - composed like "평가")
        (0xAC00, 0xD7A3),

        # 🇷🇺 Cyrillic Script
        (0x0400, 0x04FF),
        
        # 🇰🇭 Khmer Script (Cambodian)
        (0x1780, 0x17FF),
        
        # 🇮🇳 Telugu Script
        (0x0C00, 0x0C7F),
        
        # 🇬🇪 Georgian Script
        (0x10A0, 0x10FF),
        
        # 🇲🇳 Mongolian/Manchu Script
        (0x1800, 0x18AF),
        
        # 🇮🇳 Gurmukhi/Punjabi Script
        (0x0A00, 0x0A7F),
        
        # 🇮🇳 Malayalam Script
        (0x0D00, 0x0D7F),
    ]
    
    def is_in_removal_range(char: str) -> bool:
        """Helper function to check if a single character is in any exclusion range."""
        char_code = ord(char)
        for start, end in removal_ranges:
            if start <= char_code <= end:
                return True
        return False

    # Use a generator expression within "".join() to efficiently build the new string.
    # It keeps only characters for which is_in_removal_range returns False.
    cleaned_text = "".join(
        char for char in text if not is_in_removal_range(char)
    )
    
    return cleaned_text


if __name__ == "__main__":
    # 1. Setup argument parser
    parser = argparse.ArgumentParser(
        description="A script to remove Korean, Japanese, Arabic, and Thai characters from a string using iterative Unicode checks (no regex). (Excludes CJK Ideographs to preserve Chinese Hanzi)"
    )
    
    # 2. Define the required argument for the input file
    parser.add_argument(
        '-i', 
        '--in',
        dest='input_file',
        type=str,
        required=True, # The input file is now mandatory
        help="The required filepath to read the input text from."
    )
    
    # 3. Add the optional output file argument
    parser.add_argument(
        '-o', 
        '--out',
        type=str,
        dest='output_file',
        help="Optional: Specify a filepath to write the cleaned output to. If not provided, output is printed to the console.",
        default=None
    )
    
    # 4. Parse the arguments
    args = parser.parse_args()
    
    try:
        # 5. Process the input text: Read from the file specified by --in
        input_filepath = args.input_file
        # Use 'utf-8' encoding for correct handling of various international characters
        with open(input_filepath, 'r', encoding='utf-8') as f:
            input_string = f.read()
            
        cleaned_string = remove_non_chinese(input_string)
        
        # 6. Output the results
        
        if args.output_file:
            # Write to file
            output_filepath = args.output_file
            # Use 'utf-8' encoding for correct handling of remaining non-ASCII characters
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_string.strip())
            
            print("\n--- Text Cleaning Results (Non-Regex) ---")
            print(f"Input read from: {input_filepath}")
            print(f"Output saved to: {output_filepath}")
            print("-----------------------------------------\n")
        else:
            # Print to console (default behavior)
            print("\n--- Text Cleaning Results (Non-Regex) ---")
            print(f"Input read from: {input_filepath}")
            print(f"Cleaned Text:  {cleaned_string.strip()}") # .strip() removes potential leading/trailing whitespace left by removed chars
            print("-----------------------------------------\n")
        
    except FileNotFoundError:
        print(f"Error: Input file not found at path '{input_filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during processing: {e}", file=sys.stderr)
        sys.exit(1)