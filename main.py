import csv

def FCFS(id, AT, BT):
  ST = []
  ET = []
  WTs = []
  time = 0
  avgWT = 0
  idCopy = id.copy()
  while len(id) > 0:
    if time == 0:
      time += AT[0]
    ST.append(time)
    time += BT[0]
    ET.append(time)
    WTs.append((time - AT[0]) - BT[0])
    id.pop(0)
    BT.pop(0)
    AT.pop(0)
    
  avgWT = round(sum(WTs)/len(WTs), 1)
  for i in range(len(ST)):
    print(str(idCopy[i]) + " start time: " + str(ST[i]) + " end time: " + str(ET[i]) + " | waiting time: " + str(WTs[i]))
  print("Average waiting time: " + str(avgWT) + "\n")
  
def SJF(id, AT, BT):
  ST = [0] * len(id)
  ET = [0] * len(id)
  WTs = [0] * len(id)
  queue = []
  time = 0
  avgWT = 0 
  Procs = list(zip(id, AT, BT))
  sortedProcs = sorted(Procs, key=lambda x: (x[1], x[2]))
  queue.append(sortedProcs[0])
  sortedProcs.pop(0)

  while queue:
    if time == 0:
      time += queue[0][1]

    if len(queue) > 1:
      queue = sorted(queue, key=lambda x: x[2])

    ST[queue[0][0] - 1] = time
    time += queue[0][2]
    ET[queue[0][0] - 1] = time
    WTs[queue[0][0] - 1] = (time - queue[0][1]) - queue[0][2]
    
    if len(sortedProcs) > 0:
      copyList = sortedProcs.copy()
      for i in range(len(copyList)):
        if copyList[i][1] <= time:
          queue.append(copyList[i])
          sortedProcs.remove(copyList[i])
        else:
          break
          
    queue.pop(0)
    
  avgWT = round(sum(WTs)/len(WTs), 1)
  for i in range(len(ST)):
    print(str(id[i]) + " start time: " + str(ST[i]) + " end time: " + str(ET[i])+ " | waiting time: " + str(WTs[i]))
  print("Average waiting time: " + str(avgWT) + "\n")
  
class Process:
  """
    object representing a process.

    Attributes:
    - p_id (int): unique identifier for the process.
    - at (int): time at which the process arrives in the ready queue.
    - bt (int): burst time for the process to execute.
    - rem (int): remaining time for the process to complete its execution.
    - start (list): list to account for multiple start times for pre-emptive algorithms.
    - end (list): list to account for multiple end times for pre-emptive algorithms.
    - wait (int): total waiting time of the process in the ready queue.
    """

  def __init__(self, p_id, at, bt):
    """
      Instantiate a new Process instance.

      Parameters:
      - p_id (int): unique identifier for the process.
      - at (int): time at which the process arrives in the ready queue.
      - bt(int): time required by the process to execute.
    """

    self.p_id = p_id
    self.at = at
    self.bt = bt


    self.rem = bt

    #array to account for start and end time multiple times for pre-emptive algos
    self.start = []
    self.end = []

    #waiting time
    self.wait = 0



def print_processes(process_list):
  """
  Prints a list of processes in the proper format after scheduling algorithm executed.
  Also displays average waiting time.
  
  Params:
  - process_list (Process list): list of Processes to display

  """

  for process in process_list:
      start_end_pairs = [
          "start time: {} end time: {}".format(start, end)
          for start, end in zip(process.start, process.end)
      ]

      process_info = "{} {} | Waiting time: {}".format(
          process.p_id, ' | '.join(start_end_pairs), process.wait
      )
      print(process_info)

    # calculate and print average waiting time
  total_waiting_time = sum(process.wait for process in process_list)
  average_waiting_time = total_waiting_time / len(process_list)
  print("Average waiting time: {:.1f}".format(average_waiting_time))


def round_robin(process_list, qt):
    """
    Executes round robin on a list of processes and quantum time

    Params:
    process_list (Process list): list of Process objects made from user input
    qt: quantum time/time slice value

    Returns:
    done_processes: list of finished processes with updated start, end, and wait times.
    """
    # init values
    cpu_time = 0

    cur_process = None

    # sort process list by arrival time
    scheduled_list = sorted(process_list, key=lambda x: x.at)

    queue = []

    done_processes = []
    
    # check if processes arrived in the given time
    # if True, append it to the queue
    def queue_arrived_process(cur_time):
      for process in scheduled_list:
          if process.at <= cur_time:
              queue.append(scheduled_list.pop(0))
          else:
              break

    # while there is an unfinished process
    while scheduled_list or queue:
        # if a process arrives, add it to the end of the queue
        queue_arrived_process(cpu_time)
        
        # if a process is in queue
        if queue:
            
            # get the first item in the queue as the cur_process
            cur_process = queue.pop(0)

            # append a new start time
            start_time = cpu_time
            cur_process.start.append(start_time)
            
            # update cpu_time, cur_process.bt, and queue
            # depending on the remaining burst time in cur_process
            if cur_process.bt > qt:
                cpu_time += qt
                cur_process.bt -= qt

                # queue any processes that arrived during
                # the cur_process run time
                if scheduled_list:
                  for t in range(start_time, cpu_time):
                    queue_arrived_process(t)

                # append the current process to the end of the queue
                queue.append(cur_process)
            
            else:
                cpu_time += cur_process.bt
                cur_process.bt = 0

                # queue any processes that arrived during
                # the cur_process run time
                if scheduled_list:
                  for t in range(start_time, cpu_time):
                    queue_arrived_process(t)
                  
                done_processes.append(cur_process)

            # append a new end time
            cur_process.end.append(cpu_time)

        # if queue is empty, increment cpu time
        else:
            cpu_time += 1
    

    # compute the waiting time of all processes
    for process in done_processes:
        process.wait = process.start[0] - process.at
        for i in range(1, len(process.start)):
            process.wait += (process.start[i] - process.end[i-1])

    done_processes = sorted(done_processes, key=lambda x: x.p_id)
    return done_processes 


