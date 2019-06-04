import func2pipe as fp

@fp.hasyield
@fp.pipeit
def letters(item, spec):
    for letter in item:
        yield letter + spec

resultcreator = fp.createpipe([
    letters(spec = '-')
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)