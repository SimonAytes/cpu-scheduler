import cpu_scheduler_tools as ct

# Print welcome message
print("""
-------------------------------------------------
            CPU Scheduling Simulation
-------------------------------------------------
""")

# Start program
temp = ct.CPU_Scheduler()

if temp.form.scheduler_type_code == 0:
    # Run FCFS Simulation
    temp.FCFS()
else:
    # Run RR Sumulation
    temp.RR()

# Print output message
print("""
-------------------------------------------------
Project done by Simon A. Aytes
-------------------------------------------------
""")

