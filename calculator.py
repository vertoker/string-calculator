import math, re
from sys import float_info

errors = {
'pluslarge':'The plus is too large to calculate',
'minuslarge':'The minus is too large to calculate',
'multiplylarge':'The multiply is too large to calculate',
'divisionlarge':'The division is too large to calculate',
'div0':'Can not be divided by zero',
'degreelarge':'The degree is too large to calculate',
'factminus':'Сan not calculate a factorial from a negative number',
'factlarge':'The factorial is too large to calculate',
'sqrtminus':'Сan not calculate the square root from a negative number'
}
warnings = {
'null':'Expression is empty',
'skipmultiply':'Skipped multiplication sign',
'skipnumber':'Skipped number between/nearby sign(s)',
'openparenthesis':'There is an extra open parenthesis',
'closedparenthesis':'There is an extra closed parenthesis',
'additionalpoint':'There is an extra dot in the number',
'additionalsymbol':'There is an extra symbol in the expression, which not used in computation',
'nonums':'You broke real error protection. How?'
}

order_signs = {'+':1, '-':1, '*':2, '/':2, '^':3, '√':4, '!':5}
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
		try:
			return num1 + num2, ''
		except:
			return 0, errors['pluslarge']
	elif sign == '-':
		try:
			return num1 - num2, ''
		except:
			return 0, errors['minuslarge']
	elif sign == '*':
		try:
			return num1 * num2, ''
		except:
			return 0, errors['multiplylarge']
	elif sign == '/':
		if num2 == 0:
			return 0, errors['div0']
		try:
			return num1 / num2, ''
		except:
			return 0, errors['divisionlarge']
	elif sign == '^':
		try:
			return math.pow(num1, num2), ''
		except:
			return 0, errors['degreelarge']
	elif sign == '!':
		if num1 < 0:
			return 0, errors['factminus']
		try:
			return Factorial(int(num1)), ''
		except:
			return 0, errors['factlarge']
	elif sign == '√':
		if num2 < 0:
			return 0, errors['sqrtminus']
		try:
			return math.sqrt(num2), ''
		except:
			return 0, errors['sqrtlarge']
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
		return SpecialReturn(0, [warnings['null']], returnWarning, [], returnError)

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
	globalWarnings = []
	globalErrors = []
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
					if not warnings['skipmultiply'] in globalWarnings:
						globalWarnings.append(warnings['skipmultiply'])
					signs.append('*')
					order.append(power)
					target.append(targetNum)
					targetNum += 1
		elif s == '√':
			target.append(targetNum)

			if notFirstChar:
				if expression[i - 1] in all_nums_constants:
					if not warnings['skipmultiply'] in globalWarnings:
						globalWarnings.append(warnings['skipmultiply'])
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
					if not warnings['skipmultiply'] in globalWarnings:
						globalWarnings.append(warnings['skipmultiply'])
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
					if not warnings['skipmultiply'] in globalWarnings:
						globalWarnings.append(warnings['skipmultiply'])
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
			if not warnings['skipnumber'] in globalWarnings:
				globalWarnings.append(warnings['skipnumber'])
			for i in range(nextError):
				nums.append('0')
			nextError = 0

		# Logs
		#print(nums, targetNum, localNum, sep = '\n')

	# Checkout on error and other
	if localNum != '' and localNum != '-':
		nums.append(localNum)
	if nextError > 0:
		if not warnings['skipnumber'] in globalWarnings:
			globalWarnings.append(warnings['skipnumber'])
		for i in range(nextError):
			nums.append('0')
		nextError = 0
	if power > 0:
		globalWarnings.append(warnings['openparenthesis'])
	if power < 0:
		globalWarnings.append(warnings['closedparenthesis'])
	if len(nums) == 0:
		globalErrors.append(errors['nonums'])
		return SpecialReturn(0, globalWarnings, returnWarning, globalErrors, returnError)

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
					if warnings['additionalpoint'] in globalWarnings:
						globalWarnings.append(warnings['additionalpoint'])
			else:
				if localNum != '':
					if localNum[0] == '.':
						localNum = '0' + localNum
					if localNum[-1] == '.':
						localNum = localNum + '0'
					multiplier *= float(localNum)
					localNum = ''
				if n != '+' and not warnings['additionalsymbol'] in globalWarnings:
					globalWarnings.append(warnings['additionalsymbol'])

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
			localOrder = order[y]
			localPower = order_signs[signs[y]]
			orderPriority = signOrder < localOrder
			signPriority = signPower < localPower
			degreePriority = signPower == order_signs['^'] and localPower == order_signs['^']
			if orderPriority or signOrder == localOrder and (signPriority or degreePriority):
				nextID = y
				signPower = localPower
				signOrder = localOrder
		# Logs
		#print(nums, signs, order, target, sep = '\n')
		pos_type = pos_types[signs[nextID]]
		if pos_type == 0:
			nums[target[nextID]], error = Operation(signs[nextID], nums[target[nextID]], nums[target[nextID] + 1])
			if not error in globalErrors:
				globalErrors.append(error)
			signs.pop(nextID)
			order.pop(nextID)
			nums.pop(target[nextID] + 1)
			last = target.pop(nextID)
			for i in range(len(target)):
				if target[i] > last:
					target[i] -= 1
		elif pos_type == 1:# √
			nums[target[nextID]], error = Operation(signs[nextID], 0, nums[target[nextID]])
			if not error in globalErrors:
				globalErrors.append(error)
			if target[nextID] + 1 < len(nums) and len(signs) < len(nums):
				nums[target[nextID]] = Operation('*', nums[target[nextID]], nums[target[nextID] + 1])
				nums.pop(target[nextID] + 1)
			signs.pop(nextID)
			order.pop(nextID)
			last = target.pop(nextID)
		elif pos_type == 2:
			nums[target[nextID]], error = Operation(signs[nextID], nums[target[nextID]], 0)
			if not error in globalErrors:
				globalErrors.append(error)
			signs.pop(nextID)
			order.pop(nextID)
			last = target.pop(nextID)
	if (nums[0] % 1 == 0 and saveconvert2int) or convert2int:
		return SpecialReturn(int(nums[0]), globalWarnings, returnWarning, globalErrors, returnError)
	return SpecialReturn(nums[0], globalWarnings, returnWarning, globalErrors, returnError)

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
