import sys



# if there is more than one Nash equilibrium, the Nashwith the highest sum of payoffsshould be returned.
#  If still undecidable the Nash corresponding to the task with lower index for your agent
# and then for the peer agent should be returned



def test(test1, test2):

    for el in test1:
        if el in test2:
            return False
    return True


def decide_nash(matrix):
    print(matrix)
    task = ''
    minelist = findbestmine(matrix)
    maxofmine = max(minelist[1])
    test1 = minelist[0]
    indexofmaxmine = minelist[0][minelist[1].index(maxofmine)]
    peerlist = findbestpeer(matrix)
    test2 = peerlist[0]

    if(test(test1,test2)):
        return "blank-decision"
    maxofpeer = max(peerlist[1])
    indexofmaxpeer = peerlist[0][peerlist[1].index(maxofpeer)]
    if(maxofmine>= maxofpeer):
        task = "mine=T" + str(indexofmaxpeer[0]) + ",peer=T" + str(indexofmaxpeer[1])
    else:
        task = "mine=T" + str(indexofmaxmine[0]) + ",peer=T" + str(indexofmaxmine[1])


    return task

def findbestmine(matrix):
    i=0
    j=0
    temp = [-100000000000000000000,-1000000000000000]
    tempvalues = []
    nashequilibria = -1
    maxvalues = []

    length = len(matrix[i])
    while(j!=length):
        while(i!=len(matrix)):
            if(matrix[i][j][0]>=temp[0]):
                temp=matrix[i][j]
                tempvalues=[i,j]
            i+=1
        if (nashequilibria == -1):
            nashequilibria = []
            sum = 0
            for el in temp:
                sum += el
            maxvalues.append(sum)
            nashequilibria.append(tempvalues)
        elif not tempvalues in nashequilibria:
            sum = 0
            for el in temp:
                sum += el
            maxvalues.append(sum)
            nashequilibria.append(tempvalues)
        temp = [-1000000000000000, -1000000000000]
        i = 0
        j += 1

    return [nashequilibria,maxvalues]

def findbestpeer(matrix):
    i=0
    j=0
    temp = [-100000000000000000000,-1000000000000000]
    tempvalues = []
    nashequilibria = -1
    maxvalues = []


    while(i!=len(matrix)):
        length = len(matrix[i])
        while j!= length:
            if matrix[i][j][1] >= temp[1]:
                temp = matrix[i][j]
                tempvalues = [i, j]

            j += 1

        if nashequilibria == -1:
            nashequilibria = []
            sum = 0
            for el in temp:
                sum += el
            maxvalues.append(sum)
            nashequilibria.append(tempvalues)

        elif not tempvalues in nashequilibria:
            sum = 0
            for el in temp:
                sum += el
            maxvalues.append(sum)
            nashequilibria.append(tempvalues)
        temp=[-1000000000000000,-1000000000000]
        j=0
        i+=1

    return [nashequilibria,maxvalues]


