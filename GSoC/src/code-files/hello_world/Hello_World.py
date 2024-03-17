# Import Ganga's job class
# from ganga.GangaCore.GPI import Job, Local
from GangaCore.GPI import Job, Local, Executable


# Create a new job with Local backend
j = Job(backend=Local())
j.application = Executable()
j.application.exe = 'echo'
j.application.args = ['Hello World']

# Submit the job
j.submit()

# Check job status
print(j.status)

# Once completed, check the stdout
print(j.peek('stdout'))
