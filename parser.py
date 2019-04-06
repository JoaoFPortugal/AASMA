import sys


class Agent:

    def __init__(self, state, task):
        self.state = state
        task = task[:-2]
        tasks = self.parse(task)
        self.listoftasks = self.findtasks(tasks)

    def update(self, observation):
        pass

    def decide(self, behavior):
        if (behavior == "decide-rational"):
            return decide_rational(self.listoftasks)
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


class Task:

    def __init__(self, name, task):
        self.name = name
        parsedtask = self.parseTask(task)
        self.value = parsedtask

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def parseTask(self, task):
        if self.name == "T1":
            return task[5:]
        else:
            return task[4:]


def decide_rational(listoftasks):
    max_utility = 0
    max_utility_task = ''

    utilitiesfound = []
    for t in listoftasks:
        utility = calculatetotalutility(t.getValue())
        utilitiesfound.append(utility)
        if max_utility < utility:
            max_utility = utility
            max_utility_task = t.getName();
    return max_utility_task


lst = []

'''
returns the inside symbols of task
ex T1 = (A=(30%,0),B=(70%,3)) returns a list first element is A=(30%,0) and 2nd is B=(70%,3)
'''


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
    contains = False
    if (len(one) != 1):
        two = one[1].split(',', 1)
    firstarg = two[0]
    secarg = two[1]

    if "%" in firstarg:
        contains = True
        firstarg = firstarg[:-1]
        firstvalue = float(firstarg) / 100
    else:
        firstvalue = float(firstarg)
        total += firstvalue

    try:
        if secarg[-1] == ')':
            secarg = secarg[:-1]
        secondvalue = float(secarg)


        if(contains):
            return firstvalue * secondvalue
        else:
            return firstvalue*secondvalue

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

    if total == 0:
        return totalutility

    else:
        return totalutility / total


args = sys.stdin.readline().split(' ')
agent = Agent(args[0], args[1])
size = 1 if len(args) <= 2 else int(args[2])

for i in range(0, size):
    if i != 0:
        agent.update(sys.stdin.readline())
    sys.stdout.write(agent.decide(args[0]) + '\n')