class Agent:

    def __init__(self, state, task):
        self.behavior = state
        if self.behavior == "decide-rational":
            task = task[:-2]
            tasks = self.parse(task)
            self.listoftasks = self.findtasks(tasks)
            self.last_task = None
        elif self.behavior == "decide-nash":
            self.matrix = self.formMatrix(task)

    def update(self, observation):

        for e in self.listoftasks:
            if e.getName() == self.last_task:
                self.update_task(e, observation)

    def decide(self, behavior):
        self.behavior = behavior

        if behavior == "decide-rational":
            task = decide_rational(self.listoftasks)
            self.last_task = task
            return task
        elif behavior == "decide-nash":
            task = decide_nash(self.matrix)
            return task
        else:
            return '1'

    def parse(self, state):
        tasks = state.split("],")
        return tasks

    def findtasks(self, tasks):
        lst = []
        i = 0
        while i != len(tasks):
            if i == 0:
                lst.append(Task(tasks[0][1] + tasks[0][2], tasks[0]))
            else:
                lst.append(Task(tasks[i][0] + tasks[i][1], tasks[i]))
            i += 1
        return lst

    # decide - rational(T1=[A = (1, -1)], T2 = [A = (1, -1)], T3 = [A = (1, -1)], T4 = [A = (30 %, 0), B = (40 %, [B1=(2, 1), B2 = (1, -1)]), C = (30 %, -2)], T5 = [A = (1, -1)]) 4
    # (2, C.C1)
    # (3, C.C2)
    # (2, B.B3)

    def update_task(self, task, observation):
        value = task.getValue()
        first = observation.split("(")
        second = first[1].split(",")
        utility = second[0]
        third = second[1].split(")")
        tasktoupdate = third[0]
        hasnmbr = False
        if (hasNumbers(tasktoupdate)):
            hasnmbr = True
        # (-3, B)
        # (-4, B.B1)
        # senaoexistiremsubtasksadarupdate
        if not (hasnmbr):
            if "%" in value:

                task.setValue("")
            if not (tasktoupdate in task.getValue()):
                task.setValue(task.getValue() + ",")
                task.setValue(task.getValue() + tasktoupdate + "=" + "(1," + utility + ")")
            else:
                a = calculatelistofsubtasks(task.getValue())
                value = ""
                for el in a:
                    if not tasktoupdate in el:
                        value += el
                    else:
                        value += tasktoupdate + "=" + "(1," + utility + ")"
                        task.setValue(value)
        else:
            self.updatetask(tasktoupdate,task,utility)
        pass

    # B = (1, [B1=(1, -4)])

    def updatetask(self, tasktoupdate, task,utility):
        lst = tasktoupdate.split(".")
        value = ""
        subtaskl = lst[0]
        subtaskv = lst[1]
        subtasks = calculatelistofsubtasks(task.getValue())

        found = False
        listofel = []


        for el in subtasks:
            if subtaskl in el:
                found = True
                lastel = el
            else:
                listofel += el
            listofel += ','
        listofel = listofel[:-1]
        if not(found):
            for el in subtasks:
                value += el
            if value!= '':
                value +=','
            value += subtaskl + "=" + "(1, [" + subtaskv + "=(1, " + utility + ")])"

            task.setValue(value)
        else:
            prc = False
            a = calculatelistofsubtasks(lastel)[0].split('(',1)
            b = a[1]
            c = b.split(',',1)
            d = c[0]
            hashh = c[1].split('[')
            hat = []
            if (prc):
                pass
            else:
                if not(len(hashh) <= 1):
                    hat = hashh[1].split(']')

            var = ''.join(listofel)
            init = self.removepercentages(var)
            if("%" in d):
                sumc = 1
                value +=init
                value += ","
                value += subtaskl +"=" + "(" + str(sumc) + ",[" + subtaskv + "=(1, " + utility + ")])"

            else:
                value +=init
                value +=","
                sumc = int(d)+1
                if (subtaskv in c[1]):
                    print("shieeeeeeeeeeet need to do this")
                else:
                    value += subtaskl + "=" + "(" + str(sumc) + ",[" + hat[0] + ", " + subtaskv + "=(1, " + utility + ")])"
            task.setValue(value)

   #A=(30%,0),B=(40%,[B1=(2,1),B2=(1,-1)]),

    def removepercentages(self, var):

        vari = list(var)
        value = []
        found = False
        old = 0
        i=0
        j=0
        while(i!=len(vari)):
            if vari[i]== '(':
                j = i+1
            if vari[i] == '%':
                old = i
                del vari[j:old+1]

            i+=1
        i=0
        for e in vari:
            value += e
            if(e == '(') and vari[i+1]==',':
                value+='0'
            i+=1
        a = "".join(value)
        d = calculatelistofsubtasks(a)
        finalvalue = ''
        for el in d:
            if '(0,0)' in el:
                pass
            else:
                finalvalue +=el
        return finalvalue

    def formMatrix(self, task):

        count = 0
        splitted = task.split(",peer")
        mine = splitted[0][5:]
        peer = splitted[1][1:]
        columns = 0
        rows = 0
        if "T0" in task:
            rows = mine.count("T0|")
            columns = mine.count("|T0")
            count += 1

        x = [['x' for i in range(columns)] for j in range(rows)]

        while(mine!=''):
            a = removeelementfrommine(mine)
            x = putinthematrix(a[0],x, a[2],a[3],'m')
            mine = a[1]
            b = removeelementfrompeer(peer)
            x = putinthematrix(b[0],x, b[2],b[3],'p')
            peer = b[1]
            if(mine==''):
                break
        return x

    #decide - nash
    #mine = (T0 | T0=[A=(2, 2)], T0 | T1 = [A = (1, 1)], T1 | T0 = [A = (1, 1)], T1 | T1 = [A = (1, 2)])
    # peer = (T0 | T0=[A=(1, 2), B = (1, 0)], T0 | T1 = [A = (1, 2)], T1 | T0 = [A = (1, 2)], T1 | T1 = [A = (1, 1)])

    #mine = (T0 | T0=[A=(1, 0)], T0 | T1 = [A = (1, 25)], T0 | T2 = [A = (1, 5)], T1 | T0 = [A = (1, 40)], T1 | T1 = [A = (1, 0)], T1 | T2 = [A = (1, 5)], T2 | T0 = [A = (1, 10)], T2 | T1 = [A = (1, 15)], T2 | T2 = [A = (1, 10)]),
    #peer = (T0 | T0=[A=(1, 0)], T0 | T1 = [A = (1, 25)], T0 | T2 = [A = (1, 5)], T1 | T0 = [A = (1, 40)], T1 | T1 = [A = (1, 0)], T1 | T2 = [A = (1, 5)], T2 | T0 = [A = (1, 10)], T2 | T1 = [A = (1, 15)], T2 | T2 = [A = (1, 10)])

