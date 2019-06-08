import func2pipe as fp
from functools import reduce

@fp.pipeit()
def replace(line, original, replacement):
    result = str(line).replace(original, replacement)
    return result

@fp.pipeit()
def intocolumns(line, separator):
    result = str(line).split(separator)
    return result

@fp.pipeit()
def intotext(cols, separator):
    result = reduce(lambda x, y: x + separator + y, cols.values())
    return result

@fp.pipeit()
def namecols(cols, names):
    result = {}
    for nn in zip(names, range(0, 100)):
        result[nn[0]] = cols[nn[1]]
    return result

@fp.pipeit()
def addcol(cols, name, func):
    result = { **cols, name: func(cols) }
    return result

@fp.pipeit()
def removecol(cols, name):
    result = { **cols }
    if name in result:
        del result[name]
    return result

@fp.pipeit()
def splitcol(cols, colname, separator, colnames):
    result = {**cols}
    splitted = str(cols[colname]).split(separator)
    for name, value in zip(colnames, splitted):
        result[name] = value
    return result

@fp.pipeit(with_state = True, with_yield = True)
def uniquerow(cols, colname, state = []):
    current = cols[colname]
    if not current in state:
        newstate = state
        newstate.append(current)
        yield cols, newstate

def groupby(cols, colname, reducers, state = {}):
    current = cols[colname]
    