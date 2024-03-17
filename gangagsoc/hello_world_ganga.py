# Import Ganga's job class
from GangaCore.GPI import Job, Executable, Local, queues

# Define a function to submit a job that prints "Hello World"
def submit_hello_world_job():
    j = Job()
    j.name = "Hello World (Exit Ganga on completion)"
    j.application = Executable()
    j.application.exe = "echo"
    j.application.args = ["Hello World, and Quitting Ganga After that."]
    j.backend = Local()
    return j

# Function to check job status
def wait_until_complete(job):
    import time
    while job.status not in ['completed', 'failed']:
        time.sleep(1)  # Sleep for a second before checking the status again
    return job.status

# Submit the job and wait for it to complete
job = submit_hello_world_job()
job.submit()

# Wait until the job is completed
job_status = wait_until_complete(job)
print(f"Job completed with status: {job_status}")

# Optionally print the output to the terminal if job is completed successfully
if job_status == 'completed':
    print(job.peek('stdout'))

# Exit Ganga
import sys
sys.exit()
