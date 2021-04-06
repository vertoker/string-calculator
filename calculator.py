import math, re

order_signs = {'+':1, '-':1, '*':2, '/':2, '^':3, '√':3, '!':4}
pos_types = {'+':0, '-':0, '*':0, '/':0, '^':0, '√':1, '!':2}
all_nums_constants = '.1234567890epi'
all_nums = '.1234567890'
all_operations = '+-*/^√!'

def Factorial(num):
	if num < 2:
		return 1
	else:
		return num * Factorial(num - 1)

def Operation(sign, num1, num2):
	if sign == '+':
		return num1 + num2, False
	elif sign == '-':
		return num1 - num2, False
	elif sign == '*':
		return num1 * num2, False
	elif sign == '/':
		if num2 == 0:
			return 0, True
		return num1 / num2, False
	elif sign == '^':
		return math.pow(num1, num2), False
	elif sign == '!':
		if num1 < 0:
			return 0, True
		return Factorial(int(num1)), False
	elif sign == '√':
		if num2 < 0:
			return 0, True
		return math.sqrt(abs(num2)), False
	return 0, True

def SpecialReturn(num, warning, warningPermission, error, errorPermission):
	if warningPermission:
		if errorPermission:
			return num, warning, error
		return num, warning
	if errorPermission:
		return num, error
	return num

def Calculate(expression, saveconvert2int = True, returnWarning = False, returnError = False, convert2int = False):
	if expression == '':
		return SpecialReturn(0, True, returnWarning, False, returnError)

    # Format input
	expression = expression.replace(',', '.')
	expression = expression.replace(':', '/')
	expression = expression.replace('**', '^')

    # Temporarity params
	length = len(expression)
	localNum = ''
	power = 0
	targetNum = 0
	nextError = 0

    # Lists and stuff (all return params)
	globalError = False
	nums = []
	signs = []
	order = []
	target = []

    # Collect data and write lists
	for i in range(length):
		s = expression[i]
		isNum = False
		notFirstChar = i > 0
		notLastChar = i + 1 < length

		if s in '+-*/^':
			target.append(targetNum)
			targetNum += 1

			if notFirstChar:
				if not expression[i - 1] in all_nums_constants and not expression[i - 1] in '!)':
					nextError += 1
			else:
				nextError += 1

			if notLastChar:
				if not expression[i + 1] in all_nums_constants and not expression[i + 1] in '√(':
					nextError += 1
			else:
				nextError += 1

			signs.append(s)
			order.append(power)
		elif s == '!':
			target.append(targetNum)
			signs.append(s)
			order.append(power)

			if notFirstChar:
				if not expression[i - 1] in all_nums_constants and not expression[i - 1] in '!)':
					nextError += 1
			else:
				nextError += 1
			if notLastChar:
				if expression[i + 1] in all_nums_constants:
					globalError = True
					signs.append('*')
					order.append(power)
					target.append(targetNum)
					targetNum += 1
		elif s == '√':
			target.append(targetNum)

			if notFirstChar:
				if expression[i - 1] in all_nums_constants:
					globalError = True
					signs.append('*')
					order.append(power)
					targetNum += 1
					target.append(targetNum)
			if notLastChar:
				if not expression[i + 1] in all_nums_constants and not expression[i + 1] in '√(':
					nextError += 1
			else:
				nextError += 1

			signs.append(s)
			order.append(power)
		elif s == '(':
			if notFirstChar:
				if expression[i - 1] in all_nums_constants:
					globalError = True
					signs.append('*')
					order.append(power)
					target.append(targetNum)
					targetNum += 1
			if not notLastChar:
				nextError += 1
			power += 1
		elif s == ')':
			power -= 1
			if notFirstChar:
				if expression[i - 1] == '(':
					nextError += 1
			else:
				nextError += 1
			if notLastChar:
				if expression[i + 1] in all_nums_constants:
					globalError = True
					signs.append('*')
					order.append(power)
					target.append(targetNum)
					targetNum += 1
		else:
			localNum += s
			isNum = True

		if not isNum:
			if localNum != '' and localNum != '-':
				nums.append(localNum)
				localNum = ''
		if nextError > 0:
			globalError = True
			for i in range(nextError):
				nums.append('0')
			nextError = 0

		# Logs
		#print(nums, targetNum, localNum, sep = '\n')

	# Checkout on error and other
	if localNum != '' and localNum != '-':
		nums.append(localNum)
	if nextError > 0:
		globalError = True
		for i in range(nextError):
			nums.append('0')
		nextError = 0
	if power != 0:
		globalError = True
	if len(nums) == 0:
		return SpecialReturn(0, True, returnWarning, False, returnError)

	# Clean numbers and find constants
	for i in range(len(nums)):
		num = nums[i]
		multiplier = 1
		localNum = ''
		hasPoint = False
		hasNums = False

		if 'pi' in num:
			multiplier *= pow(math.pi, len(re.findall('pi', num)))
			num = num.replace('pi', '+')
			hasNums = True
		if 'e' in num:
			multiplier *= pow(math.e, len(re.findall('e', num)))
			num = num.replace('e', '+')
			hasNums = True

		for n in num:
			if n in '1234567890':
				localNum += n
				hasNums = True
			elif n == '.':
				if not hasPoint:
					hasPoint = True
					localNum += n
					hasNums = True
			else:
				if localNum != '':
					if localNum[0] == '.':
						localNum = '0' + localNum
					if localNum[-1] == '.':
						localNum = localNum + '0'
					multiplier *= float(localNum)
					localNum = ''
				if n != '+':
					globalError = True

		if localNum != '':
			if localNum[0] == '.':
				localNum = '0' + localNum
			if localNum[-1] == '.':
				localNum = localNum + '0'
			multiplier *= float(localNum)
		nums[i] = multiplier * hasNums

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
		print(nums, signs, order, target, sep = '\n')
		pos_type = pos_types[signs[nextID]]
		if pos_type == 0:
			nums[target[nextID]], error = Operation(signs[nextID], nums[target[nextID]], nums[target[nextID] + 1])
			if error:
				return SpecialReturn(0, globalError, returnWarning, error, returnError)
			signs.pop(nextID)
			order.pop(nextID)
			nums.pop(target[nextID] + 1)
			last = target.pop(nextID)
			for i in range(len(target)):
				if target[i] > last:
					target[i] -= 1
		elif pos_type == 1:# √
			nums[target[nextID]], error = Operation(signs[nextID], 0, nums[target[nextID]])
			if error:
				return SpecialReturn(0, globalError, returnWarning, error, returnError)
			if target[nextID] + 1 < len(nums) and len(signs) < len(nums):
				nums[target[nextID]] = Operation('*', nums[target[nextID]], nums[target[nextID] + 1])
				nums.pop(target[nextID] + 1)
			signs.pop(nextID)
			order.pop(nextID)
			last = target.pop(nextID)
		elif pos_type == 2:
			nums[target[nextID]], error = Operation(signs[nextID], nums[target[nextID]], 0)
			if error:
				return SpecialReturn(0, globalError, returnWarning, error, returnError)
			signs.pop(nextID)
			order.pop(nextID)
			last = target.pop(nextID)
	if (nums[0] % 1 == 0 and saveconvert2int) or convert2int:
		return SpecialReturn(int(nums[0]), globalError, returnWarning, False, returnError)
	return SpecialReturn(nums[0], globalError, returnWarning, False, returnError)

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
