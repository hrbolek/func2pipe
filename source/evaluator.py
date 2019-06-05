import re


def is_number_tryexcept(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def compile_expression(expr):
    print(expr)
    regTesterA = '^([a-zA-Z0-9_]+)((?:==)|(?:>=)|(?:=<)|(?:<)|(?:>))((?:[0-9]+)|(?:"[^"]+"))$'
    match = re.findall(regTesterA, expr)
    leftname = match[0][0]
    rightvalue = match[0][2]
    print(leftname, '?', rightvalue)
    r = 0
    if ('"' in rightvalue):
        r = rightvalue[1:-1]
    else:
        r = int(rightvalue)

    def result_eq(callforvar):
        leftvalue = callforvar(leftname)
        return leftvalue == r

    def result_le(callforvar):
        leftvalue = callforvar(leftname)
        return leftvalue <= r

    def result_lt(callforvar):
        leftvalue = callforvar(leftname)
        return leftvalue < r

    def result_ge(callforvar):
        leftvalue = callforvar(leftname)
        return leftvalue >= r

    def result_gt(callforvar):
        leftvalue = callforvar(leftname)
        return leftvalue > r

    result = {
        '==' : result_eq,
        '>=' : result_ge,
        '=<' : result_le,
        '>' : result_gt,
        '<' : result_lt,
        }
    return result[match[0][1]]


def compile_expression2(expr):
    reg = '((?:\*)|(?:[+-/<>])|(?:=<)|(?:==)|(?:=>)|(?:[A-Za-z_][A-Za-z0-9_]+)|(?:"[^"]+")|(?:True)|(?:False)|(?:[0-9]+\.[0-9]+))'
    tokens = re.compile(reg).split(expr)
    
    stackop = []
    stackla = []

    def Mul():
        pass
    def Div():
        pass
    def Add():
        pass
    def Sub():
        pass
    def Le():
        pass
    def Lt():
        pass
    def Ge():
        pass
    def Gt():
        pass
    def Eq():
        pass
    def Number(token): 
        def result(data):
            return None#float(token)
        return result
    def String(token):
        def result(data):
            return token
        return result
    def Var(token):
        def result(data):
            return data[token]
        return result

    operatorslambdas = {
        '<' : {'l': lambda left, right: lambda data: left(data) < right(data), 'priority': 0},
        '=<' : {'l': lambda left, right: lambda data: left(data) <= right(data), 'priority': 0},
        '==' : {'l': lambda left, right: lambda data: left(data) == right(data), 'priority': 0},
        '>' : {'l': lambda left, right: lambda data: left(data) > right(data), 'priority': 0},
        '=>' : {'l': lambda left, right: lambda data: left(data) >= right(data), 'priority': 0},
        '+' : {'l': lambda left, right: lambda data: left(data) + right(data), 'priority': 2},
        '-' : {'l': lambda left, right: lambda data: left(data) - right(data), 'priority': 2},
        '*' : {'l': lambda left, right: lambda data: left(data) * right(data), 'priority': 1},
        '/' : {'l': lambda left, right: lambda data: left(data) / right(data), 'priority': 1},
                        }

    operators = '(^(?:\*)|(?:[+-/<>])|(?:=<)|(?:==)|(?:=>)$)'
    operands = '(^(?:[A-Za-z_][A-Za-z0-9_]+)|(?:"[^"]+")|(?:True)|(?:False)|(?:[0-9]+\.[0-9]+)$)'
    reoperators = re.compile(operators)
    reoperands = re.compile(operands)
    for token in tokens:
        current = {}
        if (not reoperands.fullmatch(token) == None):
            lambdaop = lambda data: True
            if (token == 'True'):
                lambdaop = lambda data: True
            elif (token == 'False'):
                lambdaop = lambda data: False
            elif (token[0] in '0123456789'):
                lambdaop = Number(token)
            elif (token[0] == '"'):
                lambdaop = String(token)
            else:
                lambdaop = Var(token)
            while ((len(stackop) > 1)):
                previtem = stackop[-2]
                lastitem = stackop[-1]#['priority']
                if (lastitem['priority'] < previtem['priority']):
                    pass 
            stackla.append(lambdaop)
        elif (not reoperators.fullmatch(token) == None):
            current = operatorslambdas[token]
            pass



    return None


