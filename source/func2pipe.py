from functools import partial, wraps
import re

def pipesub_(reducer):
    '''declare pipe as subroutine, allows reduce input and output into one item by reducer
    
    Keyword arguments:
    reducer -- lambda item, result: {**item, 'result': result}
    '''
    def pipesubinner(subpipe):
        @wraps(subpipe)
        def binder(**kwargs):
            preparedsubpipe = subpipe(**kwargs)
            def result(generator):
                for item in generator:
                    for data in preparedsubpipe([item]):
                        toreturn = reducer(item, data)
                        yield toreturn
            return result
        return binder
    return pipesubinner

def pipesub(reducer):
    '''declare pipe as subroutine, allows reduce input and output into one item by reducer
    
    Keyword arguments:
    reducer -- lambda item, result: {**item, 'result': result}
    '''
    def pipesubinner(subpipe):
        @wraps(subpipe)
        def binder(**kwargs):
            preparedsubpipe = subpipe(**kwargs)
            def result(generator):
                buffer = {'currentItem': None}
                def bufferit(gen):
                    for item in gen:
                        buffer['currentItem'] = item
                        yield item
                for item in preparedsubpipe(bufferit(generator)):
                    yield reducer(buffer['currentItem'], item)
            return result
        return binder
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
        def binder(**kwargs):
            preparedsubpipe = subpipe(**kwargs)
            def result(generator):
                for item in preparedsubpipe(generator):
                    regexTester = ''
                    if (callable(pattern)):
                        regexTester = re.compile(pattern(item))
                    else:
                        regexTester = re.compile(pattern)
                    for match in regexTester.finditer(selector(item)):
                        yield mapper(match)
            return result
        return binder
    return pipefindinner

def pipeit(with_yield = False, with_state = False):
    def pipeitsimple(func):
        '''builds pipe(generator) from simple function'''
        @wraps(func)
        def bindparams(**kwargs):
            def innerselect(generator):
                for i in generator:
                    yield func(i, **kwargs)
            return innerselect
        return bindparams

    if (not with_yield) & (not with_state):
        return pipeitsimple
    
    preparedfunc = lambda func: func
    def hasyield(func):
        '''
        expected to be paired with pipeitwithnamedparams on functions which use yield
        '''
        @wraps(func)
        def bindparams(**kwargs):
            preparedfunc = func(**kwargs)
            def inner(generator):
                for items in preparedfunc(generator):
                    for item in items:
                        yield item
            return inner
        return bindparams

    if (with_yield) & (not with_state):
        result = lambda func: hasyield(pipeitsimple(func))
        return result

    def pipeitwithstate(func):
        '''builds pipe(generator) from simple function'''
        @wraps(func)
        def bindparams(**kwargs):
            def innerselect(generator):
                state = None
                initState = True
                for i in generator:
                    result = None
                    if (initState):
                        result, state = func(i, **kwargs)
                        initState = False
                    else:
                        result, state = func(i, state = state, **kwargs)
                    yield result

            return innerselect
        return bindparams
    if (not with_yield) & with_state:
        return pipeitwithstate

    '''
                buffer = {'currentItem': None}
                def bufferit(gen):
                    for item in gen:
                        buffer['currentItem'] = item
                        yield item

    '''

    def pipeitwithstatewithyield(func):
        '''builds pipe(generator) from simple function'''
        @wraps(func)
        def bindparams(**kwargs):
            def innerselect(generator):
                state = None
                initState = True
                for i in generator:
                    result = None
                    if (initState):
                        for result, statel in func(i, **kwargs):
                            state = statel
                            initState = False
                            if not result == None:
                                yield result
                    else:
                        for result, statel in func(i, state = state, **kwargs):
                            state = statel
                            if not result == None:
                                yield result

            return innerselect
        return bindparams
    return pipeitwithstatewithyield

def pipecollecttoarray(subpipe):
    '''
    collect items from subpipe as a single array
    '''
    @wraps(subpipe)
    def binder(**kwargs):
        preparedsubpipe = subpipe(**kwargs)
        def result(generator):
            for item in generator:
                r = []
                for data in preparedsubpipe([item]):
                    r.append(data)
                yield r
        return result
    return binder

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

def filter2(func = lambda item: True):
    '''
    returns function for filtering items in generator
    '''
    def innerfilter(generator):
        for item in generator:
            if func(item):
                yield item
    return innerfilter


@pipeit(with_yield = True)
def filter(item, funcfilter = lambda item: True):
    '''
    function for filtering items in generator
    '''
    if (funcfilter(item)):
        yield item

@pipeit()
def select(item, func = lambda item: item):
    return func(item)
