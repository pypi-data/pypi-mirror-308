# Function to calculate page faults using FIFO
def fifo(pages, capacity):
    page_faults = 0
    memory = []
    for page in pages:
        if page not in memory:
            page_faults += 1
            if len(memory) == capacity:
                memory.pop(0)  # Remove the first page in memory (FIFO)
            memory.append(page)
    return page_faults

# Function to calculate page faults using LRU
def lru(pages, capacity):
    page_faults = 0
    memory = []
    page_indices = {}
    
    for i, page in enumerate(pages):
        if page not in memory:
            page_faults += 1
            if len(memory) == capacity:
                # Find the least recently used page
                lru_page = min(page_indices, key=page_indices.get)
                memory.remove(lru_page)
                page_indices.pop(lru_page)
            memory.append(page)
        page_indices[page] = i  # Update the index of the page
    return page_faults

# Function to calculate page faults using Optimal Page Replacement
def optimal(pages, capacity):
    page_faults = 0
    memory = []

    for i, page in enumerate(pages):
        if page not in memory:
            page_faults += 1
            if len(memory) == capacity:
                # Determine the page to be replaced
                farthest = 0
                page_to_remove = None
                for m in memory:
                    if m not in pages[i+1:]:
                        page_to_remove = m
                        break
                    else:
                        next_use = pages[i+1:].index(m)
                        if next_use > farthest:
                            farthest = next_use
                            page_to_remove = m
                memory.remove(page_to_remove)
            memory.append(page)
    return page_faults

# Testing the algorithms
# pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
# capacity = 3

# print("FIFO Page Faults:", fifo(pages, capacity))
# print("LRU Page Faults:", lru(pages, capacity))
# print("Optimal Page Faults:", optimal(pages, capacity))



from collections import deque

# Function for FCFS (First-Come-First-Serve) Scheduling
def fcfs(processes):
    n = len(processes)
    processes.sort(key=lambda x: x['arrival_time'])  # Sort by arrival time
    gantt_chart = []
    time = 0

    for p in processes:
        if time < p['arrival_time']:
            time = p['arrival_time']  # If the CPU is idle, jump to the process arrival
        start_time = time
        time += p['burst_time']
        end_time = time
        gantt_chart.append((p['pid'], start_time, end_time))
    return gantt_chart

# Function for SJF (Shortest Job First) Scheduling
def sjf(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))  # Sort by arrival, then burst
    n = len(processes)
    gantt_chart = []
    time = 0
    ready_queue = []
    remaining_processes = processes.copy()

    while remaining_processes or ready_queue:
        # Load processes into the ready queue based on the current time
        while remaining_processes and remaining_processes[0]['arrival_time'] <= time:
            ready_queue.append(remaining_processes.pop(0))
        # Sort ready queue by burst time
        ready_queue.sort(key=lambda x: x['burst_time'])
        
        if ready_queue:
            p = ready_queue.pop(0)
            start_time = time
            time += p['burst_time']
            end_time = time
            gantt_chart.append((p['pid'], start_time, end_time))
        else:
            # If no process is ready, move to the next process arrival time
            time = remaining_processes[0]['arrival_time']
    return gantt_chart

# Function for Round Robin Scheduling
def round_robin(processes, quantum):
    n = len(processes)
    processes = sorted(processes, key=lambda x: x['arrival_time'])  # Sort by arrival time
    gantt_chart = []
    time = 0
    ready_queue = deque()
    remaining_burst_times = {p['pid']: p['burst_time'] for p in processes}
    remaining_processes = processes.copy()

    # Initialize ready queue with processes that have arrived at time 0
    while remaining_processes and remaining_processes[0]['arrival_time'] <= time:
        ready_queue.append(remaining_processes.pop(0))

    while ready_queue:
        p = ready_queue.popleft()
        start_time = time
        execution_time = min(remaining_burst_times[p['pid']], quantum)
        time += execution_time
        remaining_burst_times[p['pid']] -= execution_time
        end_time = time
        gantt_chart.append((p['pid'], start_time, end_time))
        
        # Add newly arrived processes to the ready queue
        while remaining_processes and remaining_processes[0]['arrival_time'] <= time:
            ready_queue.append(remaining_processes.pop(0))
        
        # Re-add process to queue if it's not finished
        if remaining_burst_times[p['pid']] > 0:
            ready_queue.append(p)
    
    return gantt_chart

