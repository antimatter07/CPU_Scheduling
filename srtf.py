
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

xyz = input("Input: ")
input_xyz = xyz.split()

x = int(input_xyz[0])
y = int(input_xyz[1])
z = int(input_xyz[2])



process_list = []
while y > 0:
  abc = input("Enter process details:")

  splitted_abc = abc.split()

  p_id = int(splitted_abc[0])
  at = int(splitted_abc[1])
  bt = int(splitted_abc[2])

  new_process = Process(p_id, at, bt)

  process_list.append(new_process)
  y -= 1

if x == 0:
    print('Executing first come first first served.')
elif x == 1:
    print('Executing shortest job first')
elif x == 2: 
    print('Executing shortest remaining time first.')
    
    done_processes = srtf(process_list)
    print_processes(process_list)
elif x == 3:
    print('Executing round robin')










