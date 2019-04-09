import sys

from linprog import *


def decideutil(firstarg, secarg):
    try:
        e = int(firstarg)
        if e == 0:
            return 1000000000000000000000000
        else:
            return float(secarg)
    except ValueError:

        firstarg = firstarg[:-1]
        if int(firstarg) == 0:
            return 100000000000000000000
        return float(secarg)


def findMinUtility(task):
    a = calculatelistofsubtasks(task.getValue())
    minutility = 1000000000
    for values in a:
        b = values.split('(')
        c = b[1].split(',')
        firstarg = c[0]
        d = c[1].split(')')
        secarg = d[0]
        utility = decideutil(firstarg, secarg)
        if (minutility > utility):
            minutility = utility

    return minutility


# maximizar T1x + T2y

# T1x + T2y > 0
# x,y>=0
# x,y<=1


def createListofineq(param):
    if param == 2:
        return [[1, 0], [0, 1], [-1, 0], [0, -1]]

    elif param == 3:
        return [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

    elif param == 4:
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0],
                [0, 0, 0, -1]]


def createTargetVals(param):
    if param == 2:
        return [1, 1, 0, 0]

    if param == 3:
        return [1, 1, 1, 0, 0, 0]

    if param == 4:
        return [1, 1, 1, 1, 0, 0, 0, 0]


def createEquationLeft(count):
    if count == 2:
        return [[1, 1]]
    if count == 3:
        return [[1, 1, 1]]

    if count == 4:
        return [[1, 1, 1, 1]]


def indices(mylist, value):
    return [i for i, x in enumerate(mylist) if x == value]


def divide(final, lst):
    mylist = []
    finale = []
    indice = []
    for el in lst:
        indice = indices(lst, el)
        if len(indice) > len(mylist):
            if(len(indice) != 1):
                mylist = indice


    sizetodivideby = len(indice)
    maxvalue = max(final)
    i=0

    if(mylist == []):
        return final
    for el in final:
        print(el)
        print(mylist)
        if i in mylist:
            finale.append(maxvalue/sizetodivideby)
        else:
            finale.append(el)
        i+=1
    return finale
def decide_risk(listoftasks):

    lst = []
    minlst = []
    count = 0

    for el in listoftasks:
        utility = findMinUtility(el)
        minlst.append(-utility)
        count += 1

    for el in listoftasks:
        utility = calculatetotalutility(el.getValue())
        lst.append(-utility)

    listofineq = createListofineq(len(lst))
    listoftargetvals = createTargetVals(len(lst))

    listoftargetvals.append(0)
    listofineq.append(minlst)

    B = listoftargetvals
    A = listofineq
    C = lst

    eqL = createEquationLeft(count)



    resolution, sol = linsolve(C, ineq_left=A, ineq_right=B, eq_left=eqL, eq_right=[1])

    if sol is None:
        B = B[:-1]
        A = A[:-1]
        res, sol = linsolve(C, ineq_left=A, ineq_right=B, eq_left=eqL, eq_right=[1])

    final = []
    for el in sol:
        el = round(el, 2)
        final.append(el)

    finalfinal = divide(final, lst)

    task = '('
    sizeo = len(finalfinal)



    length = len(finalfinal)
    j=0

    while(j!=length):
        finalfinal[j] = "{0:.2f}".format(float(finalfinal[j]))
        j+=1

    i=1

    for el in finalfinal:
        if not (el == "0.00"):
            if not (i == sizeo):
                if i == 1:
                    task += str(el) + ",T" + str(i)
                else:
                    task += ";" + str(el) + ",T" + str(i)
            else:
                task += ";"+str(el) + ",T" + str(i)
        i+=1
    task += ")"
    return task


