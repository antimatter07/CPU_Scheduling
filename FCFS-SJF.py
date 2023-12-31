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

def getInput(filename):
  with open(filename, 'r') as file:
    reader = csv.reader(file, delimiter = '\t')
    data = [row[0] for row in reader]
  file.close()
  return data
  
def main():
    inputs = getInput("input01.txt")
    choice = inputs[0]
    res = []
    for i in choice.split():
      if i.isdigit():
          i = int(i) 
          res.append(i)
    inputs.pop(0)

    id = []
    AT = []
    BT = []
    arr = 0

    for i in range(res[1]):
      s = inputs[i]
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
    print("\n")
    if res[0] in range(0, 4):
      match res[0]:
        case 0:
          FCFS(id, AT, BT)
        case 1:
          SJF(id, AT, BT)
        case _:
          print("Please enter the correct Algorithm number")
          print("-----------------------------------------------------------------------------")
          main()

main()  