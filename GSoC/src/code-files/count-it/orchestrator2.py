import os
import time
import shutil
# from GangaCore.GPIDev.Lib.File import LocalFile, SharedDir
# from GangaCore.GPIDev.Adapters.IRuntimeHandler import IRuntimeHandler
# from GangaCore import GangaException
# from GangaCore import Job, Executable, Local, ArgSplitter, CustomMerger

def list_txt_files_in_output_dir(job,extension='.txt'):
    """
    Lists all .txt files in the output directory of a given job.

    :param job: The Ganga job object whose output directory to search.
    :return: A list of paths to .txt files in the job's output directory.
    """
    output_dir = job.outputdir
    txt_files = [f for f in os.listdir(output_dir) if f.endswith(extension)]
    return txt_files

def retrieve_txt_files(job, destination_directory=None, extension='.txt'):
    """
    Demonstrates processing of .txt files in a job's output directory.
    Replace the print statement with actual file retrieval or processing logic as needed.

    :param job: The Ganga job object whose .txt output files to process.
    """
    txt_files = list_txt_files_in_output_dir(job,extension)

    if destination_directory is None:
        destination_directory = os.path.join(os.getcwd(), 'retrieved_txt_files')
    os.makedirs(destination_directory, exist_ok=True)

    for file_name in txt_files:
        file_path = os.path.join(job.outputdir, file_name)
        print(f"Found {extension} file: {file_path}")
        # For example, to copy the file to another directory:
        shutil.copy(file_path, destination_directory)

