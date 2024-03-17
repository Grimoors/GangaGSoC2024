import unittest
import os
import tempfile

class TestMerge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create temporary directory
        cls.temp_dir = tempfile.TemporaryDirectory()
        # Create sample count files
        cls.file_paths = []
        cls.expected_total = 0
        for i in range(3):
            count = i + 1  # Sample count for the file
            cls.expected_total += count
            file_path = os.path.join(cls.temp_dir.name, f'count_{i}.txt')
            cls.file_paths.append(file_path)
            with open(file_path, 'w') as f:
                f.write(str(count))
        # Create a file listing all count files
        cls.list_file_path = os.path.join(cls.temp_dir.name, 'file_list.txt')
        with open(cls.list_file_path, 'w') as f:
            f.write('\n'.join(cls.file_paths))

    def test_merge(self):
        # Output file for the merge function
        output_file = os.path.join(self.temp_dir.name, 'total_count.txt')
        # Call the merge function
        os.system(f'python GSoC/src/codefiles/countit/custom_merger.py {self.list_file_path} {output_file}')
        # Read the output file
        with open(output_file, 'r') as f:
            total_count = int(f.read().strip())
        # Check if the total count is as expected
        self.assertEqual(total_count, self.expected_total, f"Expected total count of {self.expected_total}, got {total_count}")

    @classmethod
    def tearDownClass(cls):
        # Clean up
        cls.temp_dir.cleanup()

if __name__ == '__main__':
    unittest.main()
