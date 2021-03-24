import math, re

order_signs = {'+':1, '-':1, '*':2, '/':2, '^':3, '√':3, '!':4}
pos_types = {'+':0, '-':0, '*':0, '/':0, '^':0, '√':1, '!':2}
alphabet = 'abcdefghijklmnopqrstuvwxyz'
all_nums = '.1234567890'

def input_float(comment):
    try:
        num = input(comment)
        return float(num)
    except:
        return input_float(comment)

def Factorial(num):
    if num < 2:
        return num
    else:
        return num * Factorial(num - 1)

def Operation(sign, num1, num2):
    if sign == '+':
        return num1 + num2
    elif sign == '-':
        return num1 - num2
    elif sign == '*':
        return num1 * num2
    elif sign == '/':
        return num1 / num2
    elif sign == '^':
        return math.pow(num1, num2)
    elif sign == '!':
        return Factorial(int(num1))
    elif sign == '√':
        if num2 < 0:
            return -math.sqrt(-num2)
        else:
            return math.sqrt(num2)
    return 0

def Calculate(expression):
    # Format input
    expression = expression.replace(',', '.')
    expression = expression.replace(':', '/')
    expression = expression.replace('**', '^')

    # Start params
    length = len(expression)
    localNum = ''
    power = 0
    targetNum = 0
    
    # Lists
    nums = []
    signs = []
    order = []
    target = []
    
    # Collect data and write lists
    for i in range(length):
        s = expression[i]
        isNum = False
        if s in all_nums or s in alphabet:
            localNum += s
            isNum = True
        elif s == '-':
            if len(signs) == 0:
                if localNum == '':
                    localNum += s
                    isNum = True
                else:
                    signs.append(s)
                    order.append(power)
                    target.append(targetNum)
                    targetNum += 1
            elif localNum == '' and signs[-1] != '!':
                localNum += s
                isNum = True
            else:
                signs.append(s)
                order.append(power)
                target.append(targetNum)
                targetNum += 1
        elif s in '+*/:^!√':
            target.append(targetNum)
            if s in '+*/:^':
                targetNum += 1
            if i > 0:
                if s == '√' and expression[i - 1] in all_nums:
                    signs.append('*')
                    order.append(power)
                    targetNum += 1
                    target.append(targetNum)
            signs.append(s)
            order.append(power)
            if i + 1 < length:
                if s == '!' and expression[i + 1] in all_nums:
                    signs.append('*')
                    order.append(power)
                    target.append(targetNum)
                    targetNum += 1

        elif s == '(':
            if localNum != '':
                signs.append('*')
                order.append(power)
                target.append(targetNum)
                targetNum += 1
            power += 1
        elif s == ')':
            if i + 1 < length:
                if expression[i + 1] in all_nums:
                    signs.append('*')
                    order.append(power)
                    target.append(targetNum)
                    targetNum += 1
            power -= 1
        if not isNum and localNum != '' and localNum != '-':
            nums.append(localNum)
            localNum = ''
    if localNum != '' and localNum != '-':
        nums.append(localNum)

    # Clean numbers and find constants
    for i in range(len(nums)):
        num = nums[i]
        multiplier = 1
        localNum = ''
        
        if 'pi' in num:
            multiplier *= pow(math.pi, len(re.findall('pi', num)))
            num = num.replace('pi', '?')
        if 'e' in num:
            multiplier *= pow(math.e, len(re.findall('e', num)))
            num = num.replace('e', '?')
        
        for n in num:
            if (n in alphabet or n == '?') and localNum != '':
                multiplier *= float(localNum)
                localNum = ''
            elif n != '?':
                localNum += n
        if localNum != '':
            multiplier *= float(localNum)
        nums[i] = multiplier
    
    # Calculate
    for x in range(len(signs)):
        nextID = 0
        signPower = order_signs[signs[0]]
        signOrder = order[0]
        for y in range(1, len(signs)):
            localPower = order_signs[signs[y]]
            localOrder = order[y]
            if signOrder < localOrder or (signOrder == localOrder and signPower < localPower):
                nextID = y
                signPower = localPower
                signOrder = localOrder
        '''# Logs
        print(nums)
        print(signs)
        print(order)
        print(target)'''
        pos_type = pos_types[signs[nextID]]
        if pos_type == 0:
            nums[target[nextID]] = Operation(signs[nextID], nums[target[nextID]], nums[target[nextID] + 1])
            signs.pop(nextID)
            order.pop(nextID)
            nums.pop(target[nextID] + 1)
            last = target.pop(nextID)
            for i in range(len(target)):
                if target[i] > last:
                    target[i] -= 1
        elif pos_type == 1:# √
            if target[nextID] + 1 < len(nums):
                nums[target[nextID] + 1] = Operation(signs[nextID], 0, nums[target[nextID] + 1])
                if len(signs) < len(nums):
                    nums[target[nextID]] = Operation('*', nums[target[nextID]], nums[target[nextID] + 1])
                    nums.pop(target[nextID] + 1)
            else:
                nums[target[nextID]] = Operation(signs[nextID], 0, nums[target[nextID]])
            signs.pop(nextID)
            order.pop(nextID)
            last = target.pop(nextID)
            for i in range(len(target)):
                if target[i] > last:
                    target[i] -= 1
        elif pos_type == 2:
            nums[target[nextID]] = Operation(signs[nextID], nums[target[nextID]], 0)
            signs.pop(nextID)
            order.pop(nextID)
            last = target.pop(nextID)
            for i in range(len(target)):
                if target[i] > last:
                    target[i] -= 1
    return nums[0]

print(Calculate(input('Input expression: ')))