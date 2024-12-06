# LibJob
LibJob is the python wrapper of windows's `job` feature, which could replace `resource` easily.

Using Example & Compares(when applying 100MB memory limit to given two processes):
by `resource` standard library:
```python
curlimit = resource.prlimit(pid1, resource.RLIMIT_VMEM)
resource.prlimit(pid1, resource.RLIMIT_MEMLOCK, (100 * 1024 * 1024, curlimit[1]))
curlimit = resource.prlimit(pid2, resource.RLIMIT_VMEM)
resource.prlimit(pid2, resource.RLIMIT_MEMLOCK, (100 * 1024 * 1024, curlimit[1]))
```
by using `pywin32`
```python
job = win32job.CreateJobObject(None, "")
extended_info = win32job.QueryInformationJobObject(job, win32job.JobObjectExtendedLimitInformation)
extended_info["ProcessMemoryLimit"] = 100 * 1024 * 1024
extended_info["BasicLimitInformation"]["LimitFlags"] |= win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY
win32job.SetInformationJobObject(job, win32job.JobObjectExtendedLimitInformation, extended_info)
proc = win32api.OpenProcess(win32con.PROCESS_SET_QUOTA | win32con.PROCESS_TERMINATE, False, pid1)
win32job.AssignProcessToJobObject(job, proc)
proc = win32api.OpenProcess(win32con.PROCESS_SET_QUOTA | win32con.PROCESS_TERMINATE, False, pid2)
win32job.AssignProcessToJobObject(job, proc)
```
by using `libjob`
```python
job = libjob.Job()
job.process_memory_limit = 100 * 1024 * 1024
job.assign(pid1)
job.assign(pid2)
```
