from calculator import *

answer = Calculate(input('Input expression: '), returnWarning = True, returnError = True)
print('\nAnswer equals: ', str(answer[0]))
print('\nAll warnings')
for warning in answer[1]:
    print(warning)
print('\nAll errors')
for error in answer[2]:
    print(error)