# Function to display Gantt chart
def display_gantt_chart(gantt_chart):
    print("Gantt Chart:")
    for (pid, start, end) in gantt_chart:
        print(f"P{pid} [{start} - {end}]", end=" | ")
    print()

# Sample processes
processes = [
    {'pid': 1, 'arrival_time': 0, 'burst_time': 8},
    {'pid': 2, 'arrival_time': 1, 'burst_time': 4},
    {'pid': 3, 'arrival_time': 2, 'burst_time': 9},
    {'pid': 4, 'arrival_time': 3, 'burst_time': 5}
]

quantum = 3

# # Run FCFS
# print("FCFS Scheduling")
# fcfs_chart = fcfs(processes)
# display_gantt_chart(fcfs_chart)

# # Run SJF
# print("\nSJF Scheduling")
# sjf_chart = sjf(processes)
# display_gantt_chart(sjf_chart)

# # Run Round Robin
# print("\nRound Robin Scheduling (Quantum = 3)")
# rr_chart = round_robin(processes, quantum)
# display_gantt_chart(rr_chart)



















import threading
import time

# Function to print numbers
def print_numbers():
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)  # Sleep to simulate work and allow switching

# Function to print letters
def print_letters():
    for letter in "ABCDE":
        print(f"Letter: {letter}")
        time.sleep(1)  # Sleep to simulate work and allow switching

# Creating threads
# thread1 = threading.Thread(target=print_numbers)
# thread2 = threading.Thread(target=print_letters)

# Starting threads
# thread1.start()
# thread2.start()

# # Waiting for threads to complete
# thread1.join()
# thread2.join()

# print("Finished printing numbers and letters.")





# import threading
# import time
# import random

# # Number of philosophers
# num_philosophers = 5

# # Semaphores to represent forks
# forks = [threading.Semaphore(1) for _ in range(num_philosophers)]

# def philosopher(i):
#     while True:
#         print(f"Philosopher {i} is thinking.")
#         time.sleep(random.uniform(1, 3))  # Simulate thinking

#         # Pick up forks (left and right)
#         left_fork = forks[i]
#         right_fork = forks[(i + 1) % num_philosophers]
        
#         # Lock both forks for eating
#         with left_fork:
#             with right_fork:
#                 print(f"Philosopher {i} is eating.")
#                 time.sleep(random.uniform(1, 2))  # Simulate eating

# # Creating and starting threads for each philosopher
# threads = []
# for i in range(num_philosophers):
#     t = threading.Thread(target=philosopher, args=(i,))
#     threads.append(t)
#     t.start()

# # Join threads (in a real program, we might want to allow termination)
# for t in threads:
#     t.join()



import threading
import time
import random

# Buffer settings
buffer = []
buffer_size = 5
buffer_lock = threading.Lock()  # Lock for buffer access
empty = threading.Semaphore(buffer_size)  # Tracks empty spaces
full = threading.Semaphore(0)  # Tracks filled spaces

# Producer function
def producer():
    while True:
        item = random.randint(1, 100)
        empty.acquire()  # Wait if buffer is full
        with buffer_lock:
            buffer.append(item)
            print(f"Producer produced: {item}")
        full.release()  # Signal that an item is added
        time.sleep(random.uniform(0.5, 1.5))  # Simulate production time

# Consumer function
def consumer():
    while True:
        full.acquire()  # Wait if buffer is empty
        with buffer_lock:
            item = buffer.pop(0)
            print(f"Consumer consumed: {item}")
        empty.release()  # Signal that a slot is free
        time.sleep(random.uniform(0.5, 1.5))  # Simulate consumption time

