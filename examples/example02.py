import func2pipe as fp

@fp.pipeit
def addone(item):
    return item + 1

@fp.pipeit
def add(a, b):
    return a + b

@fp.pipesub(lambda input, output: {'i': input, 'o': output})
@fp.pipeit
def transform(item):
    if (item > 12):
        return True
    else:
        return False

@fp.pipesub(lambda input, output: {'i': input, **output})
@fp.pipeit
def transform2(item, fixed):
    if (item > 12):
        return {'r': True, 'f': fixed }
    else:
        return {'r': False, 'f': fixed }

resultcreator = fp.createpipe([
    addone(),
    add(b = 4),
    transform2(fixed = 'fixed')
    ], closewitharray = True)

sourceA = iter(range(1, 20))
sourceB = [45, 20, 6]
print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)