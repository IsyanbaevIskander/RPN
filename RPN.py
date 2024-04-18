from math import *


def is_constant(word):
    if word in ('pi', 'e'):
        return True


def is_operator(word):
    if word in ('sqrt', 'cos', 'sin', 'ln'):
        return True


def is_combo(word):
    arr = ('pi', 'e', 'sqrt', 'cos', 'sin', 'ln')
    buffer = []
    curr_word = ''
    index = 0
    while index < len(word):
        while curr_word not in arr and index < len(word):
            curr_word += word[index]
            index += 1
        if curr_word in arr:
            buffer.append(curr_word)
            curr_word = ''
    if curr_word not in arr and curr_word != '':
        return 'Wrong expression'
    return buffer

def infix_to_postfix(expr):
    priority = {'+': 0, '-': 0, '*': 1, '/': 1, '~': 2, '^': 3, 'ln': 4, 'sqrt': 4, 'sin': 4, 'cos': 4, '(': -1}
    is_unary = True
    operators = []  # stack
    values = []     # queue
    i = 0

    while i < len(expr):
        if expr[i] == ' ':                  # обработка пробела
            i += 1
            continue
        elif expr[i] in '1234567890':       # считывание чисел
            j = i
            while j < len(expr) and (expr[j] in '1234567890' or expr[j] == '.'):
                j += 1
            values.append(float(expr[i:j]))
            i = j
            is_unary = False
            continue
        elif expr[i] == '(':                # обработка открывающей скобки
            is_unary = True
            operators.append(expr[i])
        elif expr[i] in '+-*/^':            # обработка операторов +-*/^
            if is_unary:                    # обработка унарного + и -
                if expr[i] == '+':
                    i += 1
                    continue
                elif expr[i] == '-':
                    if len(operators) == 0 or priority['~'] > priority[operators[-1]]:
                        operators.append('~')
                    else:
                        while len(operators) > 0 and priority['~'] <= priority[operators[-1]]:
                            values.append(operators[-1])
                            operators.pop(-1)
                        operators.append('~')
                    i += 1
                    continue

            if len(operators) > 0 and expr[i] == '^' and operators[-1] == '^':          # частный случай с последовательным возведением
                operators.append(expr[i])
                i += 1
                continue

            if len(operators) == 0 or priority[expr[i]] > priority[operators[-1]]:      # обработка бинарных операторов, кроме ^
                operators.append(expr[i])
            else:
                while len(operators) > 0 and priority[expr[i]] <= priority[operators[-1]]:
                    values.append(operators[-1])
                    operators.pop(-1)
                operators.append(expr[i])
            is_unary = True

        elif expr[i].isalpha():
            j = i
            while j < len(expr) and expr[j].isalpha():
                j += 1

            if is_constant(expr[i:j]):
                if expr[i:j] == 'pi':
                    values.append(pi)
                else:
                    values.append(e)
                i = j
                continue
            elif is_operator(expr[i:j]):
                curr_operator = expr[i:j]
                operators.append(curr_operator)
                i = j
                is_unary = True
                continue
            elif is_combo(expr[i:j]) == 'Wrong expression':
                return 'Wrong expression'
            else:
                buff = is_combo(expr[i:j])
                for i in buff:
                    if is_constant(i):
                        if i == 'pi':
                            values.append(pi)
                        else:
                            values.append(e)
                    elif is_operator(i):
                        operators.append(i)
                i = j
                continue

        elif expr[i] == ')':
            if len(operators) == 0:
                return 'Wrong expression'               # добавить условие в calculation()
            while operators[-1] != '(':
                values.append(operators[-1])
                operators.pop(-1)
            operators.pop(-1)
        i += 1

    while len(operators):
        values.append(operators[-1])
        operators.pop(-1)
    return values


def calculation(expr):
    postfix_expr = infix_to_postfix(expr)
    if postfix_expr == 'Wrong expression':
        return postfix_expr
    stack = []
    for i in postfix_expr:
        if type(i) is float:
            stack.append(i)
        elif i == '~':
            if len(stack) == 0:
                return 'Wrong expression'
            stack[-1] = -stack[-1]
        elif i == '+':
            if len(stack) < 2:
                return 'Wrong expression'
            curr_ans = stack[-2] + stack[-1]
            stack[-2] = curr_ans
            stack.pop(-1)
        elif i == '-':
            if len(stack) < 2:
                return 'Wrong expression'
            curr_ans = stack[-2] - stack[-1]
            stack[-2] = curr_ans
            stack.pop(-1)
        elif i == '*':
            if len(stack) < 2:
                return 'Wrong expression'
            curr_ans = stack[-2] * stack[-1]
            stack[-2] = curr_ans
            stack.pop(-1)
        elif i == '/':
            if len(stack) < 2:
                return 'Wrong expression'
            if stack[-1] == 0:
                return 'Zero division'
            curr_ans = stack[-2] / stack[-1]
            stack[-2] = curr_ans
            stack.pop(-1)
        elif i == '^':
            if len(stack) < 2:
                return 'Wrong expression'
            curr_ans = stack[-2] ** stack[-1]
            stack[-2] = curr_ans
            stack.pop(-1)
        elif i == 'ln':
            if len(stack) == 0:
                return 'Wrong expression'
            if stack[-1] <= 0:
                return 'Bad value for logarithm'
            stack[-1] = log(stack[-1])
        elif i == 'cos':
            if len(stack) == 0:
                return 'Wrong expression'
            stack[-1] = cos(stack[-1])
        elif i == 'sin':
            if len(stack) == 0:
                return 'Wrong expression'
            stack[-1] = sin(stack[-1])
        elif i == 'sqrt':
            if len(stack) == 0:
                return 'Wrong expression'
            if stack[-1] < 0:
                return 'Bad value for square root'
            stack[-1] = sqrt(stack[-1])
        else:
            return 'Wrong expression'
    return stack

def post_and_calc(expr):
    print(expr)
    print(infix_to_postfix(expr))
    print(calculation(expr))
    print()

post_and_calc('----1')
post_and_calc('-(-(-(-1)))')
post_and_calc('2^2^3')
post_and_calc('(-sin(-cos(0)))')
post_and_calc('1/0')
post_and_calc('2+2*2')
post_and_calc('100-20-5')
post_and_calc('((2-3*3)+2*(-3))/(-2)+sin(-cos(0))')
post_and_calc('(10+2/(1-1))*3-3')
post_and_calc('(2^2)^3')
post_and_calc('2^sin1.5')
post_and_calc('(-1))')
post_and_calc('3 * ln5  * 10^sin3-3 / (cos7 + ln(7)) + 11.3 * cos(3)^3.5')
print(3 * log(5) * 10**sin(3)-3 / (cos(7) + log(7)) + 11.3 * cos(3)**3.5)
print()
post_and_calc('ln3')
post_and_calc('lncossine')
