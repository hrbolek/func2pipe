import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letter': output })
@fp.hasyield
@fp.pipeit
def letters(item):
    for letter in item:
        yield letter

resultcreator = fp.createpipe([
    letters()
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)