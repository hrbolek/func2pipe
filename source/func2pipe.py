from functools import partial, wraps
import re

def pipesub(reducer):
    '''declare pipe as subroutine, allows reduce input and output into one item by reducer
    
    Keyword arguments:
    reducer -- lambda item, result: {**item, 'result': result}
    '''
    def pipesubinner(subpipe):
        @wraps(subpipe)
        def result(generator):
            for item in generator:
                for data in subpipe([item]):
                    toreturn = reducer(item, data)
                    yield toreturn
        return result
    return pipesubinner

def pipefind(pattern, mapper = lambda item: item.group(0), selector = lambda item: item):
    '''allows generate item from single input according to pattern
    
    Keyword arguments:
    pattern -- text or function to define pattern
    mapper -- function to create result
    selector -- function to select text for regex

    '''
    def pipefindinner(subpipe):
        @wraps(subpipe)
        def result(generator):
            for item in subpipe(generator):
                regexTester = ''
                if (callable(pattern)):
                    regexTester = re.compile(pattern(item))
                else:
                    regexTester = re.compile(pattern)
                for match in regexTester.finditer(selector(item)):
                    yield mapper(match)
        return result
    return pipefindinner

def pipeit(func):
    '''builds pipe(generator) from simple function'''
    @wraps(func)
    def innerselect(generator):
        for i in generator:

            yield func(i)
    return innerselect

def pipeitwithnamedparams(func):
    '''builds pipe(generator) from simple function'''
    @wraps(func)
    def bindparams(**kwargs):
        def innerselect(generator):
            for i in generator:
                yield func(i, **kwargs)
        return innerselect
    return bindparams

def hasyield(func):
    '''
    expected to be paired with pipeit or pipeitwithnamedparams on functions which use yield
    '''
    @wraps(func)
    def inner(generator):
        for items in func(generator):
            for item in items:
                yield item
    return inner

def pipecollecttoarray(subpipe):
    '''
    collect items form subpipe as a single array
    '''
    @wraps(subpipe)
    def inner(generator):
        for item in generator:
            r = []
            for data in subpipe([item]):
                r += [data]
            yield r
    return inner

def pipeapply(method, pipe = None):
    '''
    very simple func reducer
    result = method(pipe(source))
    '''
    if (pipe == None):
        return method
    else:
        return lambda source: method(pipe(source))

def createpipe(funclist, closewitharray = False, close = False):
    '''
    reduces funclist to create single function with generator as parameter and generator as result
    Keyword arguments:
    closewitharray -- if True, created function returns array
    close -- if True, created function returns nothing but exausted generator
    '''
    result = None
    for method in funclist:
        result = pipeapply(method, result)
    if (close & (not closewitharray)):
        return pipeapply(close, result)
    if (closewitharray):
        return pipeapply(closewithresults, result)
    return result


def close(pipe):
    '''
    expected to be last item in createpipe, closes pipe and allows to create function without result
    '''
    for item in pipe:
        pass

def closewithresults(pipe):
    '''
    expected to be last item in createpipe, closes pipe and allows to create function with list as result
    '''
    result = []
    for item in pipe:
        result.append(item)
    return result

def filter(func = lambda item: True):
    '''
    returns function for filtering items in generator
    '''
    def innerfilter(generator):
        for item in generator:
            if func(item):
                yield item
    return innerfilter

def select(func = lambda item: item):
    '''
    this function is simplier form of

    @pipeit
    def select(item)
        return func(item)
    '''
    def innerselect(generator):
        for item in generator:
            yield func(item)
    return innerselect