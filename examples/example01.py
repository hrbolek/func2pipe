import func2pipe as fp

@fp.pipeit
def addone(item):
    return item + 1

@fp.pipeit
def add(a, b):
    return a + b

resultcreator = fp.createpipe([
    addone(),
    add(b = 4),
    ], closewitharray = True)


sourceA = iter(range(1, 20))
sourceB = [45, 20, 6]
print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)