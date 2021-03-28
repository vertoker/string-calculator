import math, re, sys

order_signs = {'+':1, '-':1, '*':2, '/':2, '^':3, '√':3, '!':4}
pos_types = {'+':0, '-':0, '*':0, '/':0, '^':0, '√':1, '!':2}
all_nums = '.1234567890'
all_operations = '+-*/^√!'
all_0_type_operations = '+-*/^'

def Factorial(num):
	if num < 0:
		return num
	elif num < 2:
		return 1
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

def Calculate(expression, saveconvert2int = True, convert2int = False):
	if expression == '':
		return 0

    # Format input
	expression = expression.replace(',', '.')
	expression = expression.replace(':', '/')
	expression = expression.replace('**', '^')

    # Start params
	length = len(expression)
	localNum = ''
	power = 0
	targetNum = 0
	nextError = False

    # Lists
	nums = []
	signs = []
	order = []
	target = []

    # Collect data and write lists
	for i in range(length):
		s = expression[i]
		isNum = False
		if s in all_operations:
			target.append(targetNum)
			if s in all_0_type_operations:
				targetNum += 1
			if i > 0:
				if s == '√' and expression[i - 1] in all_nums:
					signs.append('*')
					order.append(power)
					targetNum += 1
					target.append(targetNum)
			else:
				nextError = True

			signs.append(s)
			if s in '+*/^':
				order.append(power)
			elif s == '-':
				order.append(sys.maxsize)

			if i + 1 < length:
				if s == '!' and expression[i + 1] in all_nums:
					signs.append('*')
					order.append(power)
					target.append(targetNum)
					targetNum += 1
				if expression[i + 1] in all_0_type_operations:
					nextError = True
			else:
				nextError = True
		elif s == '(':
			if localNum != '':
				signs.append('*')
				order.append(power)
				target.append(targetNum)
				targetNum += 1
			if i + 1 < length:
				if expression[i + 1] in all_0_type_operations:
					nextError = True
			power += 1
		elif s == ')':
			if i + 1 < length:
				if expression[i + 1] in all_nums:
					signs.append('*')
					order.append(power)
					target.append(targetNum)
					targetNum += 1
			power -= 1
		else:
			localNum += s
			isNum = True

		if not isNum:
			if localNum != '' and localNum != '-':
				nums.append(localNum)
				localNum = ''
		if nextError:
			nums.append('0')
			nextError = False

		# Logs
		'''print(nums)
		print(targetNum)
		print(localNum)
		print()'''

	# Checkout on error and add last num
	if localNum != '' and localNum != '-':
		nums.append(localNum)
	if nextError:
		nums.append('0')
		nextError = False

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
			if n in all_nums or n == '-':
				localNum += n
			elif localNum != '':
				multiplier *= float(localNum)
				localNum = ''

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
		# Logs
		'''print(nums)
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
			nums[target[nextID]] = Operation(signs[nextID], 0, nums[target[nextID]])
			if target[nextID] + 1 < len(nums) and len(signs) < len(nums):
				nums[target[nextID]] = Operation('*', nums[target[nextID]], nums[target[nextID] + 1])
				nums.pop(target[nextID] + 1)
			signs.pop(nextID)
			order.pop(nextID)
			last = target.pop(nextID)
		elif pos_type == 2:
			nums[target[nextID]] = Operation(signs[nextID], nums[target[nextID]], 0)
			signs.pop(nextID)
			order.pop(nextID)
			last = target.pop(nextID)
	if (nums[0] % 1 == 0 and saveconvert2int) or convert2int:
		return int(nums[0])
	return nums[0]

def Equals(expression):
	expressions = expression.split('=')
	nums = []
	for exp in expressions:
		nums.append(Calculate(exp))

	localNum = nums[0]
	for i in range(1, len(nums)):
		if localNum != nums[i]:
			return False
	return True
