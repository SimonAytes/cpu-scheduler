# cpu_scheduler_tools.py
# File containing the classes and functions for the CPU Scheduler project

#### SPECIFICATIONS ####
#First-come, first-served (FCFS), which schedules tasks in the 
# order in which they request the CPU.
# 
# Round-robin (RR) scheduling, where each task is run for a time quantum 
# (or for the remainder of its CPU burst). 

class Process:
    """Process object. Contains initialization method and stores variables."""
    # Process attributes
    pid = "" # Process UUID
    arrival_time = -1 # Time when the process arrives in the unit of milliseconds 
    cpu_burst = -1 # CPU time requested by a time, in the unit of milliseconds
    wait_time = -1 # Wait time of the process
    turnaround_time = -1 # Wait time + execution time
    response_time = -1 # Same as wait time

    ## Special for Red-Robin (RR)
    state_code = 0 # Denotes the state of the process --> 0 = Incomplete, 1 = Complete
    end_time = -1 # Time the process was executed

    def __init__(self, input_id, input_arrivalTime, input_cpuBurst):
        self.pid = input_id
        self.arrival_time = input_arrivalTime
        self.cpu_burst = input_cpuBurst
        self.burst_copy = input_cpuBurst

class InputForm:
    """Input Form class. Handles all user inputs."""
    # Form Attribues
    file_path = "" # File path to the input file
    scheduler_type_code = -1 # Scheduler type code --> 0 = FCFS, 1 = RR, -1 = DEFAULT
    time_slide_val = -1 # Time slide value for the CPU Scheduler

    def __init__(self):
        # Load in the input file
        self.file_path = input("Enter file path: ")
        self.__load_config__()

        # Choose the Scheduler Type
        input_scheduler_type = input("Please choose scheduler type (fcfs or rr): ")
        self.scheduler_type_code = self.__get_scheduler_code__(input_scheduler_type)

        # Specify the time slide value (Round-robin ONLY)
        if self.scheduler_type_code == 1:
            input_time_slide_val = input("Please specify a time slide value: ")
            self.time_slide_val = int(input_time_slide_val)

    def __get_scheduler_code__(self, type_input):
        """Parses the user-input scheduler type choice. If type cannot be parsed, choose FCFS"""
        if type_input.lower() == "rr":
            return 1 # Choose RR
        else:
            return 0 # Choose FCFS
        
    def __load_config__(self):
        """Loads the input file from a specified path"""
        # Define list of lines
        input_lines = []

        # Open the text file and grab each line
        with open(self.file_path) as topo_file:
            for line in topo_file:
                input_lines.append(line)
        
        # Parse the input lines and create Process objects
        return self.__parse_inputs__(input_lines)

    def __parse_inputs__(self, lines):
        """Returns a list of Process objects"""
        # Create empty list of processes
        process_list = []

        # Iterate over all lines in the file and create Process objects for each
        for line in lines:
            # Skip a line if it is blank
            if line == "":
                pass
    
            # Parse the contents (split by comma)
            contents = line.split(",")

            # Create Process object
            temp = Process(
                input_id = contents[0],
                input_arrivalTime = int(contents[1]),
                input_cpuBurst = int(contents[2])
            )

            # Append Process object to class list
            process_list.append(temp)

        # Return list of processes
        return process_list

    def GetProcesses(self):
        """"Parses input file and returns list of Process objects"""
        # Load processes from file
        processes = self.__load_config__()

        # Return list of processes
        return processes

