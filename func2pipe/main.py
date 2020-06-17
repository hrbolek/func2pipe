from functools import partial, wraps

def createPipe(*F):
  def Fdiamond(sequence):
    result = sequence
    for Fx in F:
      result = Fx(result)
    return result
  return Fdiamond 

def createSub(assign = lambda source, result: {**source, **result}, reducer = None):
    def multipleResults(*F):
        buffer = {'data': None}
        def pre(gen):
            for item in gen:
                buffer['data'] = item
                yield item

        def post(gen):
            for item in gen:
                yield assign(buffer['data'], item)

        wholePipe = createPipe(pre, *F, post)
        return wholePipe

    def reducedResult(*F):
        inner = createPipe(*F, reducer)
        def result(gen):
            for item in gen:
                yield inner([item])

        wholePipe = multipleResults(result)
        return wholePipe

    if reducer == None:
        return multipleResults
    else:
        return reducedResult

def convertToPipeFuncFull(func, with_yield = False, with_state = False, kwargs = {}):
    @wraps(func)
    def innerSelectSimple(generator):
        for i in generator:
            yield func(i, **kwargs)

    if (not with_yield) & (not with_state):
        return innerSelectSimple
    
    @wraps(func)
    def innerSelectWithYield(generator):
        for i in generator:
            for j in func(i, **kwargs):
                yield j


    if (with_yield) & (not with_state):
        return innerSelectWithYield

    @wraps(func)
    def innerSelectWithState(generator):
        state = None
        for i in generator:
            result = None
            if (state):
                result, state = func(i, state = state, **kwargs)
            else:
                result, state = func(i, **kwargs)
            if result:
                yield result

    if (not with_yield) & with_state:
        return innerSelectWithState

    @wraps(func)
    def innerSelectWithYieldWithState(generator):
        state = None
        initState = True
        for i in generator:
            result = None
            if (initState):
                for result, statel in func(i, **kwargs):
                    state = statel
                    if result:
                        yield result
                initState = False
            else:
                for result, statel in func(i, state = state, **kwargs):
                    state = statel
                    if result:
                        yield result


    return innerSelectWithYieldWithState

def convertToPipeFunc(with_yield = False, with_state = False):
    def pipeit(__func):
        @wraps(__func)
        def binder(**kwargs):
            result = wraps(__func)(convertToPipeFuncFull(__func, with_yield, with_state, kwargs))
            return result
        return binder
    return pipeit

convertToPipeFunc2 = convertToPipeFunc 
pipeit = convertToPipeFunc 
