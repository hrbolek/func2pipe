import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letter': output })
@fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
def letters(item):
    return item

resultcreator = fp.createpipe([
    letters
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)