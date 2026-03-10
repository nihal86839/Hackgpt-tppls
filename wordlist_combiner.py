#!/usr/bin/env python3
"""
🔐 Wordlist Combiner Tool
=========================
Cybersecurity Tool - Combine Two Wordlists into One

Created by: Sa
Purpose: Combine two wordlist files for security testing
"""

import os
import sys

def get_file_size(filepath):
    """Get file size in human readable format"""
    size = os.path.getsize(filepath)
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"

def count_lines(filepath):
    """Count lines in a file"""
    count = 0
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in f:
            count += 1
    return count

def combine_wordlists(file1_path, file2_path, output_path, remove_duplicates=True):
    """Combine two wordlist files"""
    
    print("\n" + "="*60)
    print("🔐 WORDLIST COMBINER TOOL")
    print("="*60)
    
    # Check if files exist
    if not os.path.exists(file1_path):
        print(f"❌ Error: File not found - {file1_path}")
        return False
    
    if not os.path.exists(file2_path):
        print(f"❌ Error: File not found - {file2_path}")
        return False
    
    # Show file info
    print(f"\n📁 File 1: {os.path.basename(file1_path)}")
    print(f"   Size: {get_file_size(file1_path)}")
    
    print(f"\n📁 File 2: {os.path.basename(file2_path)}")
    print(f"   Size: {get_file_size(file2_path)}")
    
    # Read files
    print("\n⏳ Reading files...")
    
    all_lines = []
    
    # Read file 1
    print(f"   → Reading {os.path.basename(file1_path)}...")
    with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines1 = [line.strip() for line in f if line.strip()]
        all_lines.extend(lines1)
    print(f"   ✓ Found {len(lines1):,} lines")
    
    # Read file 2
    print(f"   → Reading {os.path.basename(file2_path)}...")
    with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines2 = [line.strip() for line in f if line.strip()]
        all_lines.extend(lines2)
    print(f"   ✓ Found {len(lines2):,} lines")
    
    original_count = len(all_lines)
    
    # Remove duplicates
    duplicates_removed = 0
    if remove_duplicates:
        print("\n🧹 Removing duplicates...")
        unique_lines = list(dict.fromkeys(all_lines))  # Preserves order
        duplicates_removed = original_count - len(unique_lines)
        all_lines = unique_lines
        print(f"   ✓ Removed {duplicates_removed:,} duplicate lines")
    
    # Write output
    print(f"\n💾 Writing combined file...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_lines))
    
    # Show result
    print("\n" + "="*60)
    print("✅ SUCCESS! Wordlist Combined!")
    print("="*60)
    print(f"\n📊 Statistics:")
    print(f"   • Total lines: {len(all_lines):,}")
    print(f"   • Duplicates removed: {duplicates_removed:,}")
    print(f"   • Output file: {output_path}")
    print(f"   • Output size: {get_file_size(output_path)}")
    print("\n🎉 Done! Your combined wordlist is ready!")
    
    return True

def main():
    print("\n🔐 WORDLIST COMBINER - Python Tool")
    print("-" * 40)
    
    # Get file paths from user
    print("\n📥 Enter file paths:\n")
    
    file1 = input("   Enter first wordlist path: ").strip().strip('"').strip("'")
    file2 = input("   Enter second wordlist path: ").strip().strip('"').strip("'")
    
    # Ask about duplicates
    print("\n   Remove duplicates? (Y/n): ", end="")
    remove_dup = input().strip().lower()
    remove_duplicates = remove_dup != 'n'
    
    # Get output path
    output = input("   Enter output file path (or press Enter for default): ").strip().strip('"').strip("'")
    if not output:
        output = "combined_wordlist.txt"
    
    # Combine
    combine_wordlists(file1, file2, output, remove_duplicates)

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) >= 3:
        # Command line mode
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) >= 4 else "combined_wordlist.txt"
        remove_duplicates = True
        
        if "--keep-duplicates" in sys.argv:
            remove_duplicates = False
        
        combine_wordlists(file1, file2, output, remove_duplicates)
    else:
        # Interactive mode
        main()
