from calculator import *

typeofOutput = 1

print('1 - standard')
print('2 - only warnings')
print('3 - only errors')
print('4 - full')
typeofOutput = input('Enter type of output: ')

if typeofOutput == '1' or typeofOutput == '':
    print('\nAnswer equals ', str(Calculate(input('Input expression: '))))
elif typeofOutput == '2':
    answer = Calculate(input('Input expression: '), returnWarning = True)
    print('\nAnswer equals ', str(answer[0]))
    print('\nAll warnings')
    for warning in answer[1]:
        print(warning)
elif typeofOutput == '3':
    answer = Calculate(input('Input expression: '), returnError = True)
    print('\nAnswer equals ', str(answer[0]))
    print('\nAll errors')
    for error in answer[1]:
        print(error)
elif typeofOutput == '4':
    answer = Calculate(input('Input expression: '), returnWarning = True, returnError = True)
    print('\nAnswer equals ', str(answer[0]))
    print('\nAll warnings')
    for warning in answer[1]:
        print(warning)
    print('\nAll errors')
    for error in answer[2]:
        print(error)