# # Creating and starting producer and consumer threads
# producer_thread = threading.Thread(target=producer)
# consumer_thread = threading.Thread(target=consumer)

# producer_thread.start()
# consumer_thread.start()

# # Join threads (in a real program, we might want to allow termination)
# producer_thread.join()
# consumer_thread.join()










# Banker's Algorithm implementation

# Number of processes
num_processes = 5

# Number of resources
num_resources = 3

# Resources currently available
available = [3, 3, 2]

# Maximum demand of each process
maximum = [
    [7, 5, 3],  # P0
    [3, 2, 2],  # P1
    [9, 0, 2],  # P2
    [2, 2, 2],  # P3
    [4, 3, 3]   # P4
]

# Resources currently allocated to each process
allocation = [
    [0, 1, 0],  # P0
    [2, 0, 0],  # P1
    [3, 0, 2],  # P2
    [2, 1, 1],  # P3
    [0, 0, 2]   # P4
]

# Calculating the need matrix
need = [[maximum[i][j] - allocation[i][j] for j in range(num_resources)] for i in range(num_processes)]

# Function to check if resources can be allocated to a process
def is_safe():
    work = available[:]
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        allocated = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                # Allocate resources to process i
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                allocated = True
                print(f"Process P{i} has been allocated resources and finished.")
                break
        if not allocated:
            print("System is in an unsafe state! Deadlock may occur.")
            return False, []

    print("System is in a safe state.")
    print("Safe sequence:", safe_sequence)
    return True, safe_sequence

# Function to request resources for a process
def request_resources(process_id, request):
    print(f"Process P{process_id} is requesting resources: {request}")

    # Check if request can be granted
    if all(request[j] <= need[process_id][j] for j in range(num_resources)) and \
       all(request[j] <= available[j] for j in range(num_resources)):
        
        # Temporarily allocate requested resources
        for j in range(num_resources):
            available[j] -= request[j]
            allocation[process_id][j] += request[j]
            need[process_id][j] -= request[j]

        # Check if this allocation leaves the system in a safe state
        safe, _ = is_safe()
        
        # Rollback if not safe
        if not safe:
            for j in range(num_resources):
                available[j] += request[j]
                allocation[process_id][j] -= request[j]
                need[process_id][j] += request[j]
            print(f"Request by Process P{process_id} cannot be granted safely.")
            return False
        print(f"Request by Process P{process_id} has been granted.")
        return True

    print(f"Request by Process P{process_id} is invalid or exceeds needs.")
    return False

# # Run the safety algorithm to check the initial state
# is_safe()

# # Sample request for resources by process P1
# request_resources(1, [1, 0, 2])  # Modify this request to test different scenarios





class IndexedFileAllocation:
    def __init__(self, total_blocks, index_size):
        self.total_blocks = total_blocks
        self.index_size = index_size
        self.disk = [None for _ in range(total_blocks)]  # Initially, all blocks are free
        self.index_block = [None for _ in range(index_size)]  # Index block for storing pointers

    def allocate(self, file_size):
        if file_size > self.index_size:
            print("File size exceeds the number of available index blocks.")
            return False

        allocated_blocks = []
        for i in range(self.total_blocks):
            if self.disk[i] is None:
                allocated_blocks.append(i)
            if len(allocated_blocks) == file_size:
                break

        if len(allocated_blocks) != file_size:
            print("Cannot allocate file. Not enough free blocks.")
            return False

        # Create index block for the file
        for i in range(file_size):
            self.index_block[i] = allocated_blocks[i]

        # Allocate file blocks
        for i in range(file_size):
            self.disk[allocated_blocks[i]] = 'F'  # 'F' represents a file in the block

        print(f"File allocated with blocks: {allocated_blocks}, index block: {self.index_block[:file_size]}")
        return True

    def deallocate(self, start_block, file_size):
        for i in range(file_size):
            self.disk[self.index_block[i]] = None
            self.index_block[i] = None
        print(f"File deallocated starting from block {start_block}.")

    def display_disk(self):
        print("Disk Allocation:", self.disk)
        print("Index Block:", self.index_block)