class CPU_Scheduler:
    """CPU Scheduler class. Drives all functions of the scheduler simulation"""
    # CPU Scheduler Attributes
    form = None # Form that holds all user-input information
    process_list = [] # List of process objects
    avg_wait_times = 0.0 # Average wait times of all processes
    avg_response_times = 0.0 # Average response time of all processes
    avg_turnaround_times = 0.0 # Average turnaround time of all processes
    execution_log = []
    
    def __init__(self):
        # Get user inputs
        self.form = InputForm()
        # Load processes from input file
        self.process_list = self.form.GetProcesses()
        # DEBUG -- print Process attributes
        #self.list_processes()

    def list_processes(self):
        for p in self.process_list:
            print(p.pid)
            print(p.arrival_time)
            print(p.cpu_burst)

    def FCFS(self):
        """"First-Come First-Serve driver code."""
        # Print field title
        print("\n-------------------------------------------------\n\tFirst Come First Served Scheduling\n-------------------------------------------------")

        # Calculate the specified times for the processes
        self.__FCFS_TurnaroundTimes()
        self.__FCFS_WaitTimes()
        self.__ResponseTimes()

        # Print Gantt Chart
        self.__FCFS_GanttChart()

        # Print times
        self.__print_times()

    def RR(self):
        """Round-Robin driver code."""
        # Print field title
        print("\n-------------------------------------------------\n\tRound Robin Scheduling\n-------------------------------------------------")

        # Run the RR scheduler -- execute all processes
        self.__RR_Schedule()
        
        # Calculate the specified times for the processes
        self.__ResponseTimes()
        self.__RR_TurnaroundTime()
        self.__RR_WaitingTime()

        # Print Gantt Chart
        self.__RR_GanttChart()

        # Print times
        self.__print_times()

    def __FCFS_GanttChart(self):
        """FCFS: Create a gantt chart of the CPU scheduler"""
        completed_burst_times = []
        gantt_chart_string = ""
        
        for p in self.process_list:
            # Add process to the list
            lb = -1
            if len(completed_burst_times) == 0:
                lb = 0
            else:
                lb = str(sum(completed_burst_times))
            completed_burst_times.append(p.cpu_burst)
            ub = str(sum(completed_burst_times))
            id = p.pid

            # Add current process to string
            gantt_chart_string += f"[{lb}-{ub}]\t{id} running\n"
        
        # Print the gantt chart
        print(gantt_chart_string)

    def __FCFS_WaitTimes(self):
        """"FCFS: Calculate the wait times for all processes."""
        # Define variables to hold wait times for FCFS
        wait_times = []

        for i in range(0, len(self.process_list)):
            if i == 0:
                # Update wait times
                wait_times.append(0)
                self.process_list[0].wait_time = 0
            else:
                # Access current and previous processes
                prev_process = self.process_list[i-1]
                curr_process = self.process_list[i]

                # Calculate wait times
                curr_wait_time = (prev_process.arrival_time + prev_process.cpu_burst + wait_times[i-1]) - curr_process.arrival_time
                
                # Update wait times
                wait_times.append(curr_wait_time)
                self.process_list[i].wait_time = curr_wait_time
                
        # Calculate average wait time
        self.avg_wait_times = sum(wait_times) / len(wait_times)

    def __ResponseTimes(self):
        """"Calculate the response times for each process."""
        # Define variables to hold response times for FCFS
        response_times = []

        for i in range(0, len(self.process_list)):
            if i == 0:
                # Update response times
                response_times.append(0)
                self.process_list[0].response_time = 0
            else:
                # Access current and previous processes
                curr_process = self.process_list[i]
                
                # Get the burst times of all previous processes
                t = 0
                burst_times = []
                while t < i:
                    prev_process = self.process_list[t]
                    burst_times.append(prev_process.cpu_burst)
                    t += 1 # Increment t
                
                # Calculate response time
                curr_response_time = sum(burst_times) - curr_process.arrival_time
                
                # Update wait times
                response_times.append(curr_response_time)
                self.process_list[i].response_time = curr_response_time

        # Calculate average wait time
        self.avg_response_times = sum(response_times) / len(response_times)

    def __FCFS_TurnaroundTimes(self):
        """"Calculate the response times for each process."""
        
        # Define variables to hold response times for FCFS
        turnaround_times = []

        # Loop through each process and get turnaround times
        for p in self.process_list:
            # Calculate the turnaround time
            turnaround  = p.cpu_burst + p.wait_time
            turnaround_times.append(turnaround)
            # Update process' turnaround time
            p.turnaround_time = turnaround

        # Calculate average wait time
        self.avg_turnaround_times = sum(turnaround_times) / len(turnaround_times)

    def __print_times(self):
        """Print the time-related information from the CPU Scheduler."""
        wt_str = ""
        rt_str = ""
        tat_str = ""
        # Get all stored time values
        for p in self.process_list:
            wt_str += f"\t{p.pid} = {p.wait_time}\n"
            rt_str += f"\t{p.pid} = {p.response_time}\n"
            tat_str += f"\t{p.pid} = {p.turnaround_time}\n"

        # Print all time strings
        print(f"Turnaround times:\n{tat_str}")
        print(f"Wait times:\n{wt_str}")
        print(f"Response times:\n{rt_str}")

        # Print average times
        print(f"Average turnaround time: {round(self.avg_turnaround_times, 3)}")
        print(f"Average wait time: {round(self.avg_wait_times, 3)}")
        print(f"Average response time: {round(self.avg_response_times, 3)}")
        print("\n\n") # Print extra line

    def __RR_TurnaroundTime(self):
        """RR: Calcualte the turnaround times for each process."""
        processes = self.process_list.copy()
        total_turnaround_time = 0
        for i in range(len(processes)):
            p_turnaround_time = processes[i].end_time - processes[i].arrival_time
            '''
            turnaround_time = completion_time - arrival_time
            '''
            total_turnaround_time = total_turnaround_time + p_turnaround_time
            processes[i].turnaround_time = p_turnaround_time
        self.avg_turnaround_times = total_turnaround_time / len(processes)
    
    def __RR_WaitingTime(self):
        """RR: Calculate the wait times for all processes run through RR."""
        processes = self.process_list.copy()
        total_waiting_time = 0
        for i in range(len(processes)):
            waiting_time = processes[i].turnaround_time - processes[i].burst_copy
            total_waiting_time = total_waiting_time + waiting_time
            processes[i].wait_time = waiting_time
        self.avg_wait_times = total_waiting_time / len(processes)

    def __RR_Schedule(self):
        """RR simulation code to process all processes."""
        # Define variables
        processes = self.process_list
        slide_val = self.form.time_slide_val
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        s_time = 0
        
        # Main loop for process execution simulation
        while 1:
            normal_queue = []
            temp = []
            # Check that the process has not yet been processed, and is not in the ready queue
            for i in range(len(processes)):
                if processes[i].arrival_time <= s_time and processes[i].state_code == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if processes[i].pid == ready_queue[k].pid: # If the process is already there, mark it as present
                                present = 1
                
                    # Adds process to the ready queue
                    if present == 0:
                        ready_queue.append(processes[i])
                        temp = []

                    # Ensure that recent processes are at the end of the ready queue
                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k].pid == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                
                # If the process has not been completed...
                elif processes[i].state_code == 0:
                    temp.extend([processes[i].pid, processes[i].arrival_time, processes[i].cpu_burst, processes[i].burst_copy])
                    normal_queue.append(temp)
                    temp = []

            # If both queues are empty, end the loop. We are done
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            
            # If there are still processes in the ready queue, continue...
            if len(ready_queue) != 0:
                # Check if the runtime is more than the slide value
                if ready_queue[0].cpu_burst > slide_val:
                    start_time.append(s_time)
                    s_time = s_time + slide_val
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0].pid)
                    for j in range(len(processes)):
                        if processes[j].pid == ready_queue[0].pid:
                            break
                    processes[j].cpu_burst = processes[j].cpu_burst - slide_val
                    ready_queue.pop(0)
                # If the runtime is less than the slide val, finish executing it
                elif ready_queue[0].cpu_burst <= slide_val:
                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0].cpu_burst
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0].pid)
                    for j in range(len(processes)):
                        if processes[j].pid == ready_queue[0].pid:
                            break
                    processes[j].cpu_burst = 0
                    processes[j].state_code = 1
                    processes[j].end_time = e_time
                    ready_queue.pop(0)
            # If the ready queue is empty, ...
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0].arrival_time:
                    s_time = normal_queue[0].arrival_time
                # Check if the execution time is greater than the current time slice
                if normal_queue[0].cpu_burst > slide_val:
                    start_time.append(s_time)
                    s_time = s_time + slide_val
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0].pid)
                    for j in range(len(processes)):
                        if processes[j].pid == normal_queue[0].pid:
                            break
                    processes[j].cpu_burst = processes[j].cpu_burst - slide_val
                # Complete the execution if the burst time is <= to the time slice
                elif normal_queue[0].cpu_burst <= slide_val:
                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0].cpu_burst
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0].cpu_burst)
                    for j in range(len(processes)):
                        if processes[j].pid == normal_queue[0].pid:
                            break
                    processes[j].cpu_burst = 0
                    processes[j].state_code = 1
                    processes[j].end_time = e_time
        # Store the execution log
        self.execution_log = executed_process

        # Reset Burst Time values
        for p in self.process_list:
            p.cpu_burst = p.burst_copy

    def __RR_GanttChart(self):
        time = 0
        gantt_chart_string = ""
        for exec in self.execution_log:
            # Get the upper and lower bounds of the time slide
            lb = time
            ub = time + self.form.time_slide_val

            # Add current process to string
            gantt_chart_string += f"[{lb}-{ub}]\t{exec} running\n"

            # Increment time
            time += self.form.time_slide_val
        
        # Print the gantt chart
        print(gantt_chart_string)