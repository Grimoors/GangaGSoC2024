# from Ganga import Job, Executable, LocalFile, ArgSplitter
# from Ganga.GPI import tasks, CoreTask, CoreTransform, TaskChainInput, GangaDataset, GangaDatasetSplitter

import os 
import time


# Assuming the output directory preparation and task setup remain the same...

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


t = CoreTask()
t.name = "Count_It_Task"
t.float = 5  # Set the priority of the task

# First Transform: Split PDF into Pages
# Step 1: Split PDF into Pages
split_job = CoreTransform()
split_job.name = "Split_PDF_into_Pages"
split_job.application = Executable()
split_job.application.exe = "python3"
split_job.application.args = ["read_pdf_and_split.py",'LHC.pdf', 'output_folder',0]
split_job.backend = Local()

split_job.outputfiles = [LocalFile('./output_folder/*.txt'), LocalFile('./output_folder/*.pdf'), LocalFile('./output_folder/page_txt_paths.pkl')]

d0 = GangaDataset()
d0.files = [LocalFile('./LHC.pdf'), LocalFile('./read_pdf_and_split.py')]
d0.treat_as_inputfiles = True
split_job.addInputData(d0)

print(split_job.inputfiles)

t.appendTransform(split_job)



# # Transform 2: Count occurrences in each page
# trf2 = CoreTransform()
# trf2.name = "Count Occurrences"
# trf2.application = Executable()
# trf2.application.exe = "python3"
# # Ensure 'count_it.py' script is available
# trf2.inputfiles = [TaskChainInput(transform_id=split_job.getID()), LocalFile('count_it.py')]
# trf2.inputfiles = [LocalFile('count_it.py')]  # count_it.py needs to be in the job's running directory
# # Here we need to specify that we are using an ArgSplitter
# trf2.splitter = ArgSplitter()
# trf2.inputfiles = [LocalFile(f) for f in text_files] + [LocalFile('count_it.py')]
# # Since the exact arguments will depend on the output of the first transform, you'll need to customize this part.
# # For example, if you know the naming pattern of the output files, you can programmatically generate the args list:
# # This is a placeholder showing conceptually how you might set it up. The actual implementation would need to dynamically generate these args based on the output files from Transform 1.
# trf2.splitter.args = [["output_folder/page_1.txt", "output_folder/page_1_count.txt"], ["output_folder/page_2.txt", "output_folder/page_2_count.txt"]]  # Example
# trf2.splitter.args = [[f, f.replace('.txt', '_count.txt')] for f in text_files]
# trf2.backend = Local()
# t.appendTransform(trf2)

# Third Transform: Custom Merger
# Assuming this transform setup remains the same...

# Start the Task
t.run()