# Example usage:
# indexed_alloc = IndexedFileAllocation(10, 5)
# indexed_alloc.allocate(3)
# indexed_alloc.display_disk()
# indexed_alloc.deallocate(0, 3)
# indexed_alloc.display_disk()












class LinkedFileAllocation:
    def __init__(self, total_blocks):
        self.total_blocks = total_blocks
        self.disk = [None for _ in range(total_blocks)]  # Initially, all blocks are free

    def allocate(self, file_size):
        allocated_blocks = []
        for i in range(self.total_blocks):
            if self.disk[i] is None:
                allocated_blocks.append(i)
            if len(allocated_blocks) == file_size:
                break

        if len(allocated_blocks) != file_size:
            print("Cannot allocate file. Not enough free blocks.")
            return False

        # Link the blocks
        for i in range(file_size - 1):
            self.disk[allocated_blocks[i]] = allocated_blocks[i + 1]
        self.disk[allocated_blocks[-1]] = None  # Last block points to None, indicating end of file
        print(f"File allocated with blocks: {allocated_blocks}")
        return True

    def deallocate(self, start_block, file_size):
        current_block = start_block
        for _ in range(file_size):
            next_block = self.disk[current_block]
            self.disk[current_block] = None
            current_block = next_block
        print(f"File deallocated starting from block {start_block}.")

    def display_disk(self):
        print("Disk Allocation:", self.disk)


# Example usage:
# linked_alloc = LinkedFileAllocation(10)
# linked_alloc.allocate(4)
# linked_alloc.display_disk()
# linked_alloc.deallocate(0, 4)
# linked_alloc.display_disk()



















class ContiguousFileAllocation:
    def __init__(self, total_blocks):
        self.total_blocks = total_blocks
        self.disk = ['-' for _ in range(total_blocks)]  # Initially, all blocks are free

    def allocate(self, start_block, file_size):
        # Check if enough contiguous blocks are available
        if start_block + file_size <= self.total_blocks:
            for i in range(start_block, start_block + file_size):
                if self.disk[i] != '-':
                    print(f"Cannot allocate file. Block {i} is already occupied.")
                    return False
            # Allocate blocks
            for i in range(start_block, start_block + file_size):
                self.disk[i] = 'F'  # 'F' represents a file in the block
            print(f"File allocated from block {start_block} to {start_block + file_size - 1}.")
            return True
        else:
            print(f"Cannot allocate file. Not enough contiguous space.")
            return False

    def deallocate(self, start_block, file_size):
        for i in range(start_block, start_block + file_size):
            self.disk[i] = '-'
        print(f"File deallocated from block {start_block} to {start_block + file_size - 1}.")

    def display_disk(self):
        print("Disk Allocation:", "".join(self.disk))


# Example usage:
# contiguous_alloc = ContiguousFileAllocation(10)
# contiguous_alloc.allocate(2, 3)
# contiguous_alloc.display_disk()
# contiguous_alloc.deallocate(2, 3)
# contiguous_alloc.display_disk()

















