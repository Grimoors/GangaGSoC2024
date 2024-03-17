import unittest
import os
import shutil
import pickle

# Ensure the required packages are installed
if not shutil.which('pdfinfo'):
    os.system('pip install pdfinfo')
if not shutil.which('PyPDF2'):
    os.system('pip install PyPDF2')
if not shutil.which('pdfminer.six'):
    os.system('pip install pdfminer.six')

from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text



class TestSplitPdfPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup variables
        cls.pdf_path = 'test/test_read_and_split_pdfpy_filedirectory/input/test.pdf'  # Path to the test PDF
        cls.output_folder = 'test/test_read_and_split_pdfpy_filedirectory/output'
        cls.debug_mode = False
        
        # Ensure the output directory is clean
        if os.path.exists(cls.output_folder):
            shutil.rmtree(cls.output_folder)
        os.makedirs(cls.output_folder, exist_ok=True)

        # Read the test PDF to count pages
        cls.expected_pages = len(PdfReader(cls.pdf_path).pages)

    def test_split_pdf_pages(self):
        # Run the module as standalone
        os.system(f'python3 GSoC/src/codefiles/countit/read_pdf_and_splIt.py {self.pdf_path} {self.output_folder} {int(self.debug_mode)}')
        

        # Check the number of files generated (PDF + TXT for each page)
        generated_files = os.listdir(self.output_folder)
        self.assertEqual(len(generated_files), self.expected_pages * 2 + 1, "The number of generated files should be twice the number of pages (PDF and TXT each).")

        # Check if pickle file with text file paths is created
        self.assertIn('page_txt_paths.pkl', generated_files, "Pickle file with output paths is missing.")

        # Verify contents of the pickle file
        with open(os.path.join(self.output_folder, 'page_txt_paths.pkl'), 'rb') as f:
            output_paths = pickle.load(f)
        self.assertEqual(len(output_paths), self.expected_pages, "Pickle file should contain paths equal to the number of pages.")

    @classmethod
    def tearDownClass(cls):
        # Clean up by removing the output folder after tests
        shutil.rmtree(cls.output_folder)

if __name__ == '__main__':
    unittest.main()