class Task:

    def __init__(self, name, task):
        self.name = name
        parsedtask = self.parseTask(task)
        self.value = parsedtask

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def parseTask(self, task):
        if self.name == "T1":
            return task[5:]
        else:
            return task[4:]


def decide_rational(listoftasks):
    max_utility = -100000000000
    max_utility_task = ''

    utilitiesfound = []
    for t in listoftasks:
        utility = calculatetotalutility(t.getValue())
        utilitiesfound.append(utility)
        if max_utility < utility:
            max_utility = utility
            max_utility_task = t.getName()
    #for e in utilitiesfound:
     #  print(e)
    #print(t.getValue())

    return max_utility_task


'''
returns the inside symbols of task
ex T1 = (A=(30%,0),B=(70%,3)) returns a list first element is A=(30%,0) and 2nd is B=(70%,3)
'''


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def calculatelistofsubtasks(t):
    nest = 0
    value = ''
    listofsubtasks = []
    inside = False
    for char in t:
        if char == '(':
            nest += 1
            inside = True
        if char == ')':
            nest -= 1
            if nest == 0:
                inside = False
                value += char
                listofsubtasks.append(value)
                value = ''
                continue
        if char == ',':
            if not (inside):
                pass
            else:
                value += char
        else:
            value += char
    return listofsubtasks


# B1=(3, 2), B2 = (2, 0)


def findTotal(element):
    total = 0

    while (True):
        one = element.split('(', 1)
        if (len(one) != 1):
            two = one[1].split(',', 1)
        else:
            return total
        firstarg = two[0]
        secarg = two[1]
        element = secarg
        firstvalue = float(firstarg)
        total += firstvalue


def calculateutility(element):
    total = 1
    one = element.split('(', 1)
    two = []
    if (len(one) != 1):
        two = one[1].split(',', 1)
    firstarg = two[0]
    secarg = two[1]

    if "%" in firstarg:
        firstarg = firstarg[:-1]
        firstvalue = float(firstarg) / 100
    else:
        firstvalue = float(firstarg)
        total += firstvalue

    try:
        if secarg[-1] == ')':
            secarg = secarg[:-1]
        secondvalue = float(secarg)

        return firstvalue * secondvalue

    except ValueError:
        return firstvalue * calculatetotalutility(secarg)