"""
Shell programming is a way of writing scripts to automate tasks in Unix/Linux-like environments. It allows users to control the system, manage files, and execute commands in a simple way.

Here's an introduction to some basic shell programming concepts with examples of common shell scripts:

---

### 1. **Basic Shell Script**

A shell script is a text file containing a series of commands. The script file typically starts with a shebang (`#!/bin/bash`), which tells the system to use the Bash shell to interpret the script.

**Example: Basic Hello World Script**

```bash
#!/bin/bash
# This script prints "Hello, World!" to the terminal
echo "Hello, World!"
```

Save the file as `hello_world.sh`. To run the script:
1. Make the script executable:
   ```bash
   chmod +x hello_world.sh
   ```
2. Execute the script:
   ```bash
   ./hello_world.sh
   ```

---

### 2. **Variables in Shell Script**

Shell scripts can store and manipulate variables.

**Example: Using Variables**

```bash
#!/bin/bash
# A script to demonstrate variables
name="John Doe"
age=25
echo "Name: $name"
echo "Age: $age"
```

---

### 3. **Conditional Statements**

Shell scripting supports conditional statements (`if`, `else`, `elif`) for decision-making.

**Example: If-Else Statement**

```bash
#!/bin/bash
# A script to check if a number is positive or negative
echo "Enter a number:"
read number
if [ $number -gt 0 ]; then
    echo "The number is positive."
elif [ $number -lt 0 ]; then
    echo "The number is negative."
else
    echo "The number is zero."
fi
```

---

### 4. **Loops in Shell Script**

You can use loops to repeat tasks. Common types of loops are `for`, `while`, and `until`.

**Example: For Loop**

```bash
#!/bin/bash
# A script to print numbers from 1 to 5
for i in {1..5}
do
    echo "Number: $i"
done
```

**Example: While Loop**

```bash
#!/bin/bash
# A script to print numbers from 1 to 5 using a while loop
i=1
while [ $i -le 5 ]
do
    echo "Number: $i"
    ((i++))
done
```

---

### 5. **Functions in Shell Script**

You can define functions in shell scripts to organize code and make it reusable.

**Example: Function in Shell Script**

```bash
#!/bin/bash
# A script to define a function that greets the user

greet_user() {
    echo "Hello, $1! Welcome to shell scripting."
}

echo "Enter your name:"
read name
greet_user $name
```

---

### 6. **Handling User Input**

Shell scripts can accept user input through the `read` command.

**Example: Accepting User Input**

```bash
#!/bin/bash
# A script to ask for user's name and greet them
echo "What is your name?"
read name
echo "Hello, $name!"
```

---

### 7. **File Operations in Shell Script**

Shell scripts can create, read, and manipulate files.

**Example: Creating and Writing to a File**

```bash
#!/bin/bash
# A script to create a file and write to it

echo "Enter some text to write to a file:"
read text
echo $text > myfile.txt
echo "Text written to myfile.txt"
```

**Example: Reading from a File**

```bash
#!/bin/bash
# A script to read from a file and display its contents

echo "Enter the file name to read from:"
read filename
if [ -f $filename ]; then
    cat $filename
else
    echo "File does not exist."
fi
```

---

### 8. **Command-Line Arguments**

Shell scripts can take command-line arguments using `$1`, `$2`, etc.

**Example: Script with Command-Line Arguments**

```bash
#!/bin/bash
# A script to greet the user with a command-line argument

echo "Hello, $1!"
```

To run the script:
```bash
./greet.sh John
```

Output:
```
Hello, John!
```

---

### 9. **Error Handling and Exit Status**

Shell scripts can use exit codes to indicate whether a command was successful or failed.

**Example: Exit Status Check**

```bash
#!/bin/bash
# A script that checks if a file exists and displays a message

echo "Enter the filename:"
read filename
if [ -f $filename ]; then
    echo "The file $filename exists."
else
    echo "The file $filename does not exist."
    exit 1  # Exit with error status
fi
```

---

### 10. **Pipes and Redirects**

Shell scripts can use pipes (`|`) and redirection (`>`, `>>`) to manage input and output.

**Example: Redirect Output to a File**

```bash
#!/bin/bash
# A script to list files and redirect output to a file

ls > files_list.txt
echo "List of files saved to files_list.txt."
```

**Example: Pipe Output from One Command to Another**

```bash
#!/bin/bash
# A script to search for a word in a file using pipe

echo "Enter the word to search:"
read word
grep $word myfile.txt | wc -l
```

---

### Conclusion

Shell programming is a powerful way to automate system tasks and create scripts that interact with the system. By combining commands, variables, conditionals, loops, and functions, you can perform complex tasks with just a few lines of code. The examples provided above are just some of the basic building blocks of shell programming.

Would you like to dive deeper into any of these concepts or see additional examples?
"""