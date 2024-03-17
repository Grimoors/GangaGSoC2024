import unittest
import os

# Assume the script is named count_it.py and is in the same directory as the test
# from count_it import count_it_in_file

class TestCountIt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample text file for testing
        cls.test_file_name = "test/test_countitpy_filedirectory/input/test_input.txt"
        with open(cls.test_file_name, 'w', encoding='utf-8') as file:
            file.write("It is important to note that IT could mean information technology.\n")
            file.write("This is another sentence with it in it.\n")

        # Expected count of "it" as a whole word, case-insensitive
        cls.expected_count = 4

    def test_count_it_in_file(self):
        # Test the function
        # count = count_it_in_file(self.test_file_name)

        # Test the script as standalone
        os.system(f'python3 GSoC/src/codefiles/countit/count_it.py {self.test_file_name} test/test_countitpy_filedirectory/output/test_output.txt')

        # Read the output file
        with open('test/test_countitpy_filedirectory/output/test_output.txt', 'r', encoding='utf-8') as file:
            count = int(file.read())
        

        self.assertEqual(count, self.expected_count, f"Expected count of 'it' is {self.expected_count}, got {count}")

    @classmethod
    def tearDownClass(cls):
        # Clean up: Remove the test file after testing
        os.remove(cls.test_file_name)

if __name__ == '__main__':
    unittest.main()