def srtf(process_list):
  """
  Executes shortest remaining time first on a list of processes.

  Params:
  process_list (Process list): list of Process objects made from user input

  Returns:
  done_processes: list of finished processes with updated start, end, and wait times.
  """

  cpu_time = 0

  process_number = len(process_list)

  cur_process = None

  ready_q = []

  prev_id = -1


  done_processes = []

  #as long as process list is not empty
  while process_list and process_number > 0:


    #sort in asc order according to arrival time
    process_list = sorted(process_list, key=lambda x: x.at)

    #add arrived processes to ready queu at current cpu time
    for p in process_list:
     
      if p.at == cpu_time:
        ready_q.append(p)
      #break if arrival time is greater than cpu time since list is sorted
      elif p.at > cpu_time:
        break


    if len(ready_q) > 0:
     
      #sort ready queue according to shortest remaining time first
      ready_q.sort(key=lambda x: x.rem)
      cur_process = ready_q.pop(0)



      #if list is empty, first time process ran, making cur time a start time
      # or if previous process is not the chosen one from ready queue, it is start time
      if not cur_process.start or prev_id != cur_process.p_id:
        cur_process.start.append(cpu_time)

        #find process with previous id and set end time to current time, since a new process has just started
        for process in ready_q:
          if process.p_id == prev_id:
            process.end.append(cpu_time)

      #every process not currently executing and in ready queue is waiting. increment wait times
      for process in ready_q:
        process.wait += 1


      #Decrement running process remaining time
      cur_process.rem -= 1

      #keep track of prev id
      prev_id = cur_process.p_id

      #if remaining time is 0, process is done
      if cur_process.rem == 0:
        #append to list of end timmes
        cur_process.end.append(cpu_time + 1)

        #add to list of finished processes
        done_processes.append(cur_process)

        #remove from unfinished processes
        process_list.remove(cur_process)

        process_number -= 1
        #otherwise, since the process was popped, put it back in the ready queue
      else:
        #since unfinished current process was popped from ready queue, add it back
        ready_q.append(cur_process)

    #increment current cpu time
    cpu_time += 1



  #sort finished process list according to id 
  done_processes = sorted(done_processes, key=lambda x: x.p_id)
  
  return done_processes

def read_process_list_preemptive(filename, num_processes):
    """
    Reads succeeding lines after first line and returns a list of Process.
    This list is needed for both round robin and shortest remaining time first.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        
        # Skip the first line
        next(reader)
        
        process_list = []
        
        for _ in range(num_processes):
            p_id, at, bt = map(int, next(reader))
            process = Process(p_id, at, bt)
            process_list.append(process)
    
    return process_list


def read_first_line_csv(filename):
    """
    Read first line for extracting algo choice, process count and time quantum.
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=' ')
        x, y, z = map(int, next(reader))
    return x, y, z

def read_processes(filename):
    """
    Read processes for SJF and FCFCS.
    """
    with open(filename, 'r') as file:
      
      #skip first line
      
        reader = csv.reader(file, delimiter = '\t')
       #skip first line
        next(reader)
    
        data = [row[0] for row in reader]
    file.close()
    return data
  
#Change filename to csv file with data
filename = "input.txt"

x, y, z = read_first_line_csv(filename)

if x == 0:
    print('Executing first come first first served (FCFS)')
    process_info = read_processes(filename)
    id = []
    AT = []
    BT = []
    arr = 0

    for i in range(y):
      s = process_info[i]
      arr = 0
      for j in s.split():
        if j.isdigit():
            j = int(j)
            if arr == 0:
              id.append(j)
            elif arr == 1:
              AT.append(j)
            elif arr == 2:
              BT.append(j)
        arr+=1
    
    FCFS(id, AT, BT)
    
    
    
    
elif x == 1:
    print('Executing shortest job first (SJF)')
    
    process_info = read_processes(filename)
    id = []
    AT = []
    BT = []
    arr = 0

    for i in range(y):
      s = process_info[i]
      arr = 0
      for j in s.split():
        if j.isdigit():
            j = int(j)
            if arr == 0:
              id.append(j)
            elif arr == 1:
              AT.append(j)
            elif arr == 2:
              BT.append(j)
        arr+=1
    
    SJF(id, AT, BT)
     
    
    
elif x == 2: 
    print('Executing shortest remaining time first (SRTF)')
    
    process_list = read_process_list_preemptive(filename, y)
    
    done_processes = srtf(process_list)
    print_processes(done_processes)

elif x == 3:
    print('Executing round robin (RR)')
    
    process_list = read_process_list_preemptive(filename, y)
    
    done_processes = round_robin(process_list, z)
    print_processes(done_processes)
    
    
