
import io
import os
import re

from evaluator import compile_expression 


def compile_template(template):

    regexTester = re.compile(r'((?:\[\[)(?:[A-Z]+)(?:\:(?:[a-z_A-Z0-9]*))?(?:\((?:[^\)]*)\))?(?:\]\]))')
#    last = 0
#    for match in regexTester.finditer(template):
#        yield match
    templatelist = regexTester.split(template)
#    for item in templatelist:
#        print(item[0:25])

    regexTester = re.compile(r'(?:\[\[)([A-Z]+)(?:\:([a-z_A-Z0-9]*))?(?:\(([^\)]*)\))?(?:\]\])')
#    lnames = []
    types = []
    result = []
    index = -1
    deep = 0

    def hardprinter(item):
        def result(printer, data):
            printer(item)
            return data
        return result

    def uuesc(data):
        result = ''
        for c in str(data):
            code = ord(c)
            if (code > 127):
                result += '\\u' + str(code)+ '?'
            else:
                result += c
        return result

    def softprinter(name):
        def result(printer, data):
            #print('softprinter enter', '|'+name+'|', str(data)[0:200])
            #print('softprinter enter', 'len', str(data[0])[0:200])
            #print(data[name].encode('unicode_escape').decode('ansi'))
            if name in data:
                printer(uuesc(data[name]))#.encode('unicode_escape').decode('ansi'))
            else:
                print('Error on field ', name)
#            printer(data[name].encode('unicode_escape').decode('ansi'))
#            print('softprinter leave')
            return data
        return result

    def subroutine(funclist, iflambda = lambda data: True):
        #print('subroutine on', str(funclist))
        def result(printer, data):
            #print('subroutine enter', str(data))
            if (iflambda(data)):
                subdata = data
                for f in funclist:
                    subdata = f(printer, subdata)
            #print('subroutine leave', str(data))
            return data
        return result

    def iterator(funclist, iflambda = lambda data: True):
        #print('iterator on', str(funclist))
        def result(printer, data):
            #print('iterator enter', str(data))
            for item in data:
                #print('iterator item', str(item))
                if (iflambda(item)):
                    for f in funclist:
                        f(printer, item)
            #print('iterator leave')
            return data
        return result

    def select(name):
        def result(printer, data):
            #print('select enter', str(data), name)
            #print('select leave', str(data[name])[0:200], name)
            #print('select leave', str(data[name]), name)
            return data[name]
        return result

    def filterit(filterfunc = lambda data: True):
        def result(printer, data):
            return filter(filterfunc, data)
        return result

    def agregate(itemname, funcname):
        def sum(data):
            result = 0
            for item in data:
                result += item[itemname]
            return str(result)

        def count(data):
            result = 0
            for item in data:
                result += 1
            return str(result)

        func = sum
        if (funcname == 'count'):
            func = count

        def result(printer, data):
            value = func(data)
            printer(value)
        return result

    def createtester(expression):
        compiledexpr = compile_expression(expression)
        def evaluate(data):
            def callforvalue(name):
                return data[name]
            return compiledexpr(callforvalue)
        return evaluate

    while (index < len(templatelist) - 1):
        index += 1
        item = templatelist[index]
        match = regexTester.match(item)
        if (match == None):
            result.append((index, deep, 'O', item[0:10], hardprinter(item)))
        elif (match.group(1) == 'W'):
            types += ['W']
            deep += 1

            iflambda = lambda data: True
            if (not match.group(3) == None):
                iflambda = createtester(match.group(3))
            result.append((index, deep, 'W', match.group(2), select(match.group(2)), iflambda))

        elif (match.group(1) == 'ITERATE'):
            types += ['F']
            deep += 1
            result.append((index, deep, 'ITERATE', '', lambda printer, data: data, lambda data: True))
        elif (match.group(1) == 'F'):
            types += ['F']
            deep += 1

            iflambda = lambda data: True
            if (not match.group(3) == None):
                iflambda = createtester(match.group(3))

            result.append((index, deep, 'F', match.group(2), select(match.group(2)), iflambda))
        elif ((match.group(1) == 'A')or(match.group(1) == 'AGGREGATE')): #aggregate
            params = [match.group(3)]
            if (',' in params[0]):
                params = match.group(3).split(',')
            iflambda = lambda data: True
            if (len(params) > 1):
                iflambda = createtester(params[1])

            result.append((index, deep, 'A', match.group(2), agregate(params[0], match.group(2))))
        elif (match.group(1) == 'I'):
            result.append((index, deep, 'P', match.group(2), softprinter(match.group(2))))
        elif (match.group(1) == 'FILTER'):
            params = [match.group(3)]
            iflambda = createtester(params[0])
            result.append((index, deep, 'FILTER', '', filterit(iflambda)))
            pass
        elif (match.group(1) == 'E'):
            ltype = types[-1]
            #print(types)
            types = types[0:-1]
            #yield 'E:' + str(names) + '; ' + str(types)
            result.append((index, deep, 'E', '', lambda printer, i: i))
            sub = []
            while result[-1][1] == deep:
                sub += [result.pop()]
            sub.reverse()
            #print('reversed sub', str(sub))
            funclisttorun = list(map(lambda item: item[4], sub))
            #funclisttorun = [item for sublist in funclisttorun for item in sublist]
            #print('reversed sub', str(funclisttorun))
            deep -= 1
            if (ltype == 'W'):
                result.append((index, deep, 'subroutine:', '', subroutine(funclisttorun, sub[0][5])))
                #result.append((index, deep, 'subroutine:', '', subroutine(funclisttorun)))
            elif (ltype == 'F'):
                wraped = [funclisttorun[0]]
                wraped += [iterator(funclisttorun[1:], sub[0][5])]
                #wraped += [iterator(funclisttorun[1:])]
                result.append((index, deep, 'subroutine:', '', subroutine(wraped)))


    for item in result:
        print(item)
    funclisttorun = list(map(lambda item: item[4], result))
    if (not result[-1][1] == 0):
        print ('ERROR, [[E]] missing')
        print (result[-2])

    return subroutine(funclisttorun)