def retrieve_files_from_subjobs(job, destination_directory=None, extension='.txt'):
    """
    Recursively searches and retrieves files with a specific extension from a job and all its subjobs.

    :param job: The Ganga job object.
    :param destination_directory: The directory where files will be copied. If None, uses './retrieved_files'.
    :param extension: The file extension to search for (e.g., '.txt').
    """
    # Default destination directory
    if destination_directory is None:
        destination_directory = os.path.join(os.getcwd(), 'retrieved_files')
    os.makedirs(destination_directory, exist_ok=True)

    # Function to process each directory
    def process_directory(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(destination_directory, os.path.basename(file))
                    shutil.copy(source_path, destination_path)
                    print(f"Copied: {source_path} -> {destination_path}")

    # Process the main job's output directory
    process_directory(job.outputdir)

    # If the job has subjobs, process their output directories too
    if hasattr(job, 'subjobs'):
        for subjob in job.subjobs:
            process_directory(subjob.outputdir)


def wait_until_completed(job, timeout=6000):
    """
    Waits for the job to complete or fail, checking every few seconds.

    :param job: The Ganga job to wait for.
    :param timeout: Maximum time to wait in seconds before returning False.
    :return: True if the job completed, False if failed or timeout.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if job.status in ['completed', 'failed']:
            return job.status == 'completed'
        time.sleep(1)  # Check every second
    return False

# Helper function to ensure directory exists and is empty
def prepare_directory(path):
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
    else:
        os.makedirs(path)
    return path

# Prepare the output directory for the split job
# output_dir = prepare_directory('output_folder')


# Step 1: Split PDF into Pages
split_job = Job()
split_job.name = "Split_PDF_into_Pages"
split_job.application = Executable()
split_job.application.exe = "python3"
split_job.inputdata = GangaDataset(files=[LocalFile('./LHC.pdf'), LocalFile('./read_pdf_and_split.py')])
split_job.application.args = ["read_pdf_and_split.py",'LHC.pdf', './',1]

split_job.backend = Local()

print(split_job.inputfiles)
print(split_job.outputdir)
# split_job.outputfiles = [LocalFile('./*.txt'), LocalFile('./*.pdf'), LocalFile('./*.pkl')]
split_job.outputfiles = [LocalFile('./*')]
split_job.inputfiles = [LocalFile('./LHC.pdf'), LocalFile('./read_pdf_and_split.py')]
split_job.submit()



# Wait for the job to complete
if wait_until_completed(split_job):
    print("Split job completed successfully.")
    split_job.peek()
    # split_job.outputfiles.get()
else:
    split_job.peek()
    print(f"Split job did not complete successfully. Status is {split_job.status}.")
    raise BaseException("Split job failed. Halting execution.")


# Retrieve .txt files from the completed job
retrieve_txt_files(split_job, destination_directory='./split_pdf_texts/', extension='.txt')

# Zip the output directory for easy download
shutil.make_archive('split_pdf_texts', 'zip', './split_pdf_texts')


def prepare_custom_merger_script():
    """
    Prepares the custom merger script with correct Python syntax.
    """
    merger_code = """

import sys

def merge(file_list_txt, output_file):
    #read the content of the file
    file_list = []
    print(type(file_list_txt[0]))
    print(file_list_txt[0])
    with open(file_list_txt[0], 'r') as f_in:
        # read the file paths from the file
        file_paths = f_in.read().strip().split('\\n')
        # append the file path to the list
        file_list.extend(file_paths)

    # import pickle
    # file_list = pickle.load(open(file_list_pickle, 'rb'))
    total_count = 0
    for file_path in file_list:
        with open(file_path, 'r') as f_in:
            count = int(f_in.read().strip())
            total_count += count
    with open(output_file, 'w') as f_out:
        f_out.write(str(total_count))

if __name__ == "__main__":
    file_list    = sys.argv[1:-1]
    print(type(file_list))
    output_file = sys.argv[-1]
    merge(file_list, output_file)


"""
    script_path = './custom_merger.py'
    with open(script_path, 'w') as script_file:
        script_file.write(merger_code)
    return script_path

# Generate the custom merger script
merger_script_path = prepare_custom_merger_script()

# Assuming 'output_folder' contains both PDFs and text files for each page
output_folder = './split_pdf_texts/'  # Ensure this is the directory where split_job's output files are saved
text_files = [f for f in os.listdir(output_folder) if f.endswith('.txt')]
count_job = Job()
count_job.application = Executable()
count_job.application.exe = 'python3'
count_job.application.args = ['count_it.py', '%split']
# extract the input files from the split job fro the zipfile
shutil.unpack_archive('split_pdf_texts.zip', './', 'zip')
count_job.splitter = ArgSplitter(args=[[ "count_it.py" , os.path.join("./", f), os.path.join("./", f.replace('.txt', '_count.txt'))] for f in text_files])
count_job.inputfiles = [LocalFile('count_it.py')] + [LocalFile(os.path.join("./", f)) for f in text_files] + [LocalFile('./*.zip')] + [LocalFile('./*.pkl')]
count_job.outputfiles = ["./*"]
count_job.backend = Local()
count_job.submit()

# Wait for the job to complete
if wait_until_completed(count_job):
    print("Count job completed successfully.")
    count_job.peek()
    # split_job.outputfiles.get()
else:
    count_job.peek()
    print(f"Count job did not complete successfully. Status is {split_job.status}.")
    raise BaseException("Count job failed. Halting execution.")

# Retrieve _count.txt files from the completed job
retrieve_files_from_subjobs(count_job, destination_directory='./counts_parallel/',extension="_count.txt")

# Zip the output directory for easy download
shutil.make_archive('counts_parallel', 'zip', './counts_parallel')

# extract the input files from the split job fro the zipfile
shutil.unpack_archive('counts_parallel.zip', './', 'zip')

counts_file_list = [os.path.join('./', f) for f in os.listdir('./counts_parallel') if f.endswith('_count.txt')]
#pickle file list to a pkl file
import pickle
with open('counts_file_list.pkl', 'wb') as f:
    pickle.dump(counts_file_list, f)

#Save List as a text file
with open('counts_file_list.txt', 'w') as f:
    for item in counts_file_list:
        print(item)
        f.write("%s\n" % item)


# Custom Merger Job
merger_job = Job()
merger_job.application = Executable()
merger_job.application.exe = 'python3'
merger_job.application.args = [ merger_script_path , "counts_file_list.txt" , 'total_word_count.txt' ]
merger_job.inputfiles = [LocalFile(merger_script_path)] + [LocalFile(f) for f in counts_file_list] + [LocalFile('counts_file_list.pkl') ] + [ LocalFile('counts_file_list.txt') ]
merger_job.outputfiles = [LocalFile('./*')]
merger_job.backend = Local()
merger_job.submit()

# Wait for the job to complete
# Wait for the job to complete
if wait_until_completed(merger_job):
    print("Merger job completed successfully.")
    merger_job.peek()
    # split_job.outputfiles.get()
else:
    merger_job.peek()
    print(f"erger job did not complete successfully. Status is {split_job.status}.")
    raise BaseException("Merger job failed. Halting execution.")

#cleanup the text, pickle and zip files in the current directory
os.remove('counts_file_list.txt')
os.remove('counts_file_list.pkl')
os.remove('counts_parallel.zip')
os.remove('split_pdf_texts.zip')
for f in os.listdir('./split_pdf_texts'):
    os.remove(os.path.join('./', f))

for f in os.listdir('./counts_parallel'):
    os.remove(os.path.join('./', f))



#copy the output file to the current directory
shutil.copy(os.path.join(merger_job.outputdir, 'total_word_count.txt'), './total_word_count.txt')

# quit ganga
quit()

# # # Step 2: Count Words in Each Page

# # # List of Input Files
# text_files = [f for f in os.listdir('./split_pdf_texts') if f.endswith('.txt')]

# # # Define the job
# count_job = Job()
# count_job.splitter = ArgSplitter(args=[[os.path.join('./split_pdf_texts', f), os.path.join('./split_pdf_texts', f.replace('.txt', '_count.txt'))] for f in text_files])
# count_job.application = Executable()
# count_job.inputfiles = [LocalFile(f) for f in text_files] + [LocalFile('count_it.py')]
# count_job.outputfiles = [LocalFile('./*')]
# count_job.application.exe = 'python3'
# count_job.application.args = ["count_it.py", '%split']
# count_job.backend = Local()
# # count_job.postprocessors = [retrieve_txt_files]
# count_job.submit()


# # Wait for all subjobs to complete
# if wait_until_completed(count_job):
#     print("Count completed successfully.")
#     count_job.peek()
# else:
#     print(f"Count did not complete successfully. Status is {count_job.status}.")
#     count_job.peek()
#     raise BaseException("Count job failed. Halting execution.")
    