import os
import time
# from GangaCore.GPIDev.Lib.File import LocalFile, SharedDir
# from GangaCore.GPIDev.Adapters.IRuntimeHandler import IRuntimeHandler
# from GangaCore import GangaException
# from GangaCore import Job, Executable, Local, ArgSplitter, CustomMerger



def wait_until_completed(job, timeout=600):
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
output_dir = prepare_directory('output_folder')


# Step 1: Split PDF into Pages
split_job = Job()
split_job.name = "Split_PDF_into_Pages"
split_job.application = Executable()
split_job.application.exe = "python3"
# split_job.inputsandbox = [LocalFile('LHC.pdf')]
split_job.inputfiles = [LocalFile('./LHC.pdf'), LocalFile('./read_pdf_and_split.py')]
print(split_job.inputfiles)
print(split_job.outputdir)
split_job.outputfiles = [LocalFile('./*.txt'), LocalFile('./*.pdf'), LocalFile('./*.pkl')]
split_job.application.args = ["read_pdf_and_split.py",'LHC.pdf', 'output_folder',1]
split_job.backend = Local()
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
# split_job.wait_until_completed()
# Loop until the job's status is 'completed' or 'failed'
# while split_job.status not in ['completed', 'failed']:
#     time.sleep(1)  # Wait for 5 seconds before checking again
#     split_job.updateStatus()  # Update the status from the Ganga backend

# if split_job.status == 'completed':
#     print("Split_Job completed successfully.")
# else:
#     print(f"split_Job did not complete successfully. Status is {split_job.status}.")

# Preprocessing before the next step - Reading the output files


# Step 2: Process Each Page with Subjobs
# Assuming 'output_folder' contains both PDFs and text files for each page
text_files = [f for f in os.listdir('output_folder') if f.endswith('.txt')]
count_job = Job()
count_job.splitter = ArgSplitter(args=[[os.path.join('output_folder', f), os.path.join('output_folder', f.replace('.txt', '_count.txt'))] for f in text_files])
count_job.application = Executable()
count_job.inputfiles = [LocalFile(f) for f in text_files] + [LocalFile('count_it.py')]
count_job.outputfiles = [LocalFile('output_folder/*')]
count_job.application.exe = File('python3')
count_job.application.args = ["count_it.py", '%split']
count_job.backend = Local()
count_job.submit()

# Wait for all subjobs to complete
if wait_until_completed(count_job):
    print("Split job completed successfully.")
else:
    print(f"Split job did not complete successfully. Status is {count_job.status}.")
    raise BaseException("Count job failed. Halting execution.")
# count_job.wait_until_completed()
# while count_job.status not in ['completed', 'failed']:
#     time.sleep(1)  # Wait for 5 seconds before checking again
#     count_job.updateStatus()  # Update the status from the Ganga backend

# if count_job.status == 'completed':
#     print("count_job completed successfully.")
# else:
#     print(f"count_job did not complete successfully. Status is {count_job.status}.")

# Step 3: Custom Merger
count_files = [os.path.join('output_folder', f.replace('.txt', '_count.txt')) for f in text_files]
merger_job = Job()
merger_job.application = Executable()
merger_job.application.exe = File('custom_merger.py')
# merger_job.inputsandbox = [LocalFile(f) for f in count_files] + [LocalFile('custom_merger.py')]
merger_job.inputfiles = [LocalFile(f) for f in count_files] + [LocalFile('custom_merger.py')]
merger_job.application.args = [count_files, 'output_folder/final_count.txt']
merger_job.backend = Local()
merger_job.submit()

# Wait for the merger job to complete
if wait_until_completed(merger_job):
    print("Split job completed successfully.")
else:
    print(f"Split job did not complete successfully. Status is {merger_job.status}.")
    raise BaseException("Merger job failed. Halting execution.")
# merger_job.wait_until_completed()
# while merger_job.status not in ['completed', 'failed']:
#     time.sleep(1)  # Wait for 5 seconds before checking again
#     merger_job.updateStatus()  # Update the status from the Ganga backend

# if merger_job.status == 'completed':
#     print("merger_job completed successfully.")
# else:
#     print(f"merger_job did not complete successfully. Status is {merger_job.status}.")

# Step 4: Read and Print the Output
with open('output_folder/final_count.txt', 'r') as f:
    print(f.read())
