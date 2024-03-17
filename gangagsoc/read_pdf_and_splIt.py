import sys
import os
import pickle
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
def debug_print(message, debug_mode):
    if debug_mode:
        print(message)
def split_pdf_pages(pdf_path, output_folder, debug_mode=False):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    debug_print(f"Output directory {output_folder} created.", debug_mode)
    
    # Initialize a list to hold output paths
    output_paths = []

    # Read the PDF
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    debug_print(f"Total pages in PDF: {total_pages}", debug_mode)

    # Loop through each page in the PDF
    for i in range(total_pages):
        page = reader.pages[i]
        
        # Write the individual PDF page
        writer = PdfWriter()
        writer.add_page(page)
        output_pdf_path = os.path.join(output_folder, f'page_{i+1}.pdf')
        with open(output_pdf_path, 'wb') as outfile:
            writer.write(outfile)
        debug_print(f"Saved PDF page {i+1} to {output_pdf_path}", debug_mode)
        
        # Extract text from the PDF page and save it to a .txt file
        page_text = extract_text(output_pdf_path)
        output_txt_path = os.path.join(output_folder, f'page_{i+1}.txt')
        with open(output_txt_path, 'w', encoding='utf-8') as textfile:
            textfile.write(page_text)
        debug_print(f"Extracted text from page {i+1} and saved to {output_txt_path}", debug_mode)

        # Add the paths to the list
        # output_paths.append(output_pdf_path)
        output_paths.append(output_txt_path)
    # Save the list of paths to a pickle file
    pickle_path = os.path.join(output_folder, 'page_txt_paths.pkl')
    with open(pickle_path, 'wb') as f:
        pickle.dump(output_paths, f)
    debug_print(f"Saved output paths to {pickle_path}", debug_mode)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_pages.py <path_to_pdf> <output_folder> [debug_mode]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_folder = sys.argv[2]
    debug_mode = len(sys.argv) > 3 and sys.argv[3] != '0'
    split_pdf_pages(pdf_path, output_folder, debug_mode)
