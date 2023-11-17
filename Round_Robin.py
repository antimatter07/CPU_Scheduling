
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

# ------------------------------------------------------------
# Round Robin
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

    process_count = len(process_list)

    cur_process = None

    # sort process list by arrival time
    scheduled_list = sorted(process_list, key=lambda x: x.at)

    queue = []

    done_processes = []
    
    # check if a process arrived in the given time
    # if True, append it to the queue
    def queue_arrived_process(time):
        for process in scheduled_list:
            if process.at == time:
                queue.append(scheduled_list.pop(0))
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
                for t in range(start_time, cpu_time):
                    queue_arrived_process(t)

                # append the current process to the end of the queue
                queue.append(cur_process)
            
            else:
                cpu_time += cur_process.bt
                cur_process.bt = 0
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

# [Process('P1', 1, 20), Process('P2', 3, 4), Process('P3', 8, 6), Process('P4', 11, 12)]
process_list = [Process(1, 6, 27), Process(2, 10, 22), Process(3, 13, 20), Process(4, 20, 19), Process(5, 23, 4)]
print_processes(round_robin(process_list, 10))