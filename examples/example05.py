import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letter': output })
@fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
@fp.pipeit
def letters(item, append):
    return item + append

resultcreator = fp.createpipe([
    letters(append = 'x')
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)