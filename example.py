from calculator import *

answer, warnings, errors = Calculate(input('Input expression: '), returnWarning = True, returnError = True)
print('\nAnswer equals: ', str(answer))
print('\nAll warnings')
for warning in warnings:
    print(warning)
print('\nAll errors')
for error in errors:
    print(error)