class Agent:

    def __init__(self, state, task):
        self.behavior = state
        if self.behavior == "decide-rational":
            task = task[:-2]
            tasks = self.parse(task)
            self.listoftasks = self.findtasks(tasks)
            self.last_task = None

        elif self.behavior == "decide-nash" or self.behavior == "decide-mixed" or self.behavior == "decide-conditional":
            self.matrix = self.formMatrix(task)


        elif self.behavior == "decide-risk":
            task = task[:-2]
            tasks = self.parse(task)
            self.listoftasks = self.findtasks(tasks)

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

        elif behavior == "decide-mixed":
            task = decide_mixed(self.matrix)
            return task

        elif behavior == "decide-conditional":
            task = decide_nash(self.matrix)
            if task == "blank-decision":
                return decide_mixed(self.matrix)
            else:
                return task
        elif behavior == "decide-risk":
            task = decide_risk(self.listoftasks)
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
            self.updatetask(tasktoupdate, task, utility)
        pass

    # B = (1, [B1=(1, -4)])

    def updatetask(self, tasktoupdate, task, utility):
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
        if not (found):
            for el in subtasks:
                value += el
            if value != '':
                value += ','
            value += subtaskl + "=" + "(1, [" + subtaskv + "=(1, " + utility + ")])"

            task.setValue(value)
        else:
            prc = False
            a = calculatelistofsubtasks(lastel)[0].split('(', 1)
            b = a[1]
            c = b.split(',', 1)
            d = c[0]
            hashh = c[1].split('[')
            hat = []
            if (prc):
                pass
            else:
                if not (len(hashh) <= 1):
                    hat = hashh[1].split(']')

            var = ''.join(listofel)
            init = self.removepercentages(var)
            if ("%" in d):
                sumc = 1
                value += init
                value += ","
                value += subtaskl + "=" + "(" + str(sumc) + ",[" + subtaskv + "=(1, " + utility + ")])"

            else:
                value += init
                value += ","
                sumc = int(d) + 1
                if (subtaskv in c[1]):
                    print("shieeeeeeeeeeet need to do this")
                else:
                    value += subtaskl + "=" + "(" + str(sumc) + ",[" + hat[
                        0] + ", " + subtaskv + "=(1, " + utility + ")])"
            task.setValue(value)

    # A=(30%,0),B=(40%,[B1=(2,1),B2=(1,-1)]),

    def removepercentages(self, var):

        vari = list(var)
        value = []
        found = False
        old = 0
        i = 0
        j = 0
        while (i != len(vari)):
            if vari[i] == '(':
                j = i + 1
            if vari[i] == '%':
                old = i
                del vari[j:old + 1]

            i += 1
        i = 0
        for e in vari:
            value += e
            if (e == '(') and vari[i + 1] == ',':
                value += '0'
            i += 1
        a = "".join(value)
        d = calculatelistofsubtasks(a)
        finalvalue = ''
        for el in d:
            if '(0,0)' in el:
                pass
            else:
                finalvalue += el
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

        # mine = T0|T0 = 2, T0|T1 = 5, T1|T0 = 3, T1|T1 = 7
        # peer = T0|T0 = -1, T0|T1 = -2, T1|T0 = 4, T1|T1 = 6

        '''
        (-1,2)   (-2,3)
        
        (4,5)     (6,7)
        
        '''

        while (mine != ''):
            a = removeelementfrommine(mine)
            x = putinthematrix(a[0], x, a[2], a[3], 'm')
            mine = a[1]
            b = removeelementfrompeer(peer)
            x = putinthematrix(b[0], x, b[2], b[3], 'p')
            peer = b[1]
            if (mine == ''):
                break
        return x


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
    # for e in utilitiesfound:
    #  print(e)
    # print(t.getValue())

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

        # mine = T0|T0 = 2, T0|T1 = 5, T1|T0 = 3, T1|T1 = 7
        # peer = T0|T0 = -1, T0|T1 = -2, T1|T0 = 4, T1|T1 = 6


'''
        (-1,2)   (-2,3)

        (4,5)     (6,7)

'''


def removeelementfrommine(mine):
    i = 0
    j = 0

    if "T0|T0" in mine:
        a = mine.split("T0|T0=[")
        b = a[1].split("]", 1)
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

    return [0, '', 0, 0]


def removeelementfrompeer(peer):
    i = 0
    j = 0

    if "T0|T0" in peer:
        a = peer.split("T0|T0=[")

        b = a[1].split("]", 1)
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

    return [0, '', 0, 0]


def putinthematrix(util1, x, i, j, m):
    if x[i][j] == 'x':
        x[i][j] = util1
    else:
        a = x[i][j]
        if isinstance(a, list):
            if (len(a) == 2):
                return x
        if (m == 'm'):
            x[i][j] = [a, util1]
        else:
            x[i][j] = [util1, a]
    return x


def common(minelist, peerlist):
    com = []
    for el in minelist:
        if el in peerlist:
            com.append(el)
    return com