def calculatetotalutility(t):
    listofsubtasks = calculatelistofsubtasks(t)
    totalutility = 0.0
    total = 0.0
    for element in listofsubtasks:
        if not ("%" in element):
            total += findTotal(element)
        totalutility += calculateutility(element)

    if total <= 1:
        return totalutility

    else:
        final = totalutility / total
        return final



def removeelementfrommine(mine):
    i=0
    j=0

    if "T0|T0" in mine:
        a = mine.split("T0|T0=[")
        b = a[1].split("]",1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 0]

    if "T0|T1" in mine:
        a = mine.split("T0|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 0]
    if "T0|T2" in mine:
        a = mine.split("T0|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 0]
    if "T0|T3" in mine:
        a = mine.split("T0|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 0]

    if "T1|T0" in mine:
        a = mine.split("T1|T0=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 1]
    if "T1|T1" in mine:
        a = mine.split("T1|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 1]
    if "T1|T2" in mine:
        a = mine.split("T1|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])

        return [util, b[1], 2, 1]
    if "T1|T3" in mine:
        a = mine.split("T1|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 1]
    if "T2|T0" in mine:
        a = mine.split("T2|T0=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 2]
    if "T2|T1" in mine:
        a = mine.split("T2|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 2]
    if "T2|T2" in mine:
        a = mine.split("T2|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 2]
    if "T2|T3" in mine:
        a = mine.split("T2|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 2]
    if "T3|T0" in mine:
        a = mine.split("T3|T0=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 3]
    if "T3|T1" in mine:
        a = mine.split("T3|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 3]
    if "T3|T2" in mine:
        a = mine.split("T3|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 3]
    if "T3|T3" in mine:
        a = mine.split("T3|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 3]

    return [0,'',0,0]

def removeelementfrompeer(peer):
    i=0
    j=0


    if "T0|T0" in peer:
        a = peer.split("T0|T0=[")

        b = a[1].split("]",1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 0]

    if "T0|T1" in peer:
        a = peer.split("T0|T1=[")

        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 1]
    if "T0|T2" in peer:
        a = peer.split("T0|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 2]
    if "T0|T3" in peer:
        a = peer.split("T0|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 0, 3]

    if "T1|T0" in peer:
        a = peer.split("T1|T0=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 0]
    if "T1|T1" in peer:
        a = peer.split("T1|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 1]
    if "T1|T2" in peer:
        a = peer.split("T1|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 2]
    if "T1|T3" in peer:
        a = peer.split("T1|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 1, 3]
    if "T2|T0" in peer:
        a = peer.split("T2|T0=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 0]
    if "T2|T1" in peer:
        a = peer.split("T2|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 1]
    if "T2|T2" in peer:
        a = peer.split("T2|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 2]
    if "T2|T3" in peer:
        a = peer.split("T2|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 2, 3]
    if "T3|T0" in peer:
        a = peer.split("T3|T0=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 0]
    if "T3|T1" in peer:
        a = peer.split("T3|T1=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 1]
    if "T3|T2" in peer:
        a = peer.split("T3|T2=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 2]
    if "T3|T3" in peer:
        a = peer.split("T3|T3=[")
        b = a[1].split("]", 1)
        util = calculatetotalutility(b[0])
        return [util, b[1], 3, 3]

    return [0,'',0,0]



def putinthematrix(util1, x,i,j,m):

    if x[i][j] == 'x':
        x[i][j] = util1
    else:
        a = x[i][j]
        if isinstance(a,list):
            if(len(a)==2):
                return x
        if(m=='m'):
            x[i][j] = [util1,a]
        else:
            x[i][j] = [a,util1]
    return x


args = sys.stdin.readline().split(' ')
agent = Agent(args[0], args[1])
size = 1 if len(args) <= 2 else int(args[2])

for i in range(0, size):
    if i != 0:
        agent.update(sys.stdin.readline())
    sys.stdout.write(agent.decide(args[0]) + '\n')
