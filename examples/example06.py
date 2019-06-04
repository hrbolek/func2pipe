import func2pipe as fp

@fp.pipesub(lambda input, output: {'source': input, 'letters': output })
@fp.pipecollecttoarray
@fp.pipefind(r"[A-Z]", mapper = lambda item: item.group(0))
@fp.pipeit
def letters(item, b):
    return item + b

resultcreator = fp.createpipe([
    letters(b = 'x')
    ], closewitharray = True)


sourceA = ['ABCDEF', 'GHIJKL']
sourceB = ['MNOPQR', 'STUVWX']

print('first set')
result = resultcreator(sourceA)
print(result)
print('second set')
result = resultcreator(sourceB)
print(result)