def pickbest(a, matrix):
    max = -1000000000000
    maxindexes = []

    for el in a:
        i = el[0]
        j = el[1]
        value = (matrix[i][j][0]) + (matrix[i][j][1])

        if (value > max):
            max = value
            maxindexes = [i, j]

        elif (value == max):

            if j < maxindexes[1]:
                maxindexes = [i, j]

    return "mine=T" + str(maxindexes[1]) + ",peer=T" + str(maxindexes[0])


def decide_nash(matrix):
    minelist = findbestmine(matrix)
    maxofmine = max(minelist[1])
    indexofmaxmine = minelist[0][minelist[1].index(maxofmine)]
    peerlist = findbestpeer(matrix)

    a = common(minelist[0], peerlist[0])

    if a == []:
        return "blank-decision"

    if (len(a) == 1):
        return "mine=T" + str(a[0][1]) + ",peer=T" + str(a[0][0])

    task = pickbest(a, matrix)

    return task


def findbestmine(matrix):
    i = 0
    j = 0
    temp = [-100000000000000000000, -1000000000000000]
    tempvalues = []
    nashequilibria = []
    maxvalues = []

    while i != len(matrix):

        length = len(matrix[i])

        while j != length:
            if matrix[i][j][1] > temp[1]:
                temp = matrix[i][j]
                tempvalues = [i, j]
            j += 1

        sum = 0

        if tempvalues not in nashequilibria:
            for el in temp:
                sum += el
            maxvalues.append(sum)
            nashequilibria.append(tempvalues)

        temp = [-1000000000000000, -1000000000000]
        j = 0
        i += 1
    return [nashequilibria, maxvalues]


def findbestpeer(matrix):
    i = 0
    j = 0
    temp = [-100000000000000000000, -1000000000000000]
    tempvalues = []
    nashequilibria = []
    maxvalues = []

    length = len(matrix[0])

    while (j != length):
        while (i != len(matrix)):
            if matrix[i][j][0] >= temp[0]:
                temp = matrix[i][j]
                tempvalues = [i, j]

            i += 1
        sum = 0
        if tempvalues not in nashequilibria:
            for el in temp:
                sum += el
            maxvalues.append(sum)
            nashequilibria.append(tempvalues)

        temp = [-1000000000000000, -1000000000000]
        i = 0
        j += 1

    return [nashequilibria, maxvalues]


def decide_mixed(matrix):
    peervalues = getpeervalues(matrix)

    if (peervalues == "blank-decision"):
        return "blank-decision"

    "{0:.2f}".format(13.949999999999999)
    peervalues[0] = "{0:.2f}".format(float(peervalues[0]))
    peervalues[1] = "{0:.2f}".format(float(peervalues[1]))

    minevalues = getminevalues(matrix)

    if (minevalues == "blank-decision"):
        return "blank-decision"

    minevalues[0] = "{0:.2f}".format(float(minevalues[0]))
    minevalues[1] = "{0:.2f}".format(float(minevalues[1]))

    return "mine=(" + str(minevalues[0]) + "," + str(minevalues[1]) + "),peer=(" + str(peervalues[0]) + "," + str(
        peervalues[1]) + ")"


def getpeervalues(matrix):
    b1 = matrix[0][0][1]
    b2 = matrix[0][1][1]
    b3 = matrix[1][0][1]
    b4 = matrix[1][1][1]

    dividend = (b1 + b4 - b3 - b2)
    if dividend == 0:
        return "blank-decision"

    value = (b4 - b3) / (b1 + b4 - b3 - b2)

    if value > 1 or value < 0:
        return "blank-decision"
    else:
        return [value, 1 - value]


def getminevalues(matrix):
    a1 = matrix[0][0][0]
    a2 = matrix[0][1][0]
    a3 = matrix[1][0][0]
    a4 = matrix[1][1][0]

    dividend = (a1 - a2 - a3 + a4)
    if dividend == 0:
        return "blank-decision"

    value = (a4 - a2) / (a1 - a2 - a3 + a4)

    if value > 1 or value < 0:
        return "blank-decision"
    else:
        return [value, 1 - value]


args = sys.stdin.readline().split(' ')
agent = Agent(args[0], args[1])
size = 1 if len(args) <= 2 else int(args[2])

for i in range(0, size):
    if i != 0:
        agent.update(sys.stdin.readline())
    sys.stdout.write(agent.decide(args[0]) + '\n')
