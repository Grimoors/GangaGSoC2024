import sys
import re
import os
def count_it_in_file(input_file):
    # Read the content of the file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    # Count occurrences of "it", ignoring case and as whole words only
    count = len(re.findall(r'\bit\b', content, re.IGNORECASE))
    # Return the count
    return count
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python count_it.py <input_text_file> <output_count_file>")
        sys.exit(1)
    input_text_file = sys.argv[1]
    output_count_file = sys.argv[2]
    # Get the count of "it"
    count = count_it_in_file(input_text_file)
    # Save the count to the specified output file
    print(count) 
    with open(output_count_file, 'w', encoding='utf-8') as file:
        file.write(str(count))
    print(count) 
