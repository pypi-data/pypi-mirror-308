from __future__ import annotations
from typing import Union, Optional

import win32api, win32con, win32job


class Job:
    # Basic functions
    def __init__(self, name_or_handle: Union[str, "PyHANDLE"] = ""):
        """
        Create The Job Object Or Assign a Exist Job Handle
        When giving a string to the `name_or_handle` argument, the function will create a new job object with the given name
        Give an empty string to create a anyoumous job object(default).
        When giving a handle to the `name_or_handle` argument, the function will assign the handle with the job object.
        """
        if isinstance(name_or_handle, str):
            self._handle = win32job.CreateJobObject(None, name_or_handle)
        else:
            self._handle = name_or_handle
        
    @classmethod
    def from_exists(cls, name: str):
        """
        Assign the Job Object With a Exist Job by it's Name
        """
        return cls(win32job.OpenJobObject(win32job.JOB_OBJECT_ALL_ACCESS, False, name))
    
    def terminate(self, exitcode: int):
        """
        Terminate All Processes assigned to this job with given exit code.
        """
        win32job.TerminateJobObject(self._handle, exitcode)
        
    def assign(self, pid_or_handle: Optional[Union[int, "PyHANDLE"]]):
        """
        Assign the Job to a Existing Process.
        When giving a integer to the `pid_or_handle` argument, it'll be treated as the pid to the target process.
        When giving a handle to the `pid_or_handle` argument, the function will assign the job to the handle
        When giving `None`, the function will assign the job to current process. 
        """
        if pid_or_handle is None:
            pid_or_handle = win32api.GetCurrentProcessId()
        if isinstance(pid_or_handle, int):
            pid_or_handle = win32api.OpenProcess(win32con.PROCESS_SET_QUOTA | win32con.PROCESS_TERMINATE, False, pid_or_handle)
        win32job.AssignProcessToJobObject(self._handle, pid_or_handle)
    
    # Information Declears
    @property
    def basic_accounting_info(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectBasicAccountingInformation)
    @basic_accounting_info.setter
    def basic_accounting_info(self, val):
        win32job.SetInformationJobObject(self._handle, win32job.JobObjectBasicAccountingInformation, val)
    
    @property
    def basic_andlo_accounting_info(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectBasicAndIoAccountingInformation)
    @basic_andlo_accounting_info.setter
    def basic_andlo_accounting_info(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectBasicAndIoAccountingInformation, val)
        
    @property
    def basic_limit_info(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectBasicLimitInformation)
    @basic_limit_info.setter
    def basic_limit_info(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectBasicLimitInformation, val)
        
    @property
    def basic_process_id_list(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectBasicProcessIdList)
    @basic_process_id_list.setter
    def basic_process_id_list(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectBasicProcessIdList, val)
        
    @property
    def basic_ui_restrictions(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectBasicUIRestrictions)
    @basic_ui_restrictions.setter
    def basic_ui_restrictions(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectBasicUIRestrictions, val)
        
    @property
    def cpu_rate_control_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectCpuRateControlInformation)
    @cpu_rate_control_information.setter
    def cpu_rate_control_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectCpuRateControlInformation, val)
        
    @property
    def end_of_job_time_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectEndOfJobTimeInformation)
    @end_of_job_time_information.setter
    def end_of_job_time_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectEndOfJobTimeInformation, val)
        
    @property
    def end_of_job_time_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectEndOfJobTimeInformation)
    @end_of_job_time_information.setter
    def end_of_job_time_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectEndOfJobTimeInformation, val)
    
    @property
    def extended_limit_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectExtendedLimitInformation)
    @extended_limit_information.setter
    def extended_limit_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectExtendedLimitInformation, val)
        
    @property
    def group_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectGroupInformation)
    @group_information.setter
    def group_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectGroupInformation, val)
        
    @property
    def group_information_ex(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectGroupInformationEx)
    @group_information.setter
    def group_information_ex(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectGroupInformationEx, val)
        
    @property
    def limit_violation_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectLimitViolationInformation)
    @limit_violation_information.setter
    def limit_violation_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectLimitViolationInformation, val)
        
    @property
    def limit_violation_information2(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectLimitViolationInformation2)
    @limit_violation_information2.setter
    def limit_violation_information2(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectLimitViolationInformation2, val)
        
    @property
    def net_rate_control_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectNetRateControlInformation)
    @net_rate_control_information.setter
    def net_rate_control_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectNetRateControlInformation, val)
        
    @property
    def notification_limit_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectNotificationLimitInformation)
    @notification_limit_information.setter
    def notification_limit_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectNotificationLimitInformation, val)
        
    @property
    def notification_limit_information2(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectNotificationLimitInformation2)
    @notification_limit_information2.setter
    def notification_limit_information2(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectNotificationLimitInformation2, val)
        
    @property
    def security_limit_information(self):
        return win32job.QueryInformationJobObject(self._handle, win32job.JobObjectSecurityLimitInformation)
    @security_limit_information.setter
    def security_limit_information(self, val):
        return win32job.SetInformationJobObject(self._handle, win32job.JobObjectSecurityLimitInformation, val)
    
    # Basic Limits Wrapper & Extended Limits Wrapper
    @property
    def process_memory_limit(self):
        info = self.extended_limit_information
        if info['BasicLimitInformation']['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY:
            return info['ProcessMemoryLimit']
        return 0
    @process_memory_limit.setter
    def process_memory_limit(self, limit: int):
        info = self.extended_limit_information
        if limit == 0 and info['BasicLimitInformation']['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY:
            info['BasicLimitInformation']['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY
        else:
            info['BasicLimitInformation']['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY
            info['ProcessMemoryLimit'] = limit
        self.extended_limit_information = info
            
    @property
    def job_memory_limit(self):
        info = self.extended_limit_information
        if info['BasicLimitInformation']['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_JOB_MEMORY:
            return info['JobMemoryLimit']
        return 0
    @job_memory_limit.setter
    def job_memory_limit(self, limit: int):
        info = self.extended_limit_information
        if limit == 0 and info['BasicLimitInformation']['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_JOB_MEMORY:
            info['BasicLimitInformation']['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_JOB_MEMORY
        else:
            info['BasicLimitInformation']['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_JOB_MEMORY
            info['JobMemoryLimit'] = limit
        self.extended_limit_information = info
    
    @property
    def peak_process_memory_used(self):
        return self.extended_limit_information["PeakProcessMemoryUsed"]
        
    @property
    def peak_job_memory_used(self):
        return self.extended_limit_information["PeakJobMemoryUsed"]
    
    @property
    def per_process_user_time_limit(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_PROCESS_TIME:
            return info['PerProcessUserTimeLimit']
        return 0
    @per_process_user_time_limit.setter
    def per_process_user_time_limit(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_PROCESS_TIME:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_PROCESS_TIME
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_PROCESS_TIME
            info['PerProcessUserTimeLimit'] = limit
        self.basic_limit_information = info
            
    @property
    def per_job_user_time_limit(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_JOB_TIME:
            return info['PerJobUserTimeLimit']
        return 0
    @per_job_user_time_limit.setter
    def per_job_user_time_limit(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_JOB_TIME:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_JOB_TIME
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_JOB_TIME
            info['PerJobUserTimeLimit'] = limit
        self.basic_limit_information = info
            
    @property
    def minimum_working_set_size(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_WORKINGSET:
            return info['MinimumWorkingSetSize']
        return 0
    @minimum_working_set_size.setter
    def minimum_working_set_size(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_WORKINGSET:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_WORKINGSET
            info['MinimumWorkingSetSize'] = info['MaximumWorkingSetSize'] = 0
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_WORKINGSET
            info['MinimumWorkingSetSize'] = limit
            if not info['MaximumWorkingSetSize']:  # msdn says we can't set minimum to positive but maximum to zero
                info['MaximumWorkingSetSize'] = info['MinimumWorkingSetSize']
        self.basic_limit_information = info
        
    @property
    def maximum_working_set_size(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_WORKINGSET:
            return info['MaximumWorkingSetSize']
        return 0
    @maximum_working_set_size.setter
    def maximum_working_set_size(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_WORKINGSET:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_WORKINGSET
            info['MinimumWorkingSetSize'] = info['MaximumWorkingSetSize'] = 0
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_WORKINGSET
            info['MaximumWorkingSetSize'] = limit
            if not info['MinimumWorkingSetSize']:  # msdn says we can't set maximum to positive but minimum to zero
                info['MinimumWorkingSetSize'] = 1
        self.basic_limit_information = info
        
    @property
    def active_process_limit(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS:
            return info['ActiveProcessLimit']
        return 0
    @active_process_limit.setter
    def active_process_limit(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_ACTIVE_PROCESS
            info['ActiveProcessLimit'] = limit
        self.basic_limit_information = info
        
    @property
    def affinity(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_AFFINITY:
            return info['Affinity']
        return 0
    @affinity.setter
    def affinity(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_AFFINITY:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_AFFINITY
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_AFFINITY
            info['Affinity'] = limit
        self.basic_limit_information = info
        
    @property
    def priority_class(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_PRIORITY_CLASS:
            return info['PriorityClass']
        return 0
    @priority_class.setter
    def priority_class(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_PRIORITY_CLASS:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_PRIORITY_CLASS
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_PRIORITY_CLASS
            info['PriorityClass'] = limit
        self.basic_limit_information = info
    @property
    def scheduling_class(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_AFFINITY:
            return info['SchedulingClass']
        return 0
    @scheduling_class.setter
    def scheduling_class(self, limit: int):
        info = self.basic_limit_information
        if limit == 0 and info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_SCHEDULING_CLASS:
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_SCHEDULING_CLASS
        else:
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_SCHEDULING_CLASS
            info['SchedulingClass'] = limit
        self.basic_limit_information = info
        
    @property
    def breakaway(self):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK:
            return 'ok'
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK:
            return 'silent'
        return None
    @breakaway.setter
    def breakaway(self, val):
        info = self.basic_limit_information
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK and val != 'ok':
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK
        if info['LimitFlags'] & win32job.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK and val != 'silent':
            info['LimitFlags'] ^= win32job.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK
        if val == 'ok':
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_BREAKAWAY_OK
        if val == 'silent':
            info['LimitFlags'] |= win32job.JOB_OBJECT_LIMIT_SILENT_BREAKAWAY_OK
        self.basic_limit_information = info