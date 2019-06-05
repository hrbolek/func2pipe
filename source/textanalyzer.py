import func2pipe as fp
from functools import reduce

@fp.pipeitwithnamedparams
def replace(line, original, replacement):
    result = str(line).replace(original, replacement)
    return result

@fp.pipeitwithnamedparams
def intocolumns(line, separator):
    result = str(line).split(separator)
    return result

@fp.pipeitwithnamedparams
def intotext(cols, separator):
    result = reduce(lambda x, y: x + separator + y, cols.values())
    return result

@fp.pipeitwithnamedparams
def namecols(cols, names):
    result = {}
    for nn in zip(names, range(0, 100)):
        result[nn[0]] = cols[nn[1]]
    return result

@fp.pipeitwithnamedparams
def addcol(cols, name, func):
    result = { **cols, name: func(cols) }
    return result

@fp.pipeitwithnamedparams
def removecol(cols, name):
    result = { **cols }
    if name in result:
        del result[name]
    return result

