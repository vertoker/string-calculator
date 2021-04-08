from calculator import *

answer, warnings, errors = CalculateLog(input('Input expression: '))
print('\nAnswer equals: ', str(answer))
print('\nAll warnings')
for warning in warnings:
    print(warning)
print('\nAll errors')
for error in errors:
    print(error)

#print(Calculate(input('\nInput expression: ')))
