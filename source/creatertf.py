
import io
import os
import re

def compile_template(template):

    regexTester = re.compile(r'((?:\[\[)(?:[A-Z])(?:\:(?:[a-z_A-Z0-9]+))?(?:\((?:[^\)]+)\))?(?:\]\]))')
#    last = 0
#    for match in regexTester.finditer(template):
#        yield match
    templatelist = regexTester.split(template)

    regexTester = re.compile(r'(?:\[\[)([A-Z])(?:\:([a-z_A-Z0-9]+))?(?:\(([^\)]+)\))?(?:\]\])')
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
        for c in data:
            code = ord(c)
            if (code > 127):
                result += '\\u' + str(code)+ 'G'
            else:
                result += c
        return result

    def softprinter(name):
        def result(printer, data):
            #print('softprinter enter', '|'+name+'|', str(data)[0:200])
            #print('softprinter enter', 'len', str(data[0])[0:200])
            #print(data[name].encode('unicode_escape').decode('ansi'))
            printer(uuesc(data[name]))#.encode('unicode_escape').decode('ansi'))
#            printer(data[name].encode('unicode_escape').decode('ansi'))
#            print('softprinter leave')
            return data
        return result

    def subroutine(funclist):
        #print('subroutine on', str(funclist))
        def result(printer, data):
            #print('subroutine enter', str(data))
            subdata = data
            for f in funclist:
                subdata = f(printer, subdata)
            #print('subroutine leave', str(data))
            return data
        return result

    def iterator(funclist):
        #print('iterator on', str(funclist))
        def result(printer, data):
            #print('iterator enter', str(data))
            for item in data:
                #print('iterator item', str(item))
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

    while (index < len(templatelist) - 1):
        index += 1
        item = templatelist[index]
        match = regexTester.match(item)
        if (match == None):
            result.append((index, deep, 'O', item[0:10], hardprinter(item)))
        elif (match.group(1) == 'W'):
            types += ['W']
            deep += 1
            result.append((index, deep, 'W', match.group(2), select(match.group(2))))
        elif (match.group(1) == 'F'):
            types += ['F']
            deep += 1
            result.append((index, deep, 'F', match.group(2), select(match.group(2))))
        elif (match.group(1) == 'I'):
            result.append((index, deep, 'P', match.group(2), softprinter(match.group(2))))
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
                result.append((index, deep, 'subroutine:', '', subroutine(funclisttorun)))
            if (ltype == 'F'):
                wraped = [funclisttorun[0]]
                wraped += [iterator(funclisttorun[1:])]
                result.append((index, deep, 'subroutine:', '', subroutine(wraped)))

    print(result)
    funclisttorun = list(map(lambda item: item[4], result))
    if (not result[-1][1] == 0):
        print ('ERROR, [[E]] missing')

    return subroutine(funclisttorun)